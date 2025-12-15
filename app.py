def main():
    import pygame
    pygame.init()


def create_main_surface(screen_size):
    pygame.init()
    pygame.display.set_mode(screen_size)

    try:
        while True:
            pygame.event.pump()
    except KeyboardInterrupt:
        pass

    pygame.quit()

create_main_surface((1024, 768))