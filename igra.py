import pygame
import sys

# Инициализация Pygame
pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Определение размеров окна
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)

# Создание окна
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Пинг-Понг")

# Определение начальных позиций платформ и мяча
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20

# Позиции платформ
paddle1_x, paddle1_y = 10, HEIGHT // 2 - PADDLE_HEIGHT // 2
paddle2_x, paddle2_y = WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2

# Позиция мяча
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 4, 4

# Скорость платформ
paddle_speed = 6

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обработка нажатий клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if keys[pygame.K_s] and paddle1_y < HEIGHT - PADDLE_HEIGHT:
        paddle1_y += paddle_speed
    if keys[pygame.K_UP] and paddle2_y > 0:
        paddle2_y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle2_y < HEIGHT - PADDLE_HEIGHT:
        paddle2_y += paddle_speed

    # Движение мяча
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Проверка столкновений с верхней и нижней границами
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_speed_y *= -1

    # Проверка столкновений с платформами
    if (ball_x <= paddle1_x + PADDLE_WIDTH and paddle1_y <= ball_y <= paddle1_y + PADDLE_HEIGHT) or \
       (ball_x >= paddle2_x - BALL_SIZE and paddle2_y <= ball_y <= paddle2_y + PADDLE_HEIGHT):
        ball_speed_x *= -1

    # Проверка выхода мяча за границы экрана
    if ball_x < 0 or ball_x > WIDTH:
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= -1
        ball_speed_y *= -1

    # Отрисовка элементов на экране
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (paddle1_x, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (paddle2_x, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

