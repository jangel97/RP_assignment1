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

## **WebViewer Visualization**

The project includes the ability to visualize the search tree using **WebViewer**, which displays expanded nodes, frontier evolution, and path structure in a local browser window.

To enable it, replace the viewer argument in the script:

```python
used_viewer = WebViewer()
```

### **Run the script locally**

```bash
python3 scripts/Cuaderno_actividad_1_Búsqueda_v3.py
```

### **Requirements**

Install dependencies from:

```
python3 scripts/requirements.txt
```

WebViewer requires local execution and will not work in Google Colab.

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

