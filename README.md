<div align="center">
<br/>

<!-- BANNER — replace with your actual screenshot -->
<!-- <img src="assets/banner.png" width="100%" alt="CityMind Banner"/> -->

```
    ░█████╗░██╗████████╗██╗   ██╗███╗   ███╗██╗███╗   ██╗██████╗
    ██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝████╗ ████║██║████╗  ██║██╔══██╗
    ██║  ╚═╝██║   ██║    ╚████╔╝ ██╔████╔██║██║██╔██╗ ██║██║  ██║
    ██║  ██╗██║   ██║     ╚██╔╝  ██║╚██╔╝██║██║██║╚██╗██║██║  ██║
    ╚█████╔╝██║   ██║      ██║   ██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
    ╚════╝ ╚═╝   ╚═╝      ╚═╝   ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝
```

<h1>🏙️ CityMind — Urban Intelligence System</h1>

<p><em>A real-time AI-powered smart city simulator where 5 algorithms share one live map and talk to each other</em></p>

<br/>

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-REST_API-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML_Pipeline-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Live-00d4ff?style=for-the-badge&logo=statuspage&logoColor=white)]()

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&pause=1000&color=00D4FF&center=true&vCenter=true&width=600&lines=CSP+City+Layout+%E2%80%94+Constraint+Satisfaction;Kruskal+MST+%E2%80%94+Road+Network+Optimisation;Genetic+Algorithm+%E2%80%94+Ambulance+Placement;A*+Search+%E2%80%94+Real-Time+Emergency+Routing;K-Means+%2B+Decision+Tree+%E2%80%94+Crime+Prediction" alt="Typing SVG" />

<br/><br/>

</div>

---

## 📸 Interface Preview


<div align="center">

| 🗺️ City Layout | 🛣️ Road Network |
|:-:|:-:|
| <!-- <img src="assets/city-layout.png" width="420"/> --> | <!-- <img src="assets/road-network.png" width="420"/> --> |
| <img width="1919" height="946" alt="image" src="https://github.com/user-attachments/assets/caf49336-326b-428c-8086-6605c35b2d6c" /> | <img width="1919" height="946" alt="image" src="https://github.com/user-attachments/assets/f923eb9a-94b9-49a3-beeb-3e7ea36df766" />
 |
| *CSP backtracking assigns every building* | *Kruskal's MST — 63 edges, minimum cost* |

| 🚑 Ambulance Coverage | 🔴 Crime Heatmap |
|:-:|:-:|
| <!-- <img src="assets/ambulance.png" width="420"/> --> | <!-- <img src="assets/heatmap.png" width="420"/> --> |
| <img width="1919" height="950" alt="image" src="https://github.com/user-attachments/assets/a5fcc847-ead9-4e1f-a528-e11e1ab9b263" /> | <img width="1919" height="939" alt="image" src="https://github.com/user-attachments/assets/2592df7a-3039-4694-86c7-d55bd3e136c3" />
 |
| *Genetic Algorithm optimised depot positions* | *K-Means + Decision Tree risk prediction* |

<br/>

<!-- Full UI screenshot — widest one, shows log panel + all overlays -->
<!-- <img src="assets/full-ui.png" width="900"/> -->
<img width="1919" height="937" alt="image" src="https://github.com/user-attachments/assets/175645b5-431b-4aed-8613-f64406737bff" />

<img width="1919" height="935" alt="image" src="https://github.com/user-attachments/assets/3d0c673f-d634-422e-b61b-8a5d26997562" />

<img width="1916" height="928" alt="image" src="https://github.com/user-attachments/assets/7200f41a-51bb-4cad-bd4a-df159eaf0fa9" />




<!-- Optional: animated GIF of the simulation running -->
<!-- <img src="assets/demo.gif" width="900"/> -->
`[🎬 OPTIONAL: PASTE A GIF OF THE SIMULATION RUNNING HERE]`

</div>

---

## 🧠 What Is CityMind?

CityMind is a **fully integrated urban intelligence system** built in Python. It models a growing mid-sized city as an **8×8 grid graph** — 64 nodes, up to 112 roads — and runs **5 AI algorithms simultaneously**, all reading and writing to the same shared city map.

