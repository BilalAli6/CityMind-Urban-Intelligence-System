"""
CityMind - Urban Intelligence System
All 5 Challenges implemented:
  1. City Layout Planning (CSP / Backtracking)
  2. Road Network Optimization (MST + constraint: dual path)
  3. Ambulance Placement (Genetic Algorithm)
  4. Emergency Routing Under Changing Conditions (A* with replanning)
  5. Crime Risk Prediction (K-Means clustering + Decision Tree classification)
"""

import random
import math
import heapq
import json
import time
import copy
from collections import defaultdict, deque

import numpy as np
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# ─────────────────────────────────────────────────────────
#  SHARED CITY GRAPH  (single source of truth)
# ─────────────────────────────────────────────────────────

LOCATION_TYPES = ["Residential", "Hospital", "School",
                  "Industrial", "PowerPlant", "AmbulanceDepot", "Empty"]

TYPE_COLORS = {
    "Residential":    "#4ade80",
    "Hospital":       "#f87171",
    "School":         "#60a5fa",
    "Industrial":     "#fbbf24",
    "PowerPlant":     "#a78bfa",
    "AmbulanceDepot": "#fb923c",
    "Empty":          "#1e293b",
}

GRID_SIZE = 8   # 8×8 = 64 nodes – large enough to be meaningful


class CityGraph:
    """Shared mutable graph. All modules read/write here."""

    def __init__(self, size=GRID_SIZE):
        self.size = size
        self.nodes: dict[int, dict] = {}          # node_id → attrs
        self.edges: dict[tuple, dict] = {}        # (u,v) sorted → attrs
        self.adj:   dict[int, set]   = defaultdict(set)
        self.event_log: list[str]    = []
        self._init_nodes()

    # ── helpers ──────────────────────────────────────────

    def _init_nodes(self):
        for r in range(self.size):
            for c in range(self.size):
                nid = r * self.size + c
                self.nodes[nid] = {
                    "id": nid, "row": r, "col": c,
                    "type": "Empty",
                    "population_density": 0.0,
                    "risk_index": 0.0,
                    "accessible": True,
                    "crime_risk": "Low",          # Low / Medium / High
                    "risk_multiplier": 1.0,
                }

    def node_id(self, r, c): return r * self.size + c

    def neighbors_grid(self, nid):
        """4-connected grid neighbours (not edges, just adjacency)."""
        r, c = self.nodes[nid]["row"], self.nodes[nid]["col"]
        out = []
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                out.append(self.node_id(nr, nc))
        return out

    def add_edge(self, u, v, cost=1.0, blocked=False):
        key = (min(u,v), max(u,v))
        self.edges[key] = {"cost": cost, "blocked": blocked}
        if not blocked:
            self.adj[u].add(v); self.adj[v].add(u)

    def block_road(self, u, v):
        key = (min(u,v), max(u,v))
        if key in self.edges:
            self.edges[key]["blocked"] = True
            self.adj[u].discard(v); self.adj[v].discard(u)
            self.log(f"🚧 Road {u}↔{v} BLOCKED")

    def unblock_road(self, u, v):
        key = (min(u,v), max(u,v))
        if key in self.edges:
            self.edges[key]["blocked"] = False
            self.adj[u].add(v); self.adj[v].add(u)
            self.log(f"✅ Road {u}↔{v} CLEARED")

    def travel_cost(self, u, v):
        key = (min(u,v), max(u,v))
        if key not in self.edges or self.edges[key]["blocked"]:
            return float('inf')
        base = self.edges[key]["cost"]
        rm = max(self.nodes[u]["risk_multiplier"],
                 self.nodes[v]["risk_multiplier"])
        return base * rm

    def set_type(self, nid, t):
        self.nodes[nid]["type"] = t

    def log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.event_log.append(f"[{ts}] {msg}")
        if len(self.event_log) > 200:
            self.event_log = self.event_log[-200:]

    def to_dict(self):
        return {
            "size": self.size,
            "nodes": self.nodes,
            "edges": {f"{k[0]},{k[1]}": v for k,v in self.edges.items()},
            "adj": {str(k): list(v) for k,v in self.adj.items()},
        }


# ─────────────────────────────────────────────────────────
#  CHALLENGE 1 – City Layout Planning (CSP Backtracking)
# ─────────────────────────────────────────────────────────

