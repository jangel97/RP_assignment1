# -*- coding: utf-8 -*-
"""Cuaderno_Actividad_1_Búsqueda_v3.ipynb - Web Viewer Version"""

#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simpleai.search.viewers import WebViewer
from common import GameWalkPuzzle, resultado_experimento, get_map, run_case

# SETTINGS
RANDOM_MAP = False

# -------------------------------------------------------------------------
# MAIN (uses WebViewer)
# -------------------------------------------------------------------------

def main(MAP_ASCII, COSTS, algorithms, heuristic_number=1):
    MAP = [list(row) for row in MAP_ASCII.split("\n") if row]

    for algorithm in algorithms:
        problem = GameWalkPuzzle(MAP, COSTS, heuristic_number)

        viewer = WebViewer()

        print(f"\nExperimento con algoritmo {algorithm.__name__}:")

        result = algorithm(problem, graph_search=True, viewer=viewer)

        resultado_experimento(problem, MAP, result, viewer)

        viewer.close()


# -------------------------------------------------------------------------
# RUN
# -------------------------------------------------------------------------

if __name__ == "__main__":
    MAP_ASCII = get_map(use_random=RANDOM_MAP)
    run_case(2, MAP_ASCII, main)

