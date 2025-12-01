# **Route Search for Package Delivery**

## **Overview**

This project compares search algorithms by routing an autonomous delivery vehicle through a grid-based map containing obstacles and package locations. It provides an experimental environment to observe and analyze the performance of BFS, DFS, UCS/Dijkstra, and A*.

---

## **Objectives**

* Compare uninformed vs informed search strategies.
* Analyze **optimality**, **completeness**, **time/memory efficiency**, and **heuristic admissibility**.
* Test A* with different heuristics (e.g., Manhattan distance).
* Generate conclusions from both theoretical reasoning and practical results.

---

## **Problem Description**

* Environment represented as a **grid** with movement allowed **up, down, left, right**.
* Includes **start position**, **goal cells**, **walls**, and **empty cells**.
* Experiments may include **variable movement costs**.
* A* uses **Manhattan distance** as the default heuristic.

---

## **Algorithms**

| Algorithm      | Type       | Optimal             | Complete | Heuristic |
| -------------- | ---------- | ------------------- | -------- | --------- |
| BFS            | Uninformed | Yes (uniform cost)  | Yes      | No        |
| DFS            | Uninformed | No                  | No       | No        |
| UCS / Dijkstra | Uninformed | Yes                 | Yes      | No        |
| A*             | Informed   | Yes (if admissible) | Yes      | Yes       |

---

## **Experiment Cases**

### **Case 1 — BFS vs DFS**

Compare optimality and number of expanded nodes.

### **Case 2 — BFS, UCS, and A* with costs**

Analyze performance impact of weighted actions.

### **Case 3 — A* with multiple heuristics**

Evaluate influence on efficiency compared to UCS.

---

## **Visualization Options**

### **Animated Pygame Visualization (Default)**

The project includes a real-time animated visualization using **pygame** that shows the robot moving through the map as the search algorithm explores nodes. This visualization provides an intuitive way to understand how different search algorithms work.

#### **Features**

- **Real-time visualization**: Watch the robot explore the map step by step
- **Color-coded cells**:
  - **Dark gray**: Walls (#)
  - **Light blue**: Visited/explored cells
  - **Yellow**: Current position being explored
  - **Green**: Final solution path (shown after completion)
- **Live statistics panel** showing:
  - **Exploring**: Current position coordinates (x, y)
  - **Time**: Elapsed search time in seconds
  - **Nodos expandidos**: Number of expanded nodes (iterations)
  - **Nodos visitados**: Number of visited nodes
  - **Tamaño máximo de lista**: Maximum frontier/fringe size
  - **Longitud solución**: Solution path length (after completion)
  - **Coste solución**: Total solution cost (after completion)
  - **Objetivo**: Goal position coordinates

#### **How to Use**

By default, the animated visualization is **enabled**. Simply run:

```bash
python3 scripts/Cuaderno_actividad_1_Búsqueda_v3.py
```

The visualization will:
1. Show each step of the algorithm with a 300ms delay
2. Display the final solution path in green
3. Wait for you to press **ESC** to close the window

#### **Customization**

You can adjust the animation speed by changing the `delay_ms` parameter in the script:

```python
used_viewer = AnimatedSearchViewer(MAP, delay_ms=300, problem=problem)
```

Lower values = faster animation, higher values = slower animation.

To **disable** the animation and use console output only:

```python
main(MAP_ASCII, COSTS, algorithms, use_animation=False)
```

---

### **WebViewer Visualization**

The project also supports **WebViewer**, which displays the search tree structure, expanded nodes, and frontier evolution in a local browser window.

To enable it, set `use_animation=False` and modify the viewer in the script:

```python
used_viewer = WebViewer()
```

WebViewer requires local execution and will not work in Google Colab.

---

## **Requirements**

Install all dependencies:

```bash
pip install -r utils/requirements.txt
```

Required packages:
- `simpleai` - Search algorithms
- `pygame` - Animated visualization
- `flask` - WebViewer (optional)

---

## **How to Run Experiments**

1. Open the script or notebook.
2. Select Case 1, 2, or 3.
3. Choose one or multiple algorithms.
4. Record:

   * Path found
   * Cost
   * Nodes expanded
   * Execution time

---

## **Output Example**

| Algorithm | Nodes | Cost | Time | Optimal |
| --------- | ----- | ---- | ---- | ------- |
| BFS       | …     | …    | … ms | Yes     |
| DFS       | …     | …    | … ms | No      |
| UCS       | …     | …    | … ms | Yes     |
| A*        | …     | …    | … ms | Yes     |

