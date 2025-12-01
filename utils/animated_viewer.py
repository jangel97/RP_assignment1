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

    def __init__(self, map_grid, delay_ms=200):
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

        # Find initial and goal positions
        for y in range(len(self.map_grid)):
            for x in range(len(self.map_grid[y])):
                if self.map_grid[y][x].lower() == "t":
                    self.initial_pos = (x, y)
                elif self.map_grid[y][x].lower() == "p":
                    self.goal_pos = (x, y)

        # Initialize pygame
        pygame.init()
        width = len(self.map_grid[0]) * TILE_SIZE
        # Add extra space for info panel
        height = len(self.map_grid) * TILE_SIZE + 100
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
        info_rect = pygame.Rect(0, self.map_height, self.screen.get_width(), 100)
        pygame.draw.rect(self.screen, (40, 40, 40), info_rect)

        # Display current position
        if self.current_pos:
            pos_text = self.font_large.render(f"Exploring: {self.current_pos}", True, (255, 255, 100))
            self.screen.blit(pos_text, (10, self.map_height + 10))

        # Use built-in stats from BaseViewer
        iterations = self.stats.get('iterations', 0)
        visited_count = max(len(self.visited), self.stats.get('visited', 0))

        # Display timer
        timer_text = self.font.render(f"Time: {self.elapsed_time:.2f}s", True, (255, 200, 100))
        self.screen.blit(timer_text, (250, self.map_height + 10))

        # Display iterations
        iter_text = self.font.render(f"Iterations: {iterations}", True, (180, 220, 255))
        self.screen.blit(iter_text, (10, self.map_height + 45))

        # Display visited count
        visited_text = self.font.render(f"Visited: {visited_count}", True, (180, 220, 255))
        self.screen.blit(visited_text, (10, self.map_height + 70))

        # Display goal position
        if self.goal_pos:
            goal_text = self.font.render(f"Goal: {self.goal_pos}", True, (100, 255, 150))
            self.screen.blit(goal_text, (250, self.map_height + 45))

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
                print(f"  -> Exploring state: {state}")
                self.update_display()

    def set_path(self, path):
        """Show the final path"""
        self.path = path
        self.update_display()
        # Keep window open longer to see the final result
        pygame.time.delay(2000)

    def close(self):
        """Close the pygame window"""
        print("Press any key to close the visualization window...")
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    waiting = False
        pygame.quit()