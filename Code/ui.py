import pygame
from settings import *

class UI:
    def __init__(self):
        # general

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.stamina_bar_rect = pygame.Rect(10, 34, MANA_BAR_SIZE, BAR_HEIGHT)

        # convert weapon dict
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path)
            weapon.set_colorkey((255, 255, 255))
            weapon.convert_alpha()
            self.weapon_graphics.append(weapon)

        # convert magic dict
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path)
            magic.set_colorkey((255, 255, 255))
            magic.convert_alpha()
            self.magic_graphics.append(magic)

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
        
    def show_tmp_bar(self, player, bg_rect, color):
        transition_width = 0
        transition_color = (255, 255, 0,)
        ratio = player.target_health / player.max_health
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        if player.health < player.target_health:
            transition_width = int((player.target_health - player.health) / player.max_health * bg_rect.width)
            transition_color = (0, 255, 0)
            player.health += 0.5
            # Clamp health to the target_health to avoid overshooting
            player.health = min(player.health, player.target_health)
            ratio = player.health / player.max_health
        elif player.health > player.target_health:
            transition_width = abs(int((player.target_health - player.health)) / player.max_health * bg_rect.width)
            transition_color = (255, 255, 0)
            player.health -= 0.5
            # Clamp health to the target_health to avoid overshooting
            player.health = max(player.health, player.target_health)
            ratio = player.target_health / player.max_health  # Use target_health here

        # Convert stat to pixel    
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        transition_bar = pygame.Rect(current_rect.right, 10, transition_width, 20)

        pygame.draw.rect(self.display_surface, transition_color, transition_bar)
        pygame.draw.rect(self.display_surface, color, current_rect)
        
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)


    def show_num(self, exp, gold):
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

        text_surf = self.font.render((str(int(gold)) + " $"), False, TEXT_COLOR)
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

    def magic_overlay(self, magic_index):
        bg_rect = self.selection_box(80,(self.display_surface.get_size()[1] - 90)) # weapon
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)
        
        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_tmp_bar(player, self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.mana, player.stats['mana'], self.stamina_bar_rect, MANA_COLOR)

        self.show_num(player.exp, player.gold)
        
        self.weapon_overlay(player.weapon_index)
        self.magic_overlay(player.magic_index)