import pygame
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, f"resources/{relative_path}")

# Инициализация Pygame
pygame.init()

# Устанавливаем размеры окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Устанавливаем заголовок окна
pygame.display.set_caption("Battle Kingdom")

# Цвет фона (для старого фона)
background_color = (0, 0, 0)

# Инициализация mixer для звука
pygame.mixer.init()
pygame.mixer.music.load(resource_path("music/Waterflame & Rutra - Pixel War.mp3"))
pygame.mixer.music.play(-1)

# Загрузка фонового изображения
background_image = pygame.image.load(resource_path("images/background.jpg"))
background_image = pygame.transform.scale(background_image, (width, height))  # Масштабируем изображение под окно

# Создание объекта для управления частотой кадров
clock = pygame.time.Clock()

# Шрифт для отображения времени
font = pygame.font.SysFont("Arial", 30)

while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

    # Заполнение экрана фоновым изображением
    screen.blit(background_image, (0, 0))

    # Получаем текущее время
    time_text = font.render(pygame.time.get_ticks() // 1000, True, (255, 255, 255))  # Время в секундах

    # Отображение времени на экране
    screen.blit(time_text, (10, 10))  # Отображаем текст в верхнем левом углу

    # Обновление экрана
    pygame.display.flip()

    # Устанавливаем частоту кадров (например, 60 FPS)
    clock.tick(60)
