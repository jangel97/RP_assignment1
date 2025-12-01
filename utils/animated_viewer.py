"""
Animated Pygame Viewer for Search Algorithms

This module provides real-time visualization of search algorithms (BFS, DFS, A*, etc.)
using pygame to show how the robot explores the map step by step.

## Architecture

The visualization uses an EVENT-DRIVEN architecture based on the observer pattern:

1. **Initialization**:
   - The map is stored ONCE in memory when the viewer is created
   - Initial and goal positions are identified
   - Pygame window is initialized

2. **During Search Execution**:
   - The search algorithm (from simpleai) calls `viewer.event()` at key moments
   - Events include: 'new_node', 'chosen_node', 'new_iteration', etc.
   - Each event contains only the NODE STATE (coordinates), NOT the entire map

3. **What Gets Sent Per Move**:
   - Only state coordinates (x, y) are passed with each event
   - The viewer maintains the original map and tracks visited positions
   - Very efficient - no redundant data transmission

4. **Rendering Process**:
   - On each event, the viewer updates its internal state (current_pos, visited set)
   - Redraws the ENTIRE map using the stored map + current state
   - Color-codes cells based on: visited, current, path, walls
   - Displays live statistics in the info panel

## Data Flow

simpleai algorithm → event(name, node) → viewer updates state → redraw map → pygame display

The map stays in memory, only position updates flow through the system.
"""

import pygame
import sys
import time
from simpleai.search.viewers import BaseViewer

TILE_SIZE = 50

COLORS = {
    "#": (50, 50, 50),           # Wall
    " ": (230, 230, 230),        # Empty
    "visited": (180, 220, 255),  # Visited cells
    "current": (255, 255, 100),  # Current position
    "path": (100, 255, 150),     # Final path
}

SPRITES = {
    "T": "utils/assets/agent.png",
    "P": "utils/assets/treasure.png",
}

