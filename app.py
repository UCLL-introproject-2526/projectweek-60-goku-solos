import pygame
import random

# The size of the application
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE
FPS = 60

# The color scheme of the application
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
COLORS = [
    (0, 255, 255),  # I
    (245,234,46),  # O
    (93, 63, 211),  # T
    (9, 121, 105),    # S
    (247,87,0),    # Z
    (17,59,214),    # J
    (243,200,172),  # L
]

# 2Tris Shapes
SHAPES = [
    [[1, 1, 1, 1]],

    [[1, 1],
     [1, 1]],

    [[0, 1, 0],
     [1, 1, 1]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[1, 0, 0],
     [1, 1, 1]],

    [[0, 0, 1],
     [1, 1, 1]],
]


# The class of piece, it will take the a random choice of a shape and color mentioned above, needs improvement;;
class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))


# First function creates a grid for the tetris, second determines when and how you are allowed to move,
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
                if new_y >= 0 and grid[new_y][new_x]:
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


def draw_grid(screen, grid):
    for y in range(ROWS):
        for x in range(COLS):
            color = grid[y][x]
            if color:
                pygame.draw.rect(
                    screen, color,
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )
            pygame.draw.rect(
                screen, GRAY,
                (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                1
            )


def draw_piece(screen, piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    piece.color,
                    ((piece.x + x) * BLOCK_SIZE,
                     (piece.y + y) * BLOCK_SIZE,
                     BLOCK_SIZE, BLOCK_SIZE)
                )
# The code under is needed to restart the game and when you lose
def draw_game_over(screen):
    font = pygame.font.SysFont(None, 38)
    text = font.render("You Lost! Try Again?", True, (66, 135, 245))
    sub = pygame.font.SysFont(None, 28).render(
        "Press R to Restart", True, (255, 255, 255)
    )

    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    sub_rect = sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))

    screen.blit(text, rect)
    screen.blit(sub, sub_rect)



# 
def main():
    game_over = False # needed for later, to start the game again

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Super Simple Tetris")
    clock = pygame.time.Clock()

    grid = create_grid()

    left_piece = Piece()
    right_piece = Piece()

    left_piece.x = 1
    right_piece.x = COLS - 4


    fall_time = 0

    running = True
    while running:
        dt = clock.tick(FPS)
        fall_time += dt

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
                        else:
                            left_piece = new_piece
                
                    else:
                        new_piece = Piece()
                        new_piece.x = COLS - 4
                        if not valid_move(new_piece, grid):
                            game_over = True
                        else:
                            right_piece = new_piece

                
                fall_time = 0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    grid = create_grid()
                    left_piece = Piece()
                    right_piece = Piece()
                    left_piece.x = 1
                    right_piece.x = COLS - 4
                    fall_time = 0
                    game_over = False

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

                # This is the code to move the tetris piecees, the code above is to move the left hand tetris piece and the code below is to move the right hand
                # Tetris piece, I tried to make it as simple as possible

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


        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_piece(screen, left_piece)
        draw_piece(screen, right_piece)
        if game_over:
            draw_game_over(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


