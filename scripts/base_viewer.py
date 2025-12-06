# -*- coding: utf-8 -*-
"""Cuaderno_Actividad_1_Búsqueda_v3.ipynb - Base Viewer Version with Metrics"""

#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simpleai.search.viewers import BaseViewer
from utils.animated_viewer import AnimatedSearchViewer
from common import GameWalkPuzzle, resultado_experimento, get_map, run_case

# SETTINGS
RANDOM_MAP = False


# -----------------------------------------------------------------------------------
# METRICS EXTRACTION (unique to this script)
# -----------------------------------------------------------------------------------

def extract_metrics(problem, result, viewer, algorithm_name):
    # Length
    length = len(result.path())

    # Cost
    cost_total = 0
    prev = problem.initial_state
    for action, state in result.path():
        if action:
            cost_total += problem.cost(prev, action, state)
            prev = state

    # Stats
    expanded = viewer.stats.get("expanded_nodes", "N/A")
    max_list = viewer.stats.get("max_frontier_size", "N/A")

    # Optimality
    if algorithm_name == "breadth_first":
        optimal = "Sí" if len(set(problem.costs.values())) == 1 else "No"
    elif algorithm_name == "uniform_cost":
        optimal = "Sí"
    elif algorithm_name == "astar":
        optimal = "Sí" if problem.heuristic_number in (1, 2) else "No"
    else:
        optimal = "No"

    return {
        "Algoritmo": algorithm_name.upper(),
        "Longitud": length,
        "Coste": cost_total,
        "Expandidos": expanded,
        "ListaMáx": max_list,
        "Óptimo": optimal
    }


# -----------------------------------------------------------------------------------
# MAIN FUNCTION (with metrics table)
# -----------------------------------------------------------------------------------

def main(MAP_ASCII, COSTS, algorithms, heuristic_number=1, use_animation=False):
    MAP = [list(x) for x in MAP_ASCII.split("\n") if x]

    all_metrics = []

    for algorithm in algorithms:
        problem = GameWalkPuzzle(MAP, COSTS, heuristic_number)

        viewer = AnimatedSearchViewer(MAP, delay_ms=300, problem=problem, caption=algorithm.__name__) \
                 if use_animation else BaseViewer()

        print(f"\nExperimento con algoritmo {algorithm.__name__}:")
        result = algorithm(problem, graph_search=True, viewer=viewer)

        resultado_experimento(problem, MAP, result, viewer)

        all_metrics.append(extract_metrics(problem, result, viewer, algorithm.__name__))

        if use_animation:
            viewer.close()

    # --- METRICS TABLE ---
    print("\nTabla de métricas:")
    print("Algoritmo | Long | Coste | Expandidos | ListaMáx | Óptimo")
    print("----------------------------------------------------------")
    for m in all_metrics:
        print(f"{m['Algoritmo']:9} | {m['Longitud']:4} | {m['Coste']:5} | "
              f"{m['Expandidos']:9} | {m['ListaMáx']:8} | {m['Óptimo']}")


# -----------------------------------------------------------------------------------
# RUN
# -----------------------------------------------------------------------------------

if __name__ == "__main__":
    MAP_ASCII = get_map(use_random=RANDOM_MAP)
    run_case(3, MAP_ASCII, main)
