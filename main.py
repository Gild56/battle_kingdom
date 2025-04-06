import pygame
import sys
import os


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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    pygame.display.flip()

    clock.tick(FPS)
