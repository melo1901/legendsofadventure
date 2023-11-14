import pygame
from settings import *

class UI:
    def __init__(self):
        # general

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.stamina_bar_rect = pygame.Rect(10, 34, STAMINA_BAR_SIZE, BAR_HEIGHT)

    def show_bar(self, current, max_am, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)


    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.stamina, player.stats['stamina'], self.stamina_bar_rect, STAMINA_COLOR)