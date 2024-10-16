import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 5
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Font
FONT = pygame.font.SysFont(None, 36)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Number Puzzle")

def draw_grid(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = grid[row][col]
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY if (row + col) % 2 == 0 else WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if num != 0:
                text = FONT.render(str(num), True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def get_prime_factors(num):
    factors = []
    divisor = 2
    while num > 1:
        while num % divisor == 0:
            factors.append(divisor)
            num //= divisor
        divisor += 1
    return factors

def generate_pairs():
    pairs = set()
    for i in range(2, 21):  # Từ 2 đến 20 (bao gồm)
        prime_factors = get_prime_factors(i)
        for j in range(i + 1, 21):
            if all(j % factor == 0 for factor in prime_factors):
                pairs.add((i, j))
    return list(pairs)

def generate_solvable_grid():
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    pairs = generate_pairs()
    random.shuffle(pairs)
    for num1, num2 in pairs:
        placed = False
        while not placed:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            if grid[row][col] == 0:
                grid[row][col] = num1
                placed = True
                for i in range(GRID_SIZE):
                    if grid[row][i] == 0:
                        grid[row][i] = num2
                        break
                for j in range(GRID_SIZE):
                    if grid[j][col] == 0:
                        grid[j][col] = num2
                        break
    return grid

def get_gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def update_grid(grid, pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    num1 = grid[y1][x1]
    num2 = grid[y2][x2]

    if num1 == num2:
        grid[y1][x1] = 0
        grid[y2][x2] = 0
    elif num1 % num2 == 0:
        grid[y1][x1] = num1 // num2
        grid[y2][x2] = 0
    elif num2 % num1 == 0:
        grid[y1][x1] = 0
        grid[y2][x2] = num2 // num1
    else:
        gcd = get_gcd(num1, num2)
        grid[y1][x1] = num1 // gcd
        grid[y2][x2] = num2 // gcd

def is_game_won(grid):
    for row in grid:
        if any(num != 0 for num in row):
            return False
    return True

def main():
    clock = pygame.time.Clock()
    grid = generate_solvable_grid()
    history = []
    selected = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if selected:
                    if selected != (col, row):
                        history.append([row[:] for row in grid])
                        update_grid(grid, selected, (col, row))
                        selected = None
                else:
                    selected = (col, row)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u and history:
                    grid = history.pop()

        screen.fill(WHITE)
        draw_grid(grid)
        if is_game_won(grid):
            win_text = FONT.render("You Win!", True, BLUE)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(win_text, win_rect)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
