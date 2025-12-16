import pygame

WHITE = (255, 255, 255)
RED = (255, 60, 60)
GRAY = (40, 40, 40)

class UI:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        pygame.font.init()
        self.title_font = pygame.font.SysFont(None, 56)
        self.text_font = pygame.font.SysFont(None, 28)

    def draw_center_text(self, text, font, color, y_offset=0):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(self.width//2, self.height//2 + y_offset))
        self.screen.blit(surface, rect)

    def draw_start_menu(self):
        self.screen.fill(GRAY)
        self.draw_center_text("SUPER SIMPLE TETRIS", self.title_font, WHITE, -40)
        self.draw_center_text("Press SPACE to Start", self.text_font, WHITE, 20)

    def draw_game_over(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        self.draw_center_text("YOU LOST!", self.title_font, RED, -20)
        self.draw_center_text("Press R to Restart", self.text_font, WHITE, 30)
    