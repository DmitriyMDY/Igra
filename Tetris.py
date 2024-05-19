import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение размеров экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

# Определение размеров сетки
GRID_WIDTH, GRID_HEIGHT = 10, 20
CELL_SIZE = 30

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (0, 255, 255),
    (0, 0, 255),
    (255, 165, 0),
    (255, 255, 0),
    (0, 255, 0),
    (255, 0, 0),
    (128, 0, 128)
]

# Определение фигур
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.game_over = False

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {'shape': shape, 'color': color, 'x': GRID_WIDTH // 2 - len(shape[0]) // 2, 'y': 0}

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(screen, self.grid[y][x], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def draw_piece(self, piece):
        shape = piece['shape']
        color = piece['color']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, color, ((piece['x'] + x) * CELL_SIZE, (piece['y'] + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def rotate_piece(self):
        shape = self.current_piece['shape']
        self.current_piece['shape'] = [list(row) for row in zip(*shape[::-1])]

    def is_valid_move(self, dx, dy, shape=None):
        if shape is None:
            shape = self.current_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_piece['x'] + x + dx
                    new_y = self.current_piece['y'] + y + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True

    def place_piece(self):
        shape = self.current_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        if not self.is_valid_move(0, 0):
            self.game_over = True

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        cleared_lines = GRID_HEIGHT - len(new_grid)
        self.score += cleared_lines ** 2
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(cleared_lines)] + new_grid

    def update(self):
        if not self.game_over:
            if self.is_valid_move(0, 1):
                self.current_piece['y'] += 1
            else:
                self.place_piece()

    def move_piece(self, dx):
        if self.is_valid_move(dx, 0):
            self.current_piece['x'] += dx

    def hard_drop(self):
        while self.is_valid_move(0, 1):
            self.current_piece['y'] += 1
        self.place_piece()

def main():
    game = Tetris()
    clock = pygame.time.Clock()
    fall_time = 0

    while not game.game_over:
        screen.fill(BLACK)
        fall_speed = 500

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_piece(-1)
                elif event.key == pygame.K_RIGHT:
                    game.move_piece(1)
                elif event.key == pygame.K_DOWN:
                    game.update()
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()

        fall_time += clock.get_rawtime()
        if fall_time >= fall_speed:
            game.update()
            fall_time = 0

        game.draw_grid()
        game.draw_piece(game.current_piece)

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
