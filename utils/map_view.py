import pygame
import sys

CAPTION="MAPA"
MAP_ASCII = """
#########
# P     #
# # ##  #
#    #  #
# ##T   #
#       #
#########
"""

TILE_SIZE = 50

COLORS = {
    "#": (50, 50, 50),       # Wall
    " ": (230, 230, 230),    # Empty
}

SPRITES = {
    "T": "utils/assets/agent.png",
    "P": "utils/assets/treasure.png",
}

def parse_map(map_ascii):
    return [list(line) for line in map_ascii.strip().split("\n")]

def draw_map(screen, grid, sprites):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, COLORS.get(cell, (240,240,240)), rect)
            pygame.draw.rect(screen, (180,180,180), rect, 1)

            if cell in sprites:
                icon = sprites[cell]
                screen.blit(icon, icon.get_rect(center=rect.center))

def main():
    pygame.init()
    grid = parse_map(MAP_ASCII)
    screen = pygame.display.set_mode((len(grid[0]) * TILE_SIZE, len(grid) * TILE_SIZE))
    pygame.display.set_caption(CAPTION)

    # Load sprites
    sprites = {
        key: pygame.transform.scale(pygame.image.load(path), (TILE_SIZE-8, TILE_SIZE-8))
        for key, path in SPRITES.items()
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                pygame.image.save(screen, "map_view.png")
                print("Saved map_view.png")

        draw_map(screen, grid, sprites)
        pygame.display.flip()

if __name__ == "__main__":
    main()