The system runs a **20-step simulation** where:

- 🌊 Roads flood randomly, forcing the emergency team to **replan routes instantly**  
- 📊 Crime risk scores update every 5 steps, **shifting ambulance positions automatically**  
- 🚑 A medical team navigates to trapped civilians using **guaranteed-shortest A\* paths**  
- 🔗 Every module shares **one city graph** — no private copies, no sync issues

> **The architecture rule:** if a road floods, every algorithm knows in the same millisecond.

---

## ⚡ Five Challenges, Five Algorithms

```
               ┌────────────────────────────────────────────────────────────────┐
               │                    SHARED CITY GRAPH                           │
               │                  (single source of truth)                      │
               ├──────────┬──────────┬──────────┬──────────┬────────────────────┤
               │   C1     │   C2     │   C3     │   C4     │        C5          │
               │  CSP     │ Kruskal  │   GA     │   A*     │ K-Means + Dec.Tree │
               │ Layout   │   MST    │  Ambu-   │ Routing  │ Crime Prediction   │
               │Planning  │  Roads   │  lance   │ (live)   │  → risk weights    │
               └──────────┴──────────┴──────────┴──────────┴────────────────────┘
```

### Challenge 1 — City Layout Planning
> **Algorithm: Constraint Satisfaction Problem (CSP) + Recursive Backtracking**

Places hospitals, schools, industrial zones, power plants, ambulance depots, and residential areas on the grid — while enforcing 3 hard urban planning rules simultaneously:

| Rule | Constraint |
|------|-----------|
| A | Industrial zones cannot be adjacent to Schools or Hospitals |
| B | Every Residential area must be within **3 hops** of a Hospital |
| C | Every Power Plant must be within **2 hops** of an Industrial zone |

If no valid layout exists, the system **identifies which specific rule caused the conflict** and proposes a minimum-conflict fallback — it never crashes.

---

### Challenge 2 — Road Network Optimisation
> **Algorithm: Kruskal's Minimum Spanning Tree + Union-Find + Safety Augmentation**

Builds the **cheapest possible road network** that connects all 64 city nodes. Then adds a second independent route between the Hospital and Ambulance Depot — so if any single road floods, the ambulance can still reach the hospital.

```
Total edges built:  63  (for 64-node spanning tree)
Total road cost:    58.4 units
Residential roads:  0.8 cost  (cheaper through residential zones)
Standard roads:     1.0 cost
Blocked road:       ∞  (instantly removed from all pathfinding)
```

---

### Challenge 3 — Ambulance Placement  
> **Algorithm: Genetic Algorithm (Minimax Optimisation)**

With **C(64,3) = 39,711 possible placements** for 3 ambulances, exhaustive search is too slow — especially since this re-runs every 5 simulation steps as crime risk shifts.

The GA evolves a population of candidate placements over 80 generations:

```
Population:   40 individuals
Generations:  80
Elite:        Top 25% preserved each generation
Mutation:     25% — one random position swap
Crossover:    Half-splice from two elite parents
Fitness:      max(min_distance(citizen → nearest_ambulance))  ← minimised
```

**Pre-computation trick:** Dijkstra is run once from every node before the GA. All 3,200 fitness evaluations use O(1) lookups — **~150× faster** than re-running Dijkstra each time.

---

### Challenge 4 — Emergency Routing Under Changing Conditions
> **Algorithm: A\* Search with Admissible Heuristic + Real-Time Replanning**

A medical team travels to rescue trapped civilians in sequence. Roads flood during the mission. The moment a road becomes impassable, the router **detects the disruption and replans in the same simulation step** — not the next one.

```python
# Heuristic — admissible (never overestimates)
h(n, goal) = √((row_n - row_goal)² + (col_n - col_goal)²)

# Effective travel cost
cost(u → v) = edge.cost × max(node[u].risk_multiplier, node[v].risk_multiplier)
```

Admissible heuristic → **guaranteed optimal path every time**, not just any valid path.

**Replanning protocol:**
1. `road_blocked_event(u, v)` fires → adjacency list updated instantly
2. Current path checked for the blocked edge
3. If disrupted → A\* re-runs from team's **current position** to same goal
4. New optimal path live in same step

---

### Challenge 5 — Crime Risk Prediction
> **Algorithm: K-Means Clustering (unsupervised) → Decision Tree Classification (supervised)**

Two completely different types of machine learning, used in sequence:

**Stage 1 — K-Means (no labels)**  
Groups all 64 nodes into 3 clusters based on `population_density` and `industrial_proximity`. Discovers natural neighbourhood categories without being told what "dangerous" means.

**Stage 2 — Decision Tree (labelled)**  
Trained on synthetic crime scores generated from 6 domain-justified factors:

| Factor | Contribution | Why |
|--------|-------------|-----|
| Population density | 0–1.0 | More people = more opportunity |
| Industrial proximity | 0–1.0 | Closer to industry = less surveillance |
| Industrial zone bonus | +0.4 | Irregular activity, economic stress |
| Residential bonus | +0.2 | Opportunistic crime target |
| High-pop cluster membership | +0.2 | Structural neighbourhood evidence |
| Gaussian noise N(0, 0.05) | ± random | Real-world variability |

**Integration:** Predictions write `risk_multiplier` (×1.0 / ×1.4 / ×1.8) to every node. Both A\* and the GA call `travel_cost()` which applies this automatically — **zero additional wiring**.

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/citymind.git
cd citymind

# Install (that's all you need)
pip install flask numpy scikit-learn

# Run
python3 run.py
```

Open **[http://localhost:5555](http://localhost:5555)** — the browser opens automatically.

> No Docker. No build step. No `.env` files. Just Python.

---

## 🎮 Controls

| Action | Control |
|--------|---------|
| Initialise city (run all 5 AIs) | `Initialise City` button |
| Step simulation | `Next Step` button or `Space` |
| Run all 20 steps automatically | `Run All Steps` button |
| Switch view overlay | `1` `2` `3` `4` keys |
| Inspect any node | Hover mouse over any circle |
| Reset | `Reset` button or `R` key |

### View Overlays

```
1 → 🗺  City Layout      — building types and icons
2 → 🛣  Road Network     — MST edges; blocked roads marked ✕
3 → 🚑  Ambulance Cover  — GA coverage zones (orange radial glow)
4 → 🔴  Crime Heatmap    — risk levels (red / yellow / green per cell)
```

---

## 🔍 Hover Tooltip

Every node shows:

```
Type:             🏘️ Residential
Node ID:          37
Population:       142.5
Crime Risk:       Medium  
Risk Multiplier:  ×1.4    ← affects travel cost for A* and GA
Accessible:       ✅
```

---

## 📋 Event Log Colours

```
✅  green  → success      (path found, civilian rescued, algorithm done)
🚧  yellow → warning      (road blocked by flood)
⚡  yellow → disruption   (path broken mid-mission → replanning)
❌  red    → error        (no path available, target completely isolated)
📍  blue   → info         (A* path computed, step number)
```

---

## 🏗️ Project Structure

```
citymind/
│
├── citymind.py          ← everything: 5 AI modules + Flask API
│   ├── CityGraph            shared graph — the single source of truth
│   ├── LayoutPlanner        Challenge 1: CSP backtracking
│   ├── RoadOptimizer        Challenge 2: Kruskal MST
│   ├── AmbulancePlacer      Challenge 3: Genetic Algorithm
│   ├── EmergencyRouter      Challenge 4: A* with replanning
│   ├── CrimePrediction      Challenge 5: K-Means + Decision Tree
│   └── Simulation           20-step controller + Flask endpoints
│
├── static/
│   └── index.html       ← full UI — Canvas, 4 overlays, log, panels
│
├── run.py               ← launcher (auto-opens browser)
├── README.md
└── assets/              ← screenshots for this README
```

---

## 📡 REST API

```http
POST  /api/init         Run all 5 challenges, reset simulation
GET   /api/state        Full system state as JSON
POST  /api/step         Advance simulation one step
POST  /api/run_all      Complete all 20 steps
POST  /api/block_road   Manually block a road {"u": 7, "v": 15}
```

**Example:**

```bash
curl -X POST http://localhost:5555/api/init
curl -X POST http://localhost:5555/api/step
curl -X POST http://localhost:5555/api/block_road \
     -H "Content-Type: application/json" \
     -d '{"u": 12, "v": 20}'
```

---

## ⚙️ Configuration

All tunable parameters live at the top of `citymind.py`:

```python
GRID_SIZE      = 8     # city size (n×n)
FLOOD_PROB     = 0.20  # road flood probability per step
MAX_STEPS      = 20    # simulation length

# Ambulance GA
N_AMBULANCES   = 3
POP_SIZE       = 40
GENERATIONS    = 80
MUTATION_RATE  = 0.25

# Crime risk travel multipliers
MULTIPLIERS = {"Low": 1.0, "Medium": 1.4, "High": 1.8}

# Required building counts
REQUIRED = {
    "Hospital": 2, "School": 2, "Industrial": 3,
    "PowerPlant": 1, "AmbulanceDepot": 2, "Residential": 8,
}
```

---

## 📊 Performance

| Module | Typical Runtime |
|--------|----------------|
| CSP layout planner | 0.1 – 2s |
| Kruskal MST | < 10ms |
| Genetic Algorithm | 1 – 3s |
| A\* per query | < 1ms |
| Crime prediction pipeline | ~100ms |
| **Full initialisation** | **2 – 5s** |
| Per simulation step | < 100ms |

---

## 💡 Design Decisions

| Decision | Choice Made | Why Not the Alternative |
|----------|-------------|------------------------|
| Graph library | Custom `CityGraph` class | NetworkX would need a parallel copy → sync bugs |
| CSP solver | Backtracking | Only complete solver; diagnoses exact failing rule |
| Placement search | Genetic Algorithm | 39,711 search space; re-optimises cheaply every 5 steps |
| Pathfinding | A\* not BFS | BFS ignores edge weights; wrong for cost-weighted graph |
| Classifier | Decision Tree not Random Forest | Interpretable rules; no overfitting on 64 examples |
| Frontend | Vanilla HTML/JS | Zero build step; zero dependency failures during demo |
| Target order | Sequential not TSP | TSP is NP-hard; breaks real-time replanning |

---

## 🧪 Test Individual Modules

```python
from citymind import CityGraph, LayoutPlanner, RoadOptimizer, CrimePrediction

# Test CSP alone
graph   = CityGraph(size=8)
planner = LayoutPlanner(graph)
print("Layout valid:", planner.plan())
print("Conflict:", planner.conflict_rule)

# Test MST alone
road = RoadOptimizer(graph)
road.optimize()
print("Edges:", len(graph.edges))
print("Blocked:", sum(1 for e in graph.edges.values() if e["blocked"]))

# Test crime ML alone
crime = CrimePrediction(graph)
crime.run()
risks = [n["crime_risk"] for n in graph.nodes.values()]
print("High:", risks.count("High"), "Medium:", risks.count("Medium"), "Low:", risks.count("Low"))
```

---

## 🛠️ Tech Stack

```
Language    →  Python 3.12
Web server  →  Flask 3.0  (REST API, static serving)
ML          →  scikit-learn  (K-Means, Decision Tree)
Math        →  NumPy  (feature matrices for clustering)
Frontend    →  HTML5 Canvas + Vanilla JS + CSS3
Fonts       →  Orbitron (headings) · Space Mono (data)
Theme       →  Cyberpunk dark  (operations-centre aesthetic)
Algorithms  →  All custom — no graph/AI algorithm libraries
```

---

## 📜 License

```
MIT — use it, fork it, build on it. Just keep the credit.
```

---

<div align="center">

<br/>

**Built every algorithm from scratch — A\*, Kruskal's, Genetic Evolution,**  
**Constraint Backtracking, K-Means, Decision Tree — in pure Python.**

<br/>

*If this helped you understand AI algorithms, drop a* ⭐

<br/>

<!-- 📸 OPTIONAL: add a footer image here -->
<!-- <img src="assets/footer.png" width="100%"/> -->

</div>