class AnimatedSearchViewer(BaseViewer):
    """Pygame viewer that shows the robot moving through the map during search"""

    def __init__(self, map_grid, delay_ms=200, problem=None):
        super().__init__()
        self.map_grid = map_grid
        self.delay_ms = delay_ms
        self.visited = set()
        self.current_pos = None
        self.goal_pos = None
        self.initial_pos = None
        self.path = []
        self.nodes_explored = 0
        self.current_action = "Initializing"
        self.start_time = None
        self.elapsed_time = 0.0
        self.problem = problem
        self.solution_cost = 0.0
        self.current_cost = 0.0
        self.solution_actions = []  # List of actions in the solution path

        # Find initial and goal positions
        for y in range(len(self.map_grid)):
            for x in range(len(self.map_grid[y])):
                if self.map_grid[y][x].lower() == "t":
                    self.initial_pos = (x, y)
                elif self.map_grid[y][x].lower() == "p":
                    self.goal_pos = (x, y)
        time.sleep(2)
        # Initialize pygame
        pygame.init()
        width = len(self.map_grid[0]) * TILE_SIZE
        # Add extra space for info panel (expanded for more stats)
        height = len(self.map_grid) * TILE_SIZE + 180
        self.screen = pygame.display.set_mode((width, height))
        self.map_height = len(self.map_grid) * TILE_SIZE
        pygame.display.set_caption("BFS Search Visualization")

        # Load font for text display
        self.font = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)

        # Load sprites
        self.sprites = {}
        try:
            for key, path in SPRITES.items():
                img = pygame.image.load(path)
                self.sprites[key] = pygame.transform.scale(img, (TILE_SIZE-8, TILE_SIZE-8))
        except:
            print("Warning: Could not load sprites")

    def draw_info_panel(self):
        """Draw information panel below the map"""
        # Draw background for info panel
        info_rect = pygame.Rect(0, self.map_height, self.screen.get_width(), 180)
        pygame.draw.rect(self.screen, (40, 40, 40), info_rect)

        # Calculate solution length first (needed for display logic)
        solution_length = len(self.path) if self.path else 0

        # Display current position
        if self.current_pos:
            pos_text = self.font_large.render(f"Explorando: {self.current_pos}", True, (255, 255, 100))
            self.screen.blit(pos_text, (10, self.map_height + 10))

        # Display timer
        timer_text = self.font.render(f"Tiempo: {self.elapsed_time:.2f}s", True, (255, 200, 100))
        self.screen.blit(timer_text, (250, self.map_height + 15))

        # Display cost (right side, below timer)
        if solution_length > 0:
            # Final solution cost (green)
            cost_text = self.font.render(f"Coste: {self.solution_cost:.2f}", True, (100, 255, 150))
            self.screen.blit(cost_text, (250, self.map_height + 40))
        elif self.current_cost > 0:
            # Current exploration cost (orange)
            cost_text = self.font.render(f"Coste Actual: {self.current_cost:.2f}", True, (255, 200, 100))
            self.screen.blit(cost_text, (250, self.map_height + 40))

        # Use built-in stats from BaseViewer
        iterations = self.stats.get('iterations', 0)
        visited_count = max(len(self.visited), self.stats.get('visited', 0))
        max_fringe = self.stats.get('max_fringe_size', 0)

        # Left column stats
        y_offset = self.map_height + 50

        # Nodos expandidos
        expanded_text = self.font.render(f"Nodos expandidos: {iterations}", True, (180, 220, 255))
        self.screen.blit(expanded_text, (10, y_offset))

        # Visited
        visited_text = self.font.render(f"Nodos visitados: {visited_count}", True, (180, 220, 255))
        self.screen.blit(visited_text, (10, y_offset + 25))

        # Tamaño máximo de lista
        max_list_text = self.font.render(f"Tamaño máximo de lista: {max_fringe}", True, (180, 220, 255))
        self.screen.blit(max_list_text, (10, y_offset + 50))

        # Solution stats (shown when path is found)
        if solution_length > 0:
            length_text = self.font.render(f"Longitud solución: {solution_length}", True, (100, 255, 150))
            self.screen.blit(length_text, (10, y_offset + 75))

            # Display solution path (actions)
            if self.solution_actions:
                # Create a compact representation
                path_str = " > ".join(self.solution_actions)
                # Truncate if too long (max ~50 characters)
                if len(path_str) > 50:
                    path_str = path_str[:47] + "..."

                path_text = self.font.render(f"Camino: {path_str}", True, (100, 255, 150))
                self.screen.blit(path_text, (10, y_offset + 100))

        # Goal position (moved down)
        if self.goal_pos:
            goal_text = self.font.render(f"Objetivo: {self.goal_pos}", True, (200, 200, 200))
            self.screen.blit(goal_text, (250, y_offset + 50))

        # Initial position
        if self.initial_pos:
            init_text = self.font.render(f"Inicial: {self.initial_pos}", True, (200, 200, 200))
            self.screen.blit(init_text, (250, y_offset + 75))

    def draw_map(self):
        """Draw the current state of the map"""
        for y, row in enumerate(self.map_grid):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                # Determine cell color
                if (x, y) in self.path and (x, y) != self.initial_pos and (x, y) != self.goal_pos:
                    color = COLORS["path"]
                elif (x, y) == self.current_pos and (x, y) != self.initial_pos:
                    color = COLORS["current"]
                elif (x, y) in self.visited and (x, y) != self.initial_pos and (x, y) != self.goal_pos:
                    color = COLORS["visited"]
                else:
                    color = COLORS.get(cell, (240, 240, 240))

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (180, 180, 180), rect, 1)

                # Draw sprites for initial and goal positions
                if (x, y) == self.initial_pos and "T" in self.sprites:
                    self.screen.blit(self.sprites["T"], self.sprites["T"].get_rect(center=rect.center))
                elif (x, y) == self.goal_pos and "P" in self.sprites:
                    self.screen.blit(self.sprites["P"], self.sprites["P"].get_rect(center=rect.center))

                # Draw robot at current position
                if (x, y) == self.current_pos and (x, y) != self.initial_pos:
                    if "T" in self.sprites:
                        self.screen.blit(self.sprites["T"], self.sprites["T"].get_rect(center=rect.center))
                    else:
                        # Fallback: draw a circle
                        pygame.draw.circle(self.screen, (0, 100, 255), rect.center, TILE_SIZE // 3)

        # Draw info panel
        self.draw_info_panel()

    def update_display(self):
        """Update the pygame display and handle events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.draw_map()
        pygame.display.flip()
        pygame.time.delay(self.delay_ms)

    def event(self, name, *params):
        """Called by the search algorithm on various events"""
        # Start timer on first event
        if self.start_time is None:
            self.start_time = time.time()

        # Call parent class event handler first to track stats
        super().event(name, *params)

        # Update elapsed time
        if self.start_time:
            self.elapsed_time = time.time() - self.start_time

        # Debug: print all events and current stats
        print(f"Event: {name}, Stats: {self.stats}")

        # Track all explored nodes
        if params and hasattr(params[0], 'state'):
            node = params[0]
            state = node.state
            self.visited.add(state)

            if name == 'new_node' or name == 'chosen_node':
                # Update current position for any node being processed
                self.current_pos = state

                # Update current cost if available
                if hasattr(node, 'cost'):
                    self.current_cost = node.cost

                print(f"  -> Exploring state: {state}, Cost: {self.current_cost:.2f}")
                self.update_display()

    def set_path(self, path, result=None):
        """Show the final path and calculate cost"""
        self.path = path

        # Calculate solution cost and extract actions if problem is available
        if self.problem and result:
            origin_state = self.problem.initial_state
            total_cost = 0.0
            self.solution_actions = []

            for action, ending_state in result.path():
                if action is not None:
                    total_cost += self.problem.cost(origin_state, action, ending_state)
                    self.solution_actions.append(action)
                    origin_state = ending_state

            self.solution_cost = total_cost
            print(f"Solution path calculated: Length={len(path)}, Cost={self.solution_cost:.2f}")
            print(f"Actions list: {self.solution_actions}")
            print(f"Actions joined: {' → '.join(self.solution_actions)}")
        else:
            print(f"Warning: Cannot calculate cost - problem={self.problem}, result={result}")

        self.update_display()
        # Keep window open longer to see the final result
        pygame.time.delay(2000)

    def close(self):
        """Close the pygame window"""
        print("Press ESC to close the visualization window...")
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
        pygame.quit()