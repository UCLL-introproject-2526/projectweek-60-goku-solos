import pygame
import random
from ui import UI

# --- Constants ---
WIDTH_GAME, HEIGHT = 300, 600
WIDTH_WINDOW = 600
BLOCK_SIZE = 30
COLS = WIDTH_GAME // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE
FPS = 60

BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
COLORS = [
    (0, 255, 255),  # I
    (255, 255, 0),  # O
    (255, 0, 255),  # T
    (0, 255, 0),    # S
    (255, 0, 0),    # Z
    (0, 0, 255),    # J
    (255, 165, 0),  # L
]

SHAPES = [
    [[1,1,1,1]],
    [[1,1],[1,1]],
    [[0,1,0],[1,1,1]],
    [[0,1,1],[1,1,0]],
    [[1,1,0],[0,1,1]],
    [[1,0,0],[1,1,1]],
    [[0,0,1],[1,1,1]],
]

# --- Piece class ---
class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLS//2 - len(self.shape[0])//2
        self.y = 0
    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

# --- Grid functions ---
def create_grid():
    return [[None for _ in range(COLS)] for _ in range(ROWS)]

def valid_move(piece, grid, dx=0, dy=0):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = piece.x + x + dx
                new_y = piece.y + y + dy
                if new_x < 0 or new_x >= COLS or new_y >= ROWS:
                    return False
                if new_y >=0 and grid[new_y][new_x]:
                    return False
    return True

def lock_piece(piece, grid):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[piece.y + y][piece.x + x] = piece.color

def clear_lines(grid):
    new_grid = [row for row in grid if None in row]
    lines_cleared = ROWS - len(new_grid)
    for _ in range(lines_cleared):
        new_grid.insert(0, [None for _ in range(COLS)])
    return new_grid

def draw_grid(screen, grid, offset_x=0):
    for y in range(ROWS):
        for x in range(COLS):
            color = grid[y][x]
            if color:
                pygame.draw.rect(screen, color, ((x+offset_x//BLOCK_SIZE)*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, GRAY, ((x+offset_x//BLOCK_SIZE)*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_piece(screen, piece, offset_x=0):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, piece.color, ((piece.x + x + offset_x//BLOCK_SIZE)*BLOCK_SIZE, (piece.y+y)*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_sidebar(screen):
    sidebar_rect = pygame.Rect(WIDTH_GAME, 0, WIDTH_WINDOW - WIDTH_GAME, HEIGHT)
    pygame.draw.rect(screen, (30,30,30), sidebar_rect)
    font = pygame.font.SysFont(None, 24)
    text = font.render("Sidebar: Score / Next / Info", True, (200,200,200))
    screen.blit(text, (WIDTH_GAME + 20, 20))

# --- Main ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT))
    pygame.display.set_caption("Super Simple Tetris")
    clock = pygame.time.Clock()
    ui = UI(screen, WIDTH_WINDOW, HEIGHT)

    START = "start"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    state = START

    grid = create_grid()
    left_piece = Piece()
    right_piece = Piece()
    left_piece.x = 1
    right_piece.x = COLS - 4
    fall_time = 0
    game_over = False

    running = True
    while running:
        dt = clock.tick(FPS)
        fall_time += dt

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Escape → main menu
                if event.key == pygame.K_ESCAPE:
                    state = START
                    grid = create_grid()
                    left_piece = Piece()
                    right_piece = Piece()
                    left_piece.x = 1
                    right_piece.x = COLS - 4
                    fall_time = 0
                    game_over = False
                # Start game
                elif state == START and event.key == pygame.K_SPACE:
                    grid = create_grid()
                    left_piece = Piece()
                    right_piece = Piece()
                    left_piece.x = 1
                    right_piece.x = COLS - 4
                    fall_time = 0
                    state = PLAYING
                    game_over = False
                # Restart game
                elif state == GAME_OVER and event.key == pygame.K_r:
                    state = START

                # Controls for playing
                if state == PLAYING:
                    # Left piece - WASD
                    if event.key == pygame.K_a and valid_move(left_piece, grid, dx=-1):
                        left_piece.x -= 1
                    elif event.key == pygame.K_d and valid_move(left_piece, grid, dx=1):
                        left_piece.x += 1
                    elif event.key == pygame.K_s and valid_move(left_piece, grid, dy=1):
                        left_piece.y += 1
                    elif event.key == pygame.K_w:
                        old = left_piece.shape
                        left_piece.rotate()
                        if not valid_move(left_piece, grid):
                            left_piece.shape = old
                    # Right piece - arrows
                    elif event.key == pygame.K_LEFT and valid_move(right_piece, grid, dx=-1):
                        right_piece.x -= 1
                    elif event.key == pygame.K_RIGHT and valid_move(right_piece, grid, dx=1):
                        right_piece.x += 1
                    elif event.key == pygame.K_DOWN and valid_move(right_piece, grid, dy=1):
                        right_piece.y += 1
                    elif event.key == pygame.K_UP:
                        old = right_piece.shape
                        right_piece.rotate()
                        if not valid_move(right_piece, grid):
                            right_piece.shape = old

        # --- Game logic ---
        if state == PLAYING and not game_over:
            if fall_time > 400:
                for piece in (left_piece, right_piece):
                    if game_over:
                        break
                    if valid_move(piece, grid, dy=1):
                        piece.y += 1
                    else:
                        lock_piece(piece, grid)
                        grid = clear_lines(grid)
                        if piece == left_piece:
                            new_piece = Piece()
                            new_piece.x = 1
                            if not valid_move(new_piece, grid):
                                game_over = True
                                state = GAME_OVER
                            else:
                                left_piece = new_piece
                        else:
                            new_piece = Piece()
                            new_piece.x = COLS - 4
                            if not valid_move(new_piece, grid):
                                game_over = True
                                state = GAME_OVER
                            else:
                                right_piece = new_piece
                fall_time = 0

        # --- Drawing ---
        screen.fill(BLACK)

        if state == START:
            ui.draw_start_menu()
        elif state == PLAYING:
            draw_grid(screen, grid, offset_x=0)
            draw_piece(screen, left_piece, offset_x=0)
            draw_piece(screen, right_piece, offset_x=0)
            draw_sidebar(screen)
        elif state == GAME_OVER:
            draw_grid(screen, grid, offset_x=0)
            draw_piece(screen, left_piece, offset_x=0)
            draw_piece(screen, right_piece, offset_x=0)
            draw_sidebar(screen)
            ui.draw_game_over()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
