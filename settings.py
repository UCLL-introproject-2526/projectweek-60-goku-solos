import pygame

class Settings:
    def __init__(self):
        self.dark_theme = True

    @property
    def bg_color(self):
        return (0, 0, 0) if self.dark_theme else (255, 255, 255)

settings = Settings()
