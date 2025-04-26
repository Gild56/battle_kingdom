import pygame
import sys
import os
import random
import math


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

hit_sound = pygame.mixer.Sound(resource_path("music/sword_sound.mp3"))
enemy_hit_sound = pygame.mixer.Sound(resource_path("music/sword_sound.mp3"))

clock = pygame.time.Clock()
font = pygame.font.Font(resource_path("fonts/harreegh_popped.ttf"), 30)

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
    "B         BB   BB  B",
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
    "up": pygame.transform.scale(pygame.image.load(
        resource_path(
            "sprites/player/back.png")), (TILE_SIZE, TILE_SIZE)),
    "down": pygame.transform.scale(pygame.image.load(
        resource_path(
            "sprites/player/front.png")), (TILE_SIZE, TILE_SIZE)),
    "left": pygame.transform.scale(pygame.image.load(
        resource_path(
            "sprites/player/side_left.png")), (TILE_SIZE, TILE_SIZE)),
    "right": pygame.transform.scale(pygame.image.load(
        resource_path(
            "sprites/player/side_right.png")), (TILE_SIZE, TILE_SIZE)),
}

player_rect = player_sprites["down"].get_rect()
player_rect.topleft = (120, 120)
player_speed = 4
player_direction = "down"

brick = pygame.image.load(resource_path("sprites/map/wall.png"))
brick_img = pygame.transform.scale(brick, (TILE_SIZE, TILE_SIZE))

walls = []
for y, row in enumerate(game_map):
    for x, cell in enumerate(row):
        if cell == 'B':
            wall_rect = pygame.Rect(
                x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            walls.append(wall_rect)

enemy_sprite = pygame.image.load(resource_path("sprites/enemy/enemy.png"))
enemy_sprite = pygame.transform.scale(enemy_sprite, (TILE_SIZE, TILE_SIZE))
enemy_speed = 4
enemy_rect = pygame.Rect(200, 200, TILE_SIZE, TILE_SIZE)
enemy_direction = random.choice(["up", "down", "left", "right"])

enemy_move_delay = 15
last_enemy_move_time = pygame.time.get_ticks()
enemy_paused = False
enemy_pause_start = 0
enemy_pause_duration = 0

hit_sprite = pygame.image.load(resource_path("sprites/splash/splash.png"))
hit_sprite = pygame.transform.scale(hit_sprite, (TILE_SIZE, TILE_SIZE))

hit_cooldown = 200
last_hit_time = 0
hit_position = None
hit_count = 0

# Enemy hit variables
enemy_hit_position = None
enemy_hit_cooldown = 800
last_enemy_hit_time = 0
enemy_hit_count = 0


def move_enemy(enemy_rect, direction):
    dx, dy = 0, 0
    if direction == "up":
        dy = -enemy_speed
    elif direction == "down":
        dy = enemy_speed
    elif direction == "left":
        dx = -enemy_speed
    elif direction == "right":
        dx = enemy_speed
    new_rect = enemy_rect.move(dx, dy)
    for wall in walls:
        if new_rect.colliderect(wall):
            return enemy_rect, False
    return new_rect, True


def distance(rect1, rect2):
    dx = rect1.centerx - rect2.centerx
    dy = rect1.centery - rect2.centery
    return math.hypot(dx, dy)


def get_direction_towards_player(enemy, player):
    dx = player.centerx - enemy.centerx
    dy = player.centery - enemy.centery
    if abs(dx) > abs(dy):
        return "right" if dx > 0 else "left"
    else:
        return "down" if dy > 0 else "up"


# Game loop

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

    current_time = pygame.time.get_ticks()

    # Player attack
    if (
        pygame.mouse.get_pressed()[0]
        and current_time - last_hit_time >= hit_cooldown
    ):
        last_hit_time = current_time
        if distance(player_rect, enemy_rect) <= TILE_SIZE:
            hit_position = player_rect.topleft
            hit_count += 1
            if hit_count >= 3:
                enemy_rect = pygame.Rect(
                    -TILE_SIZE, -TILE_SIZE, TILE_SIZE, TILE_SIZE)
                hit_count = 0
            hit_sound.play()
        else:
            hit_position = None

    # Enemy attack
    if distance(player_rect, enemy_rect) <= TILE_SIZE:
        if current_time - last_enemy_hit_time >= enemy_hit_cooldown:
            last_enemy_hit_time = current_time
            enemy_hit_position = player_rect.topleft
            enemy_hit_count += 1
            enemy_hit_sound.play()
    else:
        enemy_hit_position = None

    if enemy_hit_count == 3:
        screen.fill(BLACK)
        game_over_text = font.render("Игра окончена", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(width // 2, height // 2))
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    # Move enemy
    if enemy_paused:
        if current_time - enemy_pause_start >= enemy_pause_duration:
            enemy_paused = False
    else:
        if current_time - last_enemy_move_time > enemy_move_delay:
            if distance(enemy_rect, player_rect) <= TILE_SIZE * 2:
                enemy_direction = get_direction_towards_player(
                    enemy_rect, player_rect)
            new_rect, moved = move_enemy(enemy_rect, enemy_direction)
            if moved:
                enemy_rect = new_rect
            else:
                enemy_paused = True
                enemy_pause_start = current_time
                enemy_pause_duration = random.randint(2000, 5000)
                if distance(enemy_rect, player_rect) > TILE_SIZE * 2:
                    directions = ["up", "down", "left", "right"]
                    directions.remove(enemy_direction)
                    enemy_direction = random.choice(directions)
            last_enemy_move_time = current_time

    # Drawing
    screen.blit(background, (0, 0))
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == 'B':
                screen.blit(brick_img, (x * TILE_SIZE, y * TILE_SIZE))
    screen.blit(player_sprites[player_direction], player_rect.topleft)
    screen.blit(enemy_sprite, enemy_rect.topleft)

    if hit_position and distance(player_rect, enemy_rect) <= TILE_SIZE:
        x = hit_position[0] + TILE_SIZE // 2 - TILE_SIZE // 4
        y = hit_position[1]
        screen.blit(hit_sprite, (x, y))

    if enemy_hit_position:
        x = enemy_hit_position[0] + TILE_SIZE // 2 - TILE_SIZE // 4
        y = enemy_hit_position[1]
        screen.blit(hit_sprite, (x, y))

    pygame.display.flip()
    clock.tick(FPS)
