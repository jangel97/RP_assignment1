import random
from collections import deque

def bfs_path_exists(grid, start, goal):
    h, w = len(grid), len(grid[0])
    sx, sy = start
    gx, gy = goal
    q = deque([(sx, sy)])
    visited = {(sx, sy)}

    while q:
        x, y = q.popleft()
        if (x, y) == (gx, gy):
            return True

        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < w and 0 <= ny < h and
                grid[ny][nx] != '#' and (nx, ny) not in visited):
                visited.add((nx, ny))
                q.append((nx, ny))
    return False

def generate_random_map(width=9, height=7, wall_prob=0.2, max_tries=100):
    for _ in range(max_tries):
        # start with empty grid
        grid = [[' ' for _ in range(width)] for _ in range(height)]

        # borders as walls
        for x in range(width):
            grid[0][x] = '#'
            grid[height - 1][x] = '#'
        for y in range(height):
            grid[y][0] = '#'
            grid[y][width - 1] = '#'

        # random internal walls
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if random.random() < wall_prob:
                    grid[y][x] = '#'

        # pick P and T on free cells
        free_cells = [
            (x, y)
            for y in range(1, height - 1)
            for x in range(1, width - 1)
            if grid[y][x] == ' '
        ]
        if len(free_cells) < 2:
            continue  # too many walls, try again

        px, py = random.choice(free_cells)
        free_cells.remove((px, py))
        tx, ty = random.choice(free_cells)

        # check connectivity
        if not bfs_path_exists(grid, (px, py), (tx, ty)):
            continue

        # place P and T
        grid[py][px] = 'P'
        grid[ty][tx] = 'T'

        # convert to ASCII string
        lines = ["".join(row) for row in grid]
        return "\n".join(lines)

    raise RuntimeError("Couldn't generate a valid map after many tries")


if __name__ == "__main__":
    print(generate_random_map())
