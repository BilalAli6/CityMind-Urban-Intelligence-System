# 🏙️ CityMind — Urban Intelligence System

A full implementation of the BS Cyber Security Group Project.

## Quick Start

```bash
pip install flask numpy scikit-learn
python3 run.py
# Open http://localhost:5555
```

## What's Implemented

| Challenge | Algorithm | Status |
|-----------|-----------|--------|
| 1. City Layout Planning | CSP Backtracking | ✅ |
| 2. Road Network Optimization | Kruskal's MST + Dual-path | ✅ |
| 3. Ambulance Placement | Genetic Algorithm | ✅ |
| 4. Emergency Routing | A* with Real-time Replanning | ✅ |
| 5. Crime Risk Prediction | K-Means + Decision Tree | ✅ |

## UI Features
- 4 overlay views: City Layout, Road Network, Ambulance Coverage, Crime Heatmap
- Real-time event log
- A* path visualisation
- Router state panel
- Crime risk panel
- Keyboard shortcuts: Space=step, 1-4=views, R=reset
- Hover tooltips on every node

## Architecture
- Single `CityGraph` shared across all modules
- Flask REST API backend
- Pure HTML/CSS/JS frontend (no framework)
- 20-step simulation with random flooding events
