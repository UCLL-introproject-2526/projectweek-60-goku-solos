import pygame
import random
from ui import UI, Button

# Size of window/application and the framerate
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

# --- Piece Class ---
class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLS//2 - len(self.shape[0])//2
        self.y = 0
    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

# -creating and definiing the grid
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
    return new_grid, lines_cleared

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

def draw_sidebar(screen, score):
    sidebar_rect = pygame.Rect(WIDTH_GAME, 0, WIDTH_WINDOW - WIDTH_GAME, HEIGHT)
    pygame.draw.rect(screen, (30,30,30), sidebar_rect)
    font = pygame.font.SysFont(None, 28)
    text = font.render(f"Score: {score:.1f}", True, (200,200,200))
    screen.blit(text, (WIDTH_GAME + 20, 20))

# --- Main ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT))
    pygame.display.set_caption("2Tris")
    clock = pygame.time.Clock()
    ui = UI(screen, WIDTH_WINDOW, HEIGHT)

    START, PLAYING, GAME_OVER, PAUSED = "start", "playing", "game_over", "paused"
    state = START
    game_over = False

    grid = create_grid()
    left_piece = Piece()
    right_piece = Piece()
    left_piece.x = 1
    right_piece.x = COLS - 4
    fall_time = 0
    score = 0.0

    font_btn = pygame.font.SysFont(None, 32)

    # --- Buttons ---
    start_btn = Button(rect=(WIDTH_WINDOW//2-80, HEIGHT//2, 160, 50),
                       text="Start", font=font_btn,
                       bg_color=(50,150,50), text_color=(255,255,255))
    go_restart_btn = Button(rect=(WIDTH_WINDOW//2-80, HEIGHT//2, 160, 50),
                            text="Restart", font=font_btn,
                            bg_color=(50,50,150), text_color=(255,255,255))
    go_quit_btn = Button(rect=(WIDTH_WINDOW//2-80, HEIGHT//2+70, 160, 50),
                         text="Quit", font=font_btn,
                         bg_color=(150,50,50), text_color=(255,255,255))
    resume_btn = Button(rect=(WIDTH_WINDOW//2 - 80, 250, 160, 50),
                        text="Resume", font=font_btn,
                        bg_color=(50,150,50), text_color=(255,255,255))
    pause_restart_btn = Button(rect=(WIDTH_WINDOW//2 - 80, 320, 160, 50),
                               text="Restart", font=font_btn,
                               bg_color=(50,50,150), text_color=(255,255,255))
    pause_quit_btn = Button(rect=(WIDTH_WINDOW//2 - 80, 390, 160, 50),
                            text="Quit", font=font_btn,
                            bg_color=(150,50,50), text_color=(255,255,255))
    pause_buttons = [resume_btn, pause_restart_btn, pause_quit_btn]

    running = True
    while running:
        dt = clock.tick(FPS)
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:  # returns to main menu
                    state = START
                    grid = create_grid()
                    left_piece = Piece()
                    right_piece = Piece()
                    left_piece.x = 1
                    right_piece.x = COLS - 4
                    fall_time = 0
                    score = 0.0
                    game_over = False
                if state == PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        state = PAUSED
                    # Left piece (WASD CONTROLS)
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
                    # Right piece (ARROW KEY CONTROLS)
                    if event.key == pygame.K_LEFT and valid_move(right_piece, grid, dx=-1):
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
                elif state == PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        state = PLAYING

            # Mouse click buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if state == START and start_btn.is_hovered(mouse_pos):
                    state = PLAYING
                    grid = create_grid()
                    left_piece = Piece()
                    right_piece = Piece()
                    left_piece.x = 1
                    right_piece.x = COLS - 4
                    fall_time = 0
                    score = 0.0
                    game_over = False
                elif state == GAME_OVER:
                    if go_restart_btn.is_hovered(mouse_pos):
                        state = PLAYING
                        grid = create_grid()
                        left_piece = Piece()
                        right_piece = Piece()
                        left_piece.x = 1
                        right_piece.x = COLS - 4
                        fall_time = 0
                        score = 0.0
                        game_over = False
                    elif go_quit_btn.is_hovered(mouse_pos):
                        running = False
                elif state == PAUSED:
                    for button in pause_buttons:
                        if button.is_hovered(mouse_pos):
                            if button.text == "Resume":
                                state = PLAYING
                            elif button.text == "Restart":
                                state = PLAYING
                                grid = create_grid()
                                left_piece = Piece()
                                right_piece = Piece()
                                left_piece.x = 1
                                right_piece.x = COLS - 4
                                fall_time = 0
                                score = 0.0
                                game_over = False
                            elif button.text == "Quit":
                                running = False

        # Logic
        if state == PLAYING and not game_over:
            if fall_time > 400:
                for piece in (left_piece, right_piece):
                    if valid_move(piece, grid, dy=1):
                        piece.y += 1
                    else:
                        lock_piece(piece, grid)
                        grid, lines_cleared = clear_lines(grid)
                        score += 6.7 * lines_cleared  # i finally fixed the scoring, it should be fine now

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

        # UI drawing etc.
        screen.fill(BLACK)
        if state == START:
            ui.draw_start_menu(start_btn)
        elif state == PLAYING:
            draw_grid(screen, grid)
            draw_piece(screen, left_piece)
            draw_piece(screen, right_piece)
            draw_sidebar(screen, score)
        elif state == GAME_OVER:
            draw_grid(screen, grid)
            draw_piece(screen, left_piece)
            draw_piece(screen, right_piece)
            draw_sidebar(screen, score)
            ui.draw_game_over(go_restart_btn, go_quit_btn)
        elif state == PAUSED:
            draw_grid(screen, grid)
            draw_piece(screen, left_piece)
            draw_piece(screen, right_piece)
            draw_sidebar(screen, score)
            ui.draw_pause_menu(pause_buttons)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
