import pygame
import sys
import os
import random


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, f"resources/{relative_path}")


pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
FPS = 60

pygame.display.set_caption("Battle Kingdom")


pygame.mixer.init()
pygame.mixer.music.load(
    resource_path("music/Waterflame & Rutra - Pixel War.mp3"))
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

font = pygame.font.SysFont(resource_path("fonts/harreegh_popped.ttf"), 30)

BLACK = (0, 0, 0)

map = pygame.image.load(resource_path("sprites/map/grass.jpg"))
background = pygame.transform.scale(map, (width, height))

TILE_SIZE = 40

game_map = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B         BB       B",
    "B   BBBB     BBBB  B",
    "B               B  B",
    "B               B  B",
    "B   BB    BB   BB  B",
    "B               B  B",
    "B  BBBB   BB       B",
    "B   B      BBBBBB  B",
    "B   B      B       B",
    "B   B      B       B",
    "B   BBBBB  BBBBBBBBB",
    "B                  B",
    "BBBBB       B      B",
    "BBBBBBBBBBBBBBBBBBBB",
]

player_sprites = {
    "up": pygame.transform.scale(
        pygame.image.load(
            resource_path("sprites/player/back.png")),
        (TILE_SIZE, TILE_SIZE)
    ),
    "down": pygame.transform.scale(
        pygame.image.load(
            resource_path("sprites/player/front.png")),
        (TILE_SIZE, TILE_SIZE)
    ),
    "left": pygame.transform.scale(
        pygame.image.load(
            resource_path("sprites/player/side_left.png")),
        (TILE_SIZE, TILE_SIZE)
        ),
    "right": pygame.transform.scale(
        pygame.image.load(
            resource_path("sprites/player/side_right.png")),
        (TILE_SIZE, TILE_SIZE)
    ),
}

player_rect = player_sprites["down"].get_rect()
player_rect.topleft = (120, 120)
player_speed = 4
player_direction = "down"

# Загрузка спрайта кирпичной стены
brick = pygame.image.load(resource_path("sprites/map/wall.png"))
brick_img = pygame.transform.scale(brick, (TILE_SIZE, TILE_SIZE))

walls = []

enemy_size = TILE_SIZE
enemy_color = (255, 0, 0)  # Красный
enemy_speed = 2
enemy_rect = pygame.Rect(200, 200, enemy_size, enemy_size)
enemy_direction = random.choice(["up", "down", "left", "right"])

for y, row in enumerate(game_map):
    for x, cell in enumerate(row):
        if cell == 'B':
            wall_rect = pygame.Rect(
                x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            walls.append(wall_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    dx, dy = 0, 0
    old_position = player_rect.topleft

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_rect.x -= player_speed
        player_direction = "left"
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_rect.x += player_speed
        player_direction = "right"
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        player_rect.y -= player_speed
        player_direction = "up"
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_rect.y += player_speed
        player_direction = "down"

    player_rect.x += dx
    for wall in walls:
        if player_rect.colliderect(wall):
            player_rect.x = old_position[0]
            break

    player_rect.y += dy
    for wall in walls:
        if player_rect.colliderect(wall):
            player_rect.y = old_position[1]
            break

    screen.blit(background, (0, 0))
    screen.blit(player_sprites[player_direction], player_rect.topleft)

    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == 'B':
                screen.blit(brick_img, (x * TILE_SIZE, y * TILE_SIZE))

    pygame.display.flip()

    clock.tick(FPS)
