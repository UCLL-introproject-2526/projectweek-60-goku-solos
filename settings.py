import pygame

ENABLE_PIECE_COLLISION = True


class Settings:
    def __init__(self):
        self.piece_collision = False  # off by default, on the theme of MERGING for the project :)

settings = Settings()
