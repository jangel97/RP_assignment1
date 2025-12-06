# -*- coding: utf-8 -*-
"""Common code shared across search experiment scripts"""

from __future__ import print_function

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simpleai.search import SearchProblem, astar, breadth_first, depth_first, uniform_cost
from utils.random_map import generate_random_map


# -------------------------------------------------------------------------
# PROBLEM DEFINITION
# -------------------------------------------------------------------------

class GameWalkPuzzle(SearchProblem):

    def __init__(self, board, costs, heuristic_number):
        self.board = board
        self.costs = costs
        self.heuristic_number = heuristic_number
        self.goal = (0, 0)

        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x].lower() == "t":
                    self.initial = (x, y)
                elif board[y][x].lower() == "p":
                    self.goal = (x, y)

        super().__init__(initial_state=self.initial)

    def actions(self, state):
        actions = []
        for action in self.costs.keys():
            nx, ny = self.result(state, action)
            if self.board[ny][nx] != "#":
                actions.append(action)
        return actions

    def result(self, state, action):
        x, y = state
        if "up" in action: y -= 1
        if "down" in action: y += 1
        if "left" in action: x -= 1
        if "right" in action: x += 1
        return (x, y)

    def is_goal(self, state):
        return state == self.goal

    def cost(self, state, action, state2):
        return self.costs[action]

    # Heuristics
    def heuristic1(self, s):
        return abs(s[0] - self.goal[0]) + abs(s[1] - self.goal[1])

    def heuristic2(self, s):
        return max(abs(s[0] - self.goal[0]), abs(s[1] - self.goal[1]))

    def heuristic3(self, s):
        return 2 * (abs(s[0] - self.goal[0]) + abs(s[1] - self.goal[1]))

    def heuristic(self, state):
        if self.heuristic_number == 1: return self.heuristic1(state)
        if self.heuristic_number == 2: return self.heuristic2(state)
        if self.heuristic_number == 3: return self.heuristic3(state)
        raise Exception("Heurística inválida")


# -------------------------------------------------------------------------
# EXPERIMENT OUTPUT
# -------------------------------------------------------------------------

def searchInfo(problem, result, viewer):
    def total_cost():
        cost = 0
        prev = problem.initial_state
        for action, st in result.path():
            if action:
                cost += problem.cost(prev, action, st)
                prev = st
        return cost

    res = f"Total length of solution: {len(result.path())}\n"
    res += f"Total cost of solution: {total_cost()}\n"

    for stat, val in viewer.stats.items():
        res += f"{stat.replace('_',' ')}: {val}\n"

    return res


def resultado_experimento(problem, MAP, result, viewer):
    path = [pos for (_, pos) in result.path()]

    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if (x, y) == problem.initial:
                print("T", end='')
            elif (x, y) == problem.goal:
                print("P", end='')
            elif (x, y) in path:
                print("·", end='')
            else:
                print(MAP[y][x], end='')
        print()

    print(searchInfo(problem, result, viewer))


# -------------------------------------------------------------------------
# MAP DEFINITIONS
# -------------------------------------------------------------------------

DEFAULT_MAP_ASCII = """
#########
# P     #
# # ##  #
#    #  #
# ##T   #
#       #
#########
"""


def get_map(use_random=True, width=10, height=10, wall_prob=0.45):
    """Generate or return default map"""
    return generate_random_map(width=width, height=height, wall_prob=wall_prob) if use_random else DEFAULT_MAP_ASCII


# -------------------------------------------------------------------------
# CASE RUNNER
# -------------------------------------------------------------------------

def run_case(case_number, MAP_ASCII, main_function):
    """
    Run a specific test case

    Args:
        case_number: 1, 2, or 3
        MAP_ASCII: The map string to use
        main_function: The main function to call (viewer-specific)
    """
    if case_number == 1:
        print("\n================ CASE 1 ================\n")
        COSTS = {
                    "left":1, 
                    "right":1, 
                    "up":1, 
                    "down":1,
                 }
        algorithms = (breadth_first, depth_first)
        main_function(MAP_ASCII, COSTS, algorithms)

    elif case_number == 2:
        print("\n================ CASE 2 ================\n")
        COSTS = {"left":3, "right":1, "up":1, "down":3}
        algorithms = (breadth_first, uniform_cost, astar)
        main_function(MAP_ASCII, COSTS, algorithms)

    elif case_number == 3:
        print("\n================ CASE 3 ================\n")
        COSTS = {"left":3, "right":1, "up":1, "down":3}
        algorithms = (astar,)
        for h in (1,2,3):
            print(f"\n---- A* con Heurística {h} ----\n")
            main_function(MAP_ASCII, COSTS, algorithms, heuristic_number=h)

    else:
        raise ValueError("case_number debe ser 1, 2 o 3.")
