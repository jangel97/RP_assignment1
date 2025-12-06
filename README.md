# **Route Search for Package Delivery**

## **Overview**

This project compares search algorithms by routing an autonomous delivery vehicle through a grid-based map containing obstacles and package locations. 
It provides an experimental environment to observe and analyze the performance of BFS, DFS, UCS/Dijkstra, and A*.

## **Project Structure**

```
prac1-graphs/
├── scripts/
│   ├── common.py              # Shared code (GameWalkPuzzle, utilities)
│   ├── animated_viewer.py     # Uses AnimatedSearchViewer for visualization
│   ├── base_viewer.py         # Uses BaseViewer with metrics table
│   └── web_viewer.py          # Uses WebViewer for web-based visualization
└── utils/
    ├── animated_viewer.py     # AnimatedSearchViewer implementation
    └── random_map.py          # Random map generation utility
```

### **Common Module** (`scripts/common.py`)

The `common.py` module eliminates code duplication across viewer scripts by providing:
- **GameWalkPuzzle**: SearchProblem implementation with:
  - Movement actions (up, down, left, right)
  - Three heuristic functions for A*
  - Cost calculation for different movement types
- **searchInfo()**: Extracts solution statistics (length, cost, expanded nodes)
- **resultado_experimento()**: Displays the solution path on the map
- **run_case()**: Runs predefined test cases (1, 2, or 3)
- **get_map()**: Generates random or default maps

### **Viewer Scripts**

Each script uses the common module but provides different visualization:

#### **animated_viewer.py**
- Visualizes search process with animated GUI
- Shows step-by-step node expansion
- Best for understanding algorithm behavior

#### **base_viewer.py**
- Minimal visualization with comprehensive metrics
- Generates comparison table with:
  - Solution length and cost
  - Expanded nodes
  - Max frontier size
  - Optimality analysis
- Best for benchmarking and analysis

#### **web_viewer.py**
- Web-based visualization interface
- Accessible via browser
- Best for remote or web-based demos

## **Usage**

Each script can be run independently:

```bash
# Run with animated viewer
python scripts/animated_viewer.py

# Run with base viewer and metrics
python scripts/base_viewer.py

# Run with web viewer
python scripts/web_viewer.py
```

### **Test Cases**

Three predefined cases are available in each script:

**Case 1**: Uniform costs (all moves cost 1)
- Algorithms: BFS, DFS

**Case 2**: Non-uniform costs (left=3, right=1, up=1, down=3)
- Algorithms: BFS, Uniform Cost, A*

**Case 3**: A* with different heuristics
- Tests heuristic1 (Manhattan), heuristic2 (Chebyshev), heuristic3 (2×Manhattan)

Edit the last line of each script to change the case:
```python
run_case(1, MAP_ASCII, main)  # Change 1 to 2 or 3
```

### **Map Configuration**

Control map generation by setting `RANDOM_MAP` in each script:
```python
RANDOM_MAP = True   # Use randomly generated map
RANDOM_MAP = False  # Use default predefined map
```

## **Dependencies**

Run:
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r scripts/requirements.txt
```

## **Algorithms Compared**

- **Breadth-First Search (BFS)**: Complete, optimal for uniform costs
- **Depth-First Search (DFS)**: Not optimal, low memory usage
- **Uniform Cost Search**: Optimal for any cost function
- **A***: Optimal with admissible heuristics, most efficient