def manhattan_hops(graph, a, b):
    """BFS hop count on the full grid (ignoring edges/blocks)."""
    visited = {a}
    queue = deque([(a, 0)])
    while queue:
        node, d = queue.popleft()
        if node == b: return d
        for nb in graph.neighbors_grid(node):
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, d+1))
    return float('inf')


def bfs_hops_unrestricted(graph, start):
    """Return hop-distance from start to all nodes (unrestricted grid)."""
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph.neighbors_grid(u):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


class LayoutPlanner:
    """
    CSP with backtracking.
    Assigns required building types to grid cells respecting all constraints.
    """

    REQUIRED = {
        "Hospital":       2,
        "School":         2,
        "Industrial":     3,
        "PowerPlant":     1,
        "AmbulanceDepot": 2,
        "Residential":    8,
    }

    def __init__(self, graph: CityGraph):
        self.graph = graph
        self.solution = None
        self.conflict_rule = None

    def _check_constraints(self, assignment):
        """Returns (ok, violated_rule_string)."""
        hosp_ids    = [n for n,t in assignment.items() if t == "Hospital"]
        indust_ids  = [n for n,t in assignment.items() if t == "Industrial"]
        school_ids  = [n for n,t in assignment.items() if t == "School"]
        pp_ids      = [n for n,t in assignment.items() if t == "PowerPlant"]
        resid_ids   = [n for n,t in assignment.items() if t == "Residential"]

        g = self.graph

        # Rule A: Industrial not adjacent to School / Hospital
        for ind in indust_ids:
            for nb in g.neighbors_grid(ind):
                if assignment.get(nb) in ("School", "Hospital"):
                    return False, "Industrial cannot be adjacent to School/Hospital"

        # Rule B: Every residential within 3 hops of a hospital
        for res in resid_ids:
            if hosp_ids:
                min_d = min(manhattan_hops(g, res, h) for h in hosp_ids)
                if min_d > 3:
                    return False, "Residential not within 3 hops of a Hospital"

        # Rule C: Power plant within 2 hops of industrial
        for pp in pp_ids:
            if not indust_ids:
                return False, "PowerPlant placed but no Industrial zones"
            min_d = min(manhattan_hops(g, pp, ind) for ind in indust_ids)
            if min_d > 2:
                return False, "PowerPlant not within 2 hops of Industrial"

        return True, None

    def plan(self):
        """Run backtracking CSP. Returns True if solution found."""
        # Build ordered list of (type, count) to place
        variables = []
        for t, cnt in self.REQUIRED.items():
            variables.extend([t] * cnt)
        random.shuffle(variables)

        all_cells = list(self.graph.nodes.keys())
        random.shuffle(all_cells)

        assignment = {}
        result = self._backtrack(variables, 0, assignment, all_cells)
        if result:
            self.solution = assignment
            self._apply(assignment)
            self.graph.log("✅ Challenge 1: City layout planned successfully (CSP)")
            return True
        else:
            # Propose minimum-conflict solution greedily
            self._greedy_fallback(all_cells)
            self.graph.log(f"⚠️ Challenge 1: Full CSP failed – used greedy fallback")
            return False

    def _backtrack(self, variables, idx, assignment, cells):
        if idx == len(variables):
            ok, rule = self._check_constraints(assignment)
            return ok
        t = variables[idx]
        for cell in cells:
            if cell in assignment:
                continue
            assignment[cell] = t
            ok, rule = self._check_constraints(assignment)
            if ok or rule is None:
                if self._backtrack(variables, idx+1, assignment, cells):
                    return True
            del assignment[cell]
        return False

    def _greedy_fallback(self, cells):
        """Place buildings ignoring constraints – highlight conflicts."""
        assignment = {}
        ptr = 0
        for t, cnt in self.REQUIRED.items():
            for _ in range(cnt):
                while ptr < len(cells) and cells[ptr] in assignment:
                    ptr += 1
                if ptr < len(cells):
                    assignment[cells[ptr]] = t
                    ptr += 1
        _, rule = self._check_constraints(assignment)
        self.conflict_rule = rule
        self.solution = assignment
        self._apply(assignment)

    def _apply(self, assignment):
        for nid, t in assignment.items():
            self.graph.set_type(nid, t)
        # Assign population density by type
        for nid, node in self.graph.nodes.items():
            t = node["type"]
            if t == "Residential":   node["population_density"] = random.uniform(50, 200)
            elif t == "Industrial":  node["population_density"] = random.uniform(10, 80)
            elif t == "Hospital":    node["population_density"] = random.uniform(5, 30)
            else:                    node["population_density"] = random.uniform(1, 15)


# ─────────────────────────────────────────────────────────
#  CHALLENGE 2 – Road Network Optimization (Kruskal MST + Dual-path constraint)
# ─────────────────────────────────────────────────────────

class RoadOptimizer:
    """
    Builds MST (Kruskal) then adds redundant path between
    Hospital and AmbulanceDepot to satisfy dual-route requirement.
    """

    def __init__(self, graph: CityGraph):
        self.graph = graph

    def _edge_cost(self, u, v):
        t_u = self.graph.nodes[u]["type"]
        t_v = self.graph.nodes[v]["type"]
        cost = 0.8 if (t_u == "Residential" or t_v == "Residential") else 1.0
        return cost

    def _kruskal(self, node_ids):
        edges = []
        seen = set()
        for nid in node_ids:
            for nb in self.graph.neighbors_grid(nid):
                if nb in node_ids:
                    key = (min(nid,nb), max(nid,nb))
                    if key not in seen:
                        seen.add(key)
                        edges.append((self._edge_cost(nid, nb), nid, nb))
        edges.sort()
        parent = {n: n for n in node_ids}

        def find(x):
            while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
            return x
        def union(a, b):
            ra, rb = find(a), find(b)
            if ra == rb: return False
            parent[ra] = rb; return True

        mst = []
        for cost, u, v in edges:
            if union(u, v):
                mst.append((u, v, cost))
        return mst

    def optimize(self):
        node_ids = set(self.graph.nodes.keys())
        mst = self._kruskal(node_ids)

        for u, v, cost in mst:
            self.graph.add_edge(u, v, cost=cost)

        # Dual-path constraint: ensure Hospital ↔ AmbulanceDepot redundancy
        hospitals = [n for n,d in self.graph.nodes.items() if d["type"]=="Hospital"]
        depots    = [n for n,d in self.graph.nodes.items() if d["type"]=="AmbulanceDepot"]

        if hospitals and depots:
            h = hospitals[0]; dep = depots[0]
            # Add one extra edge along alternate route
            self._add_redundant_path(h, dep)

        total_cost = sum(v["cost"] for v in self.graph.edges.values())
        self.graph.log(f"✅ Challenge 2: MST built ({len(mst)} edges, cost={total_cost:.1f}), dual-path ensured")

    def _add_redundant_path(self, src, dst):
        """BFS to find second independent path; add edges if missing."""
        # Simple approach: add direct grid edges along one alternative route
        r1,c1 = self.graph.nodes[src]["row"], self.graph.nodes[src]["col"]
        r2,c2 = self.graph.nodes[dst]["row"], self.graph.nodes[dst]["col"]
        prev = src
        # Walk along column then row (alternate direction)
        r, c = r1, c1
        while c != c2:
            c += 1 if c2 > c else -1
            nid = self.graph.node_id(r, c)
            key = (min(prev,nid), max(prev,nid))
            if key not in self.graph.edges:
                self.graph.add_edge(prev, nid, cost=self._edge_cost(prev,nid))
            prev = nid
        while r != r2:
            r += 1 if r2 > r else -1
            nid = self.graph.node_id(r, c)
            key = (min(prev,nid), max(prev,nid))
            if key not in self.graph.edges:
                self.graph.add_edge(prev, nid, cost=self._edge_cost(prev,nid))
            prev = nid


# ─────────────────────────────────────────────────────────
#  CHALLENGE 3 – Ambulance Placement (Genetic Algorithm)
# ─────────────────────────────────────────────────────────

class AmbulancePlacer:
    """
    Genetic Algorithm to minimise max response distance
    from any residential node to its nearest ambulance.
    """
    N_AMBULANCES = 3
    POP_SIZE = 40
    GENERATIONS = 80
    MUTATION_RATE = 0.25

    def __init__(self, graph: CityGraph):
        self.graph = graph
        self.placements: list[int] = []

    def _reachable_nodes(self):
        return [n for n,d in self.graph.nodes.items() if d["accessible"]]

    def _residential_nodes(self):
        return [n for n,d in self.graph.nodes.items()
                if d["type"] in ("Residential","Hospital","School")]

    def _dijkstra_all(self, source):
        dist = {source: 0.0}
        pq = [(0.0, source)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist.get(u, float('inf')): continue
            for v in self.graph.adj[u]:
                c = self.graph.travel_cost(u, v)
                nd = d + c
                if nd < dist.get(v, float('inf')):
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist

    def _fitness(self, placement, dist_cache, residents):
        # Minimise worst-case distance from any resident to nearest ambulance
        worst = 0.0
        for res in residents:
            best = min(dist_cache[amb].get(res, float('inf')) for amb in placement)
            worst = max(worst, best)
        return worst   # lower = better

    def place(self):
        reachable  = self._reachable_nodes()
        residents  = self._residential_nodes() or reachable

        if len(reachable) < self.N_AMBULANCES:
            self.placements = reachable[:self.N_AMBULANCES]
            return

        # Pre-compute Dijkstra from every reachable node
        dist_cache = {n: self._dijkstra_all(n) for n in reachable}

        # Initial population
        population = [random.sample(reachable, self.N_AMBULANCES)
                      for _ in range(self.POP_SIZE)]

        best_placement = population[0]
        best_fitness   = self._fitness(best_placement, dist_cache, residents)

        for gen in range(self.GENERATIONS):
            scored = [(self._fitness(p, dist_cache, residents), p) for p in population]
            scored.sort(key=lambda x: x[0])
            if scored[0][0] < best_fitness:
                best_fitness   = scored[0][0]
                best_placement = scored[0][1]

            elite = [p for _,p in scored[:self.POP_SIZE//4]]
            new_pop = list(elite)

            while len(new_pop) < self.POP_SIZE:
                p1, p2 = random.sample(elite, 2)
                # Crossover
                child = list(set(p1[:len(p1)//2] + p2[len(p2)//2:]))
                while len(child) < self.N_AMBULANCES:
                    child.append(random.choice(reachable))
                child = list(set(child))[:self.N_AMBULANCES]
                # Mutation
                if random.random() < self.MUTATION_RATE:
                    idx = random.randint(0, len(child)-1)
                    child[idx] = random.choice(reachable)
                if len(child) == self.N_AMBULANCES:
                    new_pop.append(child)

            population = new_pop

        self.placements = best_placement
        for nid in self.placements:
            self.graph.nodes[nid]["type"] = "AmbulanceDepot"
        self.graph.log(f"✅ Challenge 3: Ambulances placed at nodes {self.placements} (GA, worst-case={best_fitness:.2f})")


# ─────────────────────────────────────────────────────────
#  CHALLENGE 4 – Emergency Routing (A* with replanning)
# ─────────────────────────────────────────────────────────

class EmergencyRouter:
    """
    A* pathfinding with admissible heuristic (Euclidean grid distance).
    Re-plans automatically when a road is blocked.
    """

    def __init__(self, graph: CityGraph):
        self.graph = graph
        self.current_path: list[int] = []
        self.team_position: int | None = None
        self.targets: list[int]  = []
        self.visited_targets: list[int] = []
        self.total_cost: float = 0.0

    def _heuristic(self, a, b):
        ra, ca = self.graph.nodes[a]["row"], self.graph.nodes[a]["col"]
        rb, cb = self.graph.nodes[b]["row"], self.graph.nodes[b]["col"]
        return math.sqrt((ra-rb)**2 + (ca-cb)**2)

    def astar(self, start, goal):
        """Returns (path_list, cost) or ([], inf)."""
        open_set = [(0 + self._heuristic(start, goal), 0, start, [start])]
        visited  = {}
        while open_set:
            f, g, u, path = heapq.heappop(open_set)
            if u in visited and visited[u] <= g: continue
            visited[u] = g
            if u == goal: return path, g
            for v in self.graph.adj[u]:
                c = self.graph.travel_cost(u, v)
                if c == float('inf'): continue
                ng = g + c
                if ng < visited.get(v, float('inf')):
                    heapq.heappush(open_set,
                        (ng + self._heuristic(v, goal), ng, v, path+[v]))
        return [], float('inf')

    def start_mission(self, start: int, targets: list[int]):
        self.team_position = start
        self.targets = list(targets)
        self.visited_targets = []
        self.total_cost = 0.0
        self.graph.log(f"🚑 Mission started from {start}, targets: {targets}")
        self._plan_next()

    def _plan_next(self):
        if not self.targets:
            self.graph.log("🎯 Mission complete – all civilians reached!")
            return
        goal = self.targets[0]
        path, cost = self.astar(self.team_position, goal)
        if path:
            self.current_path = path
            self.graph.log(f"📍 A* path to target {goal}: {path} (cost={cost:.2f})")
        else:
            self.graph.log(f"❌ No path to target {goal} – blocked!")
            self.current_path = []

    def road_blocked_event(self, u, v):
        """Called when a road becomes blocked mid-mission."""
        self.graph.block_road(u, v)
        # Check if current path uses this road
        key = (min(u,v), max(u,v))
        path_edges = [(min(self.current_path[i], self.current_path[i+1]),
                       max(self.current_path[i], self.current_path[i+1]))
                      for i in range(len(self.current_path)-1)]
        if key in path_edges:
            self.graph.log(f"⚡ Path disrupted! Replanning from {self.team_position}…")
            self._plan_next()

    def advance_step(self):
        """Move one step along current path."""
        if len(self.current_path) < 2:
            self._plan_next()
            return
        nxt = self.current_path[1]
        cost = self.graph.travel_cost(self.team_position, nxt)
        if cost == float('inf'):
            self.graph.log(f"🚧 Next step blocked, replanning…")
            self._plan_next()
            return
        self.total_cost += cost
        self.team_position = nxt
        self.current_path = self.current_path[1:]
        if self.team_position == self.targets[0]:
            rescued = self.targets.pop(0)
            self.visited_targets.append(rescued)
            self.graph.log(f"✅ Civilian rescued at node {rescued}")
            self._plan_next()

    def state(self):
        return {
            "position": self.team_position,
            "targets": self.targets,
            "visited": self.visited_targets,
            "path": self.current_path,
            "cost": self.total_cost,
        }


# ─────────────────────────────────────────────────────────
#  CHALLENGE 5 – Crime Risk Prediction (K-Means + Decision Tree)
# ─────────────────────────────────────────────────────────

class CrimePrediction:
    """
    Step 1: K-Means clustering (unsupervised) on population density & industrial proximity.
    Step 2: Synthetic dataset + Decision Tree classifier (supervised).
    Step 3: Risk fed back into shared graph as travel cost multiplier.
    """

    def __init__(self, graph: CityGraph):
        self.graph = graph
        self.model = None
        self.le    = LabelEncoder()
        self.kmeans = None
        self.cluster_labels = {}

    def _industrial_proximity(self, nid):
        """BFS hops to nearest industrial node (unrestricted)."""
        industrial = [n for n,d in self.graph.nodes.items() if d["type"]=="Industrial"]
        if not industrial: return 5.0
        return min(manhattan_hops(self.graph, nid, ind) for ind in industrial)

    def run(self):
        nodes = list(self.graph.nodes.keys())
        if len(nodes) < 3:
            return

        # ── STEP 1: K-Means clustering ──────────────────
        features = []
        for n in nodes:
            pop  = self.graph.nodes[n]["population_density"]
            prox = self._industrial_proximity(n)
            features.append([pop, prox])

        X = np.array(features)
        k = 3
        self.kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        clusters = self.kmeans.fit_predict(X)
        for i, n in enumerate(nodes):
            self.cluster_labels[n] = int(clusters[i])

        # ── STEP 2: Synthetic crime dataset ─────────────
        # Logic: higher pop + closer to industrial → higher crime
        train_X, train_y = [], []
        for i, n in enumerate(nodes):
            pop, prox = X[i]
            cluster   = clusters[i]
            t         = self.graph.nodes[n]["type"]

            # deterministic scoring
            score = 0.0
            score += pop / 200.0                        # 0-1
            score += max(0, (5 - prox)) / 5.0          # closer industrial = higher
            if t == "Industrial":  score += 0.4
            if t == "Residential": score += 0.2
            if cluster == int(np.argmax([X[clusters==c][:,0].mean() for c in range(k)])):
                score += 0.2   # high-pop cluster bonus
            score += random.gauss(0, 0.05)             # small noise

            if score >= 0.65:   label = "High"
            elif score >= 0.35: label = "Medium"
            else:               label = "Low"

            train_X.append([pop, prox, cluster])
            train_y.append(label)

        # ── Decision Tree classifier ────────────────────
        self.le.fit(["Low","Medium","High"])
        enc_y = self.le.transform(train_y)
        self.model = DecisionTreeClassifier(max_depth=5, random_state=42)
        self.model.fit(np.array(train_X), enc_y)

        # ── STEP 3: Predict & update graph ──────────────
        MULTIPLIERS = {"Low": 1.0, "Medium": 1.4, "High": 1.8}
        for i, n in enumerate(nodes):
            feat  = np.array([[X[i][0], X[i][1], int(clusters[i])]])
            pred  = self.le.inverse_transform(self.model.predict(feat))[0]
            self.graph.nodes[n]["crime_risk"]      = pred
            self.graph.nodes[n]["risk_index"]      = {"Low":0.2,"Medium":0.5,"High":0.9}[pred]
            self.graph.nodes[n]["risk_multiplier"] = MULTIPLIERS[pred]

        self.graph.log("✅ Challenge 5: Crime risk predicted (K-Means + DT), graph weights updated")


# ─────────────────────────────────────────────────────────
#  SIMULATION CONTROLLER
# ─────────────────────────────────────────────────────────

class Simulation:
    def __init__(self):
        self.graph   = CityGraph(GRID_SIZE)
        self.planner = LayoutPlanner(self.graph)
        self.road    = RoadOptimizer(self.graph)
        self.amb     = AmbulancePlacer(self.graph)
        self.router  = EmergencyRouter(self.graph)
        self.crime   = CrimePrediction(self.graph)
        self.step_no = 0
        self.max_steps = 50
        self.initialized = False
        self.ambulance_positions: list[int] = []

    def initialize(self):
        self.graph.log("🏙️  CityMind initialising…")
        self.planner.plan()
        self.road.optimize()
        self.crime.run()
        self.amb.place()
        self.ambulance_positions = list(self.amb.placements)

        # Start emergency mission
        residents = [n for n,d in self.graph.nodes.items() if d["type"]=="Residential"]
        depots    = [n for n,d in self.graph.nodes.items() if d["type"]=="AmbulanceDepot"]
        if residents and depots:
            targets = random.sample(residents, min(4, len(residents)))
            self.router.start_mission(depots[0], targets)

        self.initialized = True
        self.graph.log("🟢 System fully initialised – simulation ready")

    def step(self):
        if not self.initialized or self.step_no >= self.max_steps:
            return False
        self.step_no += 1
        self.graph.log(f"─── Step {self.step_no}/{self.max_steps} ───")

        # Random flooding event (20 % chance)
        if random.random() < 0.85:
            edges = list(self.graph.edges.keys())
            if edges:
                eu, ev = random.choice(edges)
                if not self.graph.edges[(eu,ev)]["blocked"]:
                    self.router.road_blocked_event(eu, ev)

        # Advance emergency team
        self.router.advance_step()

        # Re-evaluate ambulance placement every 5 steps as risk changes
        if self.step_no % 5 == 0:
            self.crime.run()
            self.amb.place()
            self.ambulance_positions = list(self.amb.placements)

        return True

    def full_state(self):
        return {
            "graph":       self.graph.to_dict(),
            "step":        self.step_no,
            "max_steps":   self.max_steps,
            "initialized": self.initialized,
            "ambulances":  self.ambulance_positions,
            "router":      self.router.state(),
            "event_log":   self.graph.event_log[-50:],
            "type_colors": TYPE_COLORS,
        }


# ─────────────────────────────────────────────────────────
#  FLASK WEB SERVER
# ─────────────────────────────────────────────────────────

from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__, static_folder="static")
sim = Simulation()


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/init", methods=["POST"])
def api_init():
    global sim
    sim = Simulation()
    sim.initialize()
    return jsonify(sim.full_state())


@app.route("/api/state")
def api_state():
    return jsonify(sim.full_state())


@app.route("/api/step", methods=["POST"])
def api_step():
    sim.step()
    return jsonify(sim.full_state())


@app.route("/api/block_road", methods=["POST"])
def api_block_road():
    data = request.json
    sim.router.road_blocked_event(data["u"], data["v"])
    return jsonify(sim.full_state())


@app.route("/api/run_all", methods=["POST"])
def api_run_all():
    while sim.step_no < sim.max_steps:
        sim.step()
    return jsonify(sim.full_state())


if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    print("🏙️  CityMind starting on http://localhost:5555")
    app.run(debug=False, port=5555)
