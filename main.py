import pygame
import random
from ui import UI, Button , load_sounds , play_music
from settings import settings
import asyncio



# Size of window/application and the framerate
WIDTH_GAME, HEIGHT = 300, 600
WIDTH_WINDOW = 600
BLOCK_SIZE = 30
COLS = WIDTH_GAME // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE
FPS = 144

# Currently adding a settings menu where you can change the theme of the game post the main menu screen.
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
ORANGE_THEME = (246, 87, 2)

# Colors for all of the different blocks, these are the preset colors but we randomized which block gets
# which color, not preset colors for each unique block like in normal Tetris
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

# tetris pieces class
class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLS//2 - len(self.shape[0])//2
        self.y = 0
    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

# creating and definiing the grid
def create_grid():
    return [[None for _ in range(COLS)] for _ in range(ROWS)]

# enumerate is needed to get position and value, it gives the index whereas without it we wouldn't get it

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
            pygame.draw.rect(screen, BLACK, ((x+offset_x//BLOCK_SIZE)*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_piece(screen, piece, offset_x=0):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, piece.color, ((piece.x + x + offset_x//BLOCK_SIZE)*BLOCK_SIZE, (piece.y+y)*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_sidebar(screen, score,multiplier, sidebar_image):
    sidebar_rect = pygame.Rect(WIDTH_GAME, 0, WIDTH_WINDOW - WIDTH_GAME, HEIGHT)
    pygame.draw.rect(screen, GRAY, sidebar_rect)

    font = pygame.font.SysFont(None, 28)
    text = font.render(f"Score: {score:.1f}", True, WHITE)

    font = pygame.font.SysFont(None, 28)

    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    mult_text = font.render(f"Multiplier: x{multiplier}", True, WHITE)

    screen.blit(score_text, (WIDTH_GAME + 20, 20))
    screen.blit(mult_text, (WIDTH_GAME + 20, 50))



   

    # Score position
    score_x = WIDTH_GAME + 20
    score_y = 20
    screen.blit(text, (score_x, score_y))

    # Image position 
    image_x = WIDTH_GAME + 20
    image_y = score_y + 50  # spacing below score
    screen.blit(sidebar_image, (image_x, image_y))

# The ACTUAL game
async def main():
    pygame.init()

    MAX_SCORE = 200
    POWER_DURATION = 10000  # milliseconds (5 seconds)

    power_active = False
    power_start_time = 0
    
    score_multiplier = 1



    if power_active:
        if pygame.time.get_ticks() - power_start_time >= POWER_DURATION:
            power_active = False
            score_multiplier = 1
            
            




    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(8)

    
    
    screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT))
    sidebar_image_normal = pygame.image.load("assets/sidebar_image.webp").convert_alpha()
    sidebar_image_normal = pygame.transform.scale(sidebar_image_normal, (260, 520))

    sidebar_image_power = pygame.image.load("assets/sidebar_image_power.webp").convert_alpha()
    sidebar_image_power = pygame.transform.scale(sidebar_image_power, (260, 520))


    

    


    pygame.display.set_caption("Twotris")
    clock = pygame.time.Clock()
    ui = UI(screen, WIDTH_WINDOW, HEIGHT)

    #SOUND AND MUSIC

    sounds = load_sounds()   
    play_music()

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

    # Buttons, see beginning of file for the import from UI
    start_btn = Button(rect=(WIDTH_WINDOW//2-50, HEIGHT//2 + 100, 117, 35), text="Start", font=font_btn, bg_color=(ORANGE_THEME), text_color=(WHITE)) # 2 + 100 is needed to move it vertically down
    
    go_restart_btn = Button(rect=(WIDTH_WINDOW//2-80, HEIGHT//2, 160, 50), text="Restart", font=font_btn, bg_color=(50,50,150), text_color=(WHITE))
    
    go_quit_btn = Button(rect=(WIDTH_WINDOW//2-80, HEIGHT//2+70, 160, 50), text="Quit", font=font_btn, bg_color=(150,50,50), text_color=(WHITE))
    
    resume_btn = Button(rect=(WIDTH_WINDOW//2 - 80, 250, 160, 50), text="Resume", font=font_btn, bg_color=(50,150,50), text_color=(WHITE))
    
    pause_restart_btn = Button(rect=(WIDTH_WINDOW//2 - 80, 320, 160, 50), text="Restart", font=font_btn, bg_color=(50,50,150), text_color=(WHITE))
    
    pause_quit_btn = Button(rect=(WIDTH_WINDOW//2 - 80, 390, 160, 50), text="Quit", font=font_btn, bg_color=(150,50,50), text_color=(WHITE))

    settings_btn = Button(rect=(WIDTH_WINDOW//2 - 80, 330, 160, 50), text="Settings", font=font_btn, bg_color=(80,80,150), text_color=WHITE)


    pause_buttons = [resume_btn, pause_restart_btn, pause_quit_btn]

    running = True
    while running:
        dt = clock.tick(FPS)
        fall_time += dt

        if power_active:
            if pygame.time.get_ticks() - power_start_time >= POWER_DURATION:
                power_active = False
                score_multiplier = score_multiplier + 1
                MAX_SCORE = MAX_SCORE * 2 

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
                    score_multiplier= 1
                    power_active = False
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
                        power_active = False
                        score_multiplier=1
                        
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
                                power_active = False
                                score_multiplier = 1
                                game_over = False
                            elif button.text == "Quit":
                                running = False

        # buncha if statements, such as for when you're able to move (whether its game over etc.) and scoring
        if state == PLAYING and not game_over:
            if fall_time > 400:
                for piece in (left_piece, right_piece):
                    if valid_move(piece, grid, dy=1):
                        piece.y += 1
                    else:
                        lock_piece(piece, grid)
                        sounds["drop"].play()

                        grid, lines_cleared = clear_lines(grid)
                        if lines_cleared > 0:
                            sounds["clear"].play()

                        score += 67 * lines_cleared * score_multiplier # i finally fixed the scoring, it should be fine now
                        
                        

                        # Trigger power mode
                        if score >= MAX_SCORE and not power_active:
                            power_active = True
                            power_start_time = pygame.time.get_ticks()
                            score_multiplier = score_multiplier + 1   # or 3 if you’re feeling spicy

                        



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
                                sounds["gameover"].play()
                            else:
                                right_piece = new_piece
                fall_time = 0

        # UI drawing etc.
        screen.fill(settings.bg_color) # Here specifically calling the color from settings.py in order to have a different background color depending on the users setting.
        if state == START:
            ui.draw_start_menu(start_btn)

        elif state == PLAYING:
            
            draw_grid(screen, grid)
            draw_piece(screen, left_piece)
            draw_piece(screen, right_piece)
            if power_active == True:
                draw_sidebar(screen, score,score_multiplier,sidebar_image_power)
            else:
                draw_sidebar(screen,score,score_multiplier,sidebar_image_normal)
            


        elif state == GAME_OVER:
            
            draw_grid(screen, grid)
            draw_piece(screen, left_piece)
            draw_piece(screen, right_piece)
            if power_active == True:
                draw_sidebar(screen, score,score_multiplier,sidebar_image_power)
            else:
                draw_sidebar(screen, score,score_multiplier,sidebar_image_normal)
            ui.draw_game_over(go_restart_btn, go_quit_btn)

        elif state == PAUSED:
            
            draw_grid(screen, grid)
            draw_piece(screen, left_piece)
            draw_piece(screen, right_piece)
            if power_active == True:
                draw_sidebar(screen, score,score_multiplier,sidebar_image_power)
            else:
                draw_sidebar(screen,score,score_multiplier,sidebar_image_normal)
            ui.draw_pause_menu(pause_buttons)

        pygame.display.flip()
        
        await asyncio.sleep(0)


    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())