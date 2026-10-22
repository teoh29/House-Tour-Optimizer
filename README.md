# CSC3206 Assignment 2 — House Tour Optimizer (A* Search)

## Group Name: Claude Suggest AI Names

## Members:

- Choo Yen Ching
- Colin Leong Hong Seng
- Damien Yee Jin Yang
- Teoh En Yi
- Sian Yi Xuan

## 1. Overview

This program models a house-visit tour that starts at Sunway University and visits every group member's residence exactly once, using **A\* Graph Search** guided by a nearest-unvisited-node heuristic. It also runs two baselines for comparison, which are **Uniform Cost Search (UCS)** (A\* with the heuristic switched off) and **exhaustive brute-force enumeration** of all possible routes to verify that A\* finds the true global optimum.

On completion, the program prints a formatted results dashboard to the terminal and saves a labelled route diagram as `route_map.png` in the same folder.

## 2. Requirements

- Python 3.9 or newer
- pip packages:
  - `matplotlib`
  - `networkx`

## 3. Installation

Open a terminal / command prompt in the folder containing the script and run:

```bash
pip install matplotlib networkx
```

(If `pip` is not recognised, try `python -m pip install matplotlib networkx`.)

## 4. How to Run

```bash
python ai_assignment2_code.py
```

(Use `python3` instead of `python` on macOS/Linux.)

## 5. What You Should See

1. **Terminal output** — a boxed dashboard containing:
   - Graph integrity verification (symmetry, completeness, non-negative weights) and any triangle-inequality warnings found in the data
   - UCS and brute-force baseline stats (states expanded / permutations checked, execution time)
   - A\* results: optimal route cost, estimated drive time, fuel used, CO2 emitted, states expanded, and execution time
   - A step-by-step table of the optimal route showing each leg, the group member at that stop, and the running distance total
   - The final optimal traversal sequence

2. **A generated image file**, `route_map.png`, saved to the same directory the script is run from. It shows all locations as a network graph, with the optimal A\* route highlighted and each route edge labelled with its distance in km.

### Sample Output
 
Actual output from a verified run of the script. Route, cost, and states-expanded figures are deterministic and will be identical on any machine; execution-time figures (ms) will vary slightly depending on your hardware.

```
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                               CSC3206 AI ASSIGNMENT 2 — HOUSE TOUR OPTIMIZER                                               
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
  [ SYSTEM VERIFICATION & BASELINES ]
  • Graph Integrity : PASSED (Symmetry & Completeness Verified)
  • Metric Warning  : 1 Triangle Inequality violations detected (Minor urban routing detours exist):
                      ➔ Puchong Perdana to Taman Putra Prima (7.00 km) > via Taman Puchong Utama (6.80 km)
  • UCS Baseline    : 44 states expanded | Exec Time: 0.329 ms
  • Brute-Force     : 120 permutations   | Exec Time: 0.129 ms
  • Worst-Case Route: 53.20 km
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  [ A* OPTIMIZATION RESULTS ]
  • Search Strategy : A* Graph Search (Nearest-Node Heuristic)
  • Total Cost      : 20.25 km
  • Est. Drive Time : 40.50 min
  • Fuel Estimated  : 1.62 L
  • CO2 Emissions   : 3.74 kg
  • States Expanded : 21 states (Expanded 23 fewer states than UCS)
  • Execution Time  : 0.237 ms (Median over 1,000 runs)
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Step   | Location                    | Group Member         | Leg        | Total     
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  [0]    | Sunway University           | Tour Origin Point    | 0.00 km    | 0.00 km   
  [1]    | Nadayu28 Residences         | Teoh En Yi           | +0.75 km   | 0.75 km   
  [2]    | Bandar Puteri Puchong       | Colin Leong          | +9.30 km   | 10.05 km  
  [3]    | Puchong Perdana             | Sian Yi Xuan         | +3.40 km   | 13.45 km  
  [4]    | Taman Puchong Utama         | Damien Yee           | +2.10 km   | 15.55 km  
  [5]    | Taman Putra Prima           | Choo Yen Ching       | +4.70 km   | 20.25 km  
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  OPTIMAL TRAVERSAL SEQUENCE:
  Sunway University ➔ Nadayu28 Residences ➔ Bandar Puteri Puchong ➔ Puchong Perdana ➔ Taman Puchong Utama ➔ Taman Putra Prima
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
```

## 6. Notes

- The script automatically detects headless/automated environments (no display attached) and switches Matplotlib to a non-interactive backend, so it will run without errors on a grading server as well as a normal desktop.
- The script includes an internal correctness check: it raises an error if the A\* route cost does not exactly match the brute-force optimal cost, so a normal run completing without errors is itself confirmation that A\* found the correct optimal route.
- If `route_map.png` already exists in the folder, it will be overwritten each time the script is run.

## 7. Troubleshooting

| Issue | Likely Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'matplotlib'` (or `networkx`) | Packages not installed | Run `pip install matplotlib networkx` |
| No `route_map.png` produced | Script did not reach the end (check terminal for an error message) | Re-run and read the printed error; ensure write permission in the folder |