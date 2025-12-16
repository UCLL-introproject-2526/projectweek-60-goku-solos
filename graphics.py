import pygame

class AnimatedBackground:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.y = 0
        self.speed = 1

        self.surface = pygame.Surface((width, height))
        self.surface.fill((30, 30, 30))  # dark background

    def update(self):
        self.y += self.speed
        if self.y >= self.height:
            self.y = 0

    def draw(self, screen):
        screen.blit(self.surface, (0, self.y))
        screen.blit(self.surface, (0, self.y - self.height))
