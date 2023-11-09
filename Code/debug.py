import pygame

pygame.init()
font = pygame.font.SysFont("Arial", 30)


def debug_text(info, y=0, x=10):
    display_surface = pygame.display.get_surface()
    debug_surface = font.render(str(info), True, (255, 255, 255))
    debug_rectangle = debug_surface.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, (0, 0, 0), debug_rectangle)
    display_surface.blit(debug_surface, debug_rectangle)
