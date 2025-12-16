import pygame

WHITE = (255, 255, 255)
RED = (255, 60, 60)
GRAY = (40, 40, 40)

class Button:
    def __init__(self, rect, text, font, bg_color, text_color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.surface = self.font.render(self.text, True, self.text_color)
        self.surface_rect = self.surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        screen.blit(self.surface, self.surface_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class UI:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        pygame.font.init()
        self.menu_bg = pygame.image.load("assets/menu_bg.webp").convert()
        self.menu_bg = pygame.transform.scale(self.menu_bg, (width, height))
        self.title_font = pygame.font.SysFont(None, 64)

    def draw_center_text(self, text, font, color, y_offset=0),:
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(self.width//2, self.height//2 + y_offset))
        self.screen.blit(surface, rect)

    def draw_start_menu(self, start_button):
        self.screen.blit(self.menu_bg, (0, 0))
        self.draw_center_text("2Tris", self.title_font, WHITE, -40)
        start_button.draw(self.screen)

    def draw_game_over(self, restart_button, quit_button):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        self.draw_center_text("You Lost! Try Again?", self.title_font, RED, -80)
        restart_button.draw(self.screen)
        quit_button.draw(self.screen)

    def draw_pause_menu(self, buttons):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0,0,0))
        self.screen.blit(overlay, (0,0))
        self.draw_center_text("PAUSED", self.title_font, WHITE, -80)
        for button in buttons:
            button.draw(self.screen)