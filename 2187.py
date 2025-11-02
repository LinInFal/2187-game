import pygame
import random
import sys
import math

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 500, 650
GRID_SIZE = 4
CELL_SIZE = 100
GRID_PADDING = 10
FONT_SIZE = 50
SMALL_FONT_SIZE = 24

# Цвета
BACKGROUND_COLOR = (250, 248, 239)
GRID_COLOR = (187, 173, 160)
EMPTY_CELL_COLOR = (205, 193, 180)
TEXT_COLOR = (119, 110, 101)
BRIGHT_TEXT_COLOR = (249, 246, 242)

# Цвета для разных значений клеток
CELL_COLORS = {
    1: (238, 228, 218),
    3: (237, 224, 200),
    9: (242, 177, 121),
    27: (245, 149, 99),
    81: (246, 124, 95),
    243: (246, 94, 59),
    729: (237, 207, 114),
    2187: (237, 204, 97),
    6561: (237, 200, 80),
    19683: (237, 197, 63),
    59049: (237, 194, 46)
}

# Целевое число (первое нечетное число после 2048)
TARGET = 2187  # 3^7 = 2187

class Game2048:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2187")
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.small_font = pygame.font.SysFont(None, SMALL_FONT_SIZE)
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.add_new_tile()
        self.add_new_tile()
    
    def add_new_tile(self):
        # Находим все пустые клетки
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            # С вероятностью 90% ставим 1, с 10% - 3
            self.grid[i][j] = 1 if random.random() < 0.9 else 3
    
    def get_color(self, value):
        return CELL_COLORS.get(value, (60, 58, 50))
    
    def get_text_color(self, value):
        return BRIGHT_TEXT_COLOR if value > 3 else TEXT_COLOR
    
    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Рисуем заголовок
        title = self.font.render("2187", True, TEXT_COLOR)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
        
        # Рисуем счет
        score_text = self.small_font.render(f"Счет: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (20, 80))
        
        # Рисуем целевое число
        target_text = self.small_font.render(f"Цель: {TARGET}", True, TEXT_COLOR)
        self.screen.blit(target_text, (WIDTH - target_text.get_width() - 20, 80))
        
        # Рисуем сетку
        grid_rect = pygame.Rect(
            (WIDTH - (CELL_SIZE * GRID_SIZE + GRID_PADDING * (GRID_SIZE + 1))) // 2,
            120,
            CELL_SIZE * GRID_SIZE + GRID_PADDING * (GRID_SIZE + 1),
            CELL_SIZE * GRID_SIZE + GRID_PADDING * (GRID_SIZE + 1)
        )
        pygame.draw.rect(self.screen, GRID_COLOR, grid_rect, border_radius=10)
        
        # Рисуем клетки
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell_rect = pygame.Rect(
                    grid_rect.left + GRID_PADDING + j * (CELL_SIZE + GRID_PADDING),
                    grid_rect.top + GRID_PADDING + i * (CELL_SIZE + GRID_PADDING),
                    CELL_SIZE,
                    CELL_SIZE
                )
                
                value = self.grid[i][j]
                if value == 0:
                    pygame.draw.rect(self.screen, EMPTY_CELL_COLOR, cell_rect, border_radius=5)
                else:
                    pygame.draw.rect(self.screen, self.get_color(value), cell_rect, border_radius=5)
                    
                    # Рисуем число
                    text = self.font.render(str(value), True, self.get_text_color(value))
                    text_rect = text.get_rect(center=cell_rect.center)
                    self.screen.blit(text, text_rect)
        
        # Сообщение о победе или проигрыше
        if self.won:
            win_text = self.font.render("Вы достигли цели!", True, (0, 128, 0))
            self.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT - 80))
        elif self.game_over:
            game_over_text = self.font.render("Игра окончена!", True, (255, 0, 0))
            self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT - 80))
        
        # Инструкция
        instruction = self.small_font.render("Используйте стрелки для перемещения", True, TEXT_COLOR)
        self.screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 60))

        restart = self.small_font.render("Используйте R для рестарта", True, TEXT_COLOR)
        self.screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT - 40))
        
        pygame.display.flip()
    
    def move(self, direction):
        # direction: 0 - вверх, 1 - вправо, 2 - вниз, 3 - влево
        moved = False
        
        if direction == 0:  # Вверх
            for j in range(GRID_SIZE):
                for i in range(1, GRID_SIZE):
                    if self.grid[i][j] != 0:
                        row = i
                        while row > 0 and self.grid[row-1][j] == 0:
                            self.grid[row-1][j] = self.grid[row][j]
                            self.grid[row][j] = 0
                            row -= 1
                            moved = True
                        if row > 0 and self.grid[row-1][j] == self.grid[row][j]:
                            self.grid[row-1][j] *= 3  # Умножаем на 3 вместо 2
                            self.score += self.grid[row-1][j]
                            self.grid[row][j] = 0
                            moved = True
        
        elif direction == 1:  # Вправо
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE-2, -1, -1):
                    if self.grid[i][j] != 0:
                        col = j
                        while col < GRID_SIZE-1 and self.grid[i][col+1] == 0:
                            self.grid[i][col+1] = self.grid[i][col]
                            self.grid[i][col] = 0
                            col += 1
                            moved = True
                        if col < GRID_SIZE-1 and self.grid[i][col+1] == self.grid[i][col]:
                            self.grid[i][col+1] *= 3
                            self.score += self.grid[i][col+1]
                            self.grid[i][col] = 0
                            moved = True
        
        elif direction == 2:  # Вниз
            for j in range(GRID_SIZE):
                for i in range(GRID_SIZE-2, -1, -1):
                    if self.grid[i][j] != 0:
                        row = i
                        while row < GRID_SIZE-1 and self.grid[row+1][j] == 0:
                            self.grid[row+1][j] = self.grid[row][j]
                            self.grid[row][j] = 0
                            row += 1
                            moved = True
                        if row < GRID_SIZE-1 and self.grid[row+1][j] == self.grid[row][j]:
                            self.grid[row+1][j] *= 3
                            self.score += self.grid[row+1][j]
                            self.grid[row][j] = 0
                            moved = True
        
        elif direction == 3:  # Влево
            for i in range(GRID_SIZE):
                for j in range(1, GRID_SIZE):
                    if self.grid[i][j] != 0:
                        col = j
                        while col > 0 and self.grid[i][col-1] == 0:
                            self.grid[i][col-1] = self.grid[i][col]
                            self.grid[i][col] = 0
                            col -= 1
                            moved = True
                        if col > 0 and self.grid[i][col-1] == self.grid[i][col]:
                            self.grid[i][col-1] *= 3
                            self.score += self.grid[i][col-1]
                            self.grid[i][col] = 0
                            moved = True
        
        if moved:
            self.add_new_tile()
            self.check_game_state()
        
        return moved
    
    def check_game_state(self):
        # Проверка на победу
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == TARGET:
                    self.won = True
                    return
        
        # Проверка на проигрыш
        # Если есть пустые клетки, игра продолжается
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return
        
        # Проверка возможных ходов
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                # Проверка соседей
                if i > 0 and self.grid[i][j] == self.grid[i-1][j]:
                    return
                if i < GRID_SIZE-1 and self.grid[i][j] == self.grid[i+1][j]:
                    return
                if j > 0 and self.grid[i][j] == self.grid[i][j-1]:
                    return
                if j < GRID_SIZE-1 and self.grid[i][j] == self.grid[i][j+1]:
                    return
        
        self.game_over = True
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if not self.game_over and not self.won:
                        if event.key == pygame.K_UP:
                            self.move(0)
                        elif event.key == pygame.K_RIGHT:
                            self.move(1)
                        elif event.key == pygame.K_DOWN:
                            self.move(2)
                        elif event.key == pygame.K_LEFT:
                            self.move(3)
                    # Перезапуск игры
                    if event.key == pygame.K_r:
                        self.__init__()
            
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game2048()
    game.run()
