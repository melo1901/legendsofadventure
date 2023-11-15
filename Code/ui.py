import pygame
from settings import *

class UI:
    def __init__(self):
        # general

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.stamina_bar_rect = pygame.Rect(10, 34, STAMINA_BAR_SIZE, BAR_HEIGHT)

        # convert weapon dict
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path)
            weapon.set_colorkey((255, 255, 255))
            weapon.convert_alpha()
            self.weapon_graphics.append(weapon)

    def show_bar(self, current, max_am, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_am
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        # draw a bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect,3)

    def show_num(self, exp, money):
        #exp values
        
        text_surf = self.font.render((str(int(exp)) + " XP"),False,TEXT_COLOR)        
        x = self.display_surface.get_size()[0] - 20
        y = 45
        text_rect = text_surf.get_rect(bottomright=(x, y))

        # draw the exp
        
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20),3)

        # money values

        text_surf = self.font.render((str(int(money)) + " $"), False, TEXT_COLOR)
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))
        
        # draw the money

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20),3)
   
    def selection_box(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index):
        bg_rect = self.selection_box(10,(self.display_surface.get_size()[1] - 110)) # weapon
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        
        self.display_surface.blit(weapon_surf, weapon_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.stamina, player.stats['stamina'], self.stamina_bar_rect, STAMINA_COLOR)

        self.show_num(player.exp, player.money)
        
        self.weapon_overlay(player.weapon_index)
        self.selection_box(80,(self.display_surface.get_size()[1] - 90)) # magic