import pygame
from settings import *

class Upgrade:
    def __init__(self,player):

        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attrib_nr = len(player.stats)
        self.attrib_names = list(player.stats.keys())
        self.max_values = list(player.max_stats)
        self.font = pygame.font.Font(UPGRADE_UI_FONT, UI_FONT_SIZE)

        # selection system
        self.select_index = 0
        self.select_time = None
        self.can_move = True

        # item dimensions
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.select_index < self.attrib_nr - 1:
                self.select_index += 1
                self.can_move = False
                self.select_time = pygame.time.get_ticks()
            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.select_index >= 1:
                self.select_index -= 1
                self.can_move = False
                self.select_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.select_time = pygame.time.get_ticks()
                self.item_list[self.select_index].trigger(self.player)

    def select_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.select_time >= 200:
                self.can_move = True

    def create_items(self):
        self.item_list = []
        
        for item, index in enumerate(range(self.attrib_nr)):
            # horizontal
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attrib_nr
            left = (item * increment) + (increment - self.width) // 2

            # vertical
            top = self.display_surface.get_size()[1] * 0.1

            # create object
            item = Item(left, top, self.width, self.height, index,self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.select_cooldown()
        
        for index, item in enumerate(self.item_list):
            name = self.attrib_names[index].upper()
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_exp_cost_by_index(index)
            item.display(self.display_surface,self.select_index,name,value,max_value,cost)

class Item:
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font

    def display_names(self,surface,name,cost,selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # title
        title_surf = self.font.render(name,False,color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        # cost
        cost_surf = self.font.render(f'{int(cost)} EXP',False,color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))
        surface.blit(title_surf,title_rect)
        surface.blit(cost_surf,cost_rect)

    def trigger(self,player):
        upgrade_attrib = list(player.stats.keys())[self.index]

        if upgrade_attrib == "health":
            if player.exp >= player.upgrade_exp_cost[upgrade_attrib] and player.stats[upgrade_attrib] < player.max_stats[upgrade_attrib]:
                player.exp -= player.upgrade_exp_cost[upgrade_attrib]
                player.max_health += player.upgrade_exp_value[upgrade_attrib]
                player.upgrade_exp_cost[upgrade_attrib] += 50

            if player.max_health > player.max_stats[upgrade_attrib]:
                player.max_health = player.max_stats[upgrade_attrib]
        
        else:
            if player.exp >= player.upgrade_exp_cost[upgrade_attrib] and player.stats[upgrade_attrib] < player.max_stats[upgrade_attrib]:
                player.exp -= player.upgrade_exp_cost[upgrade_attrib]
                player.stats[upgrade_attrib] += player.upgrade_exp_value[upgrade_attrib]
                player.upgrade_exp_cost[upgrade_attrib] += 50

            if player.stats[upgrade_attrib] > player.max_stats[upgrade_attrib]:
                player.stats[upgrade_attrib] = player.max_stats[upgrade_attrib]

    def display(self,surface,select_nr,name,value,max_value,cost):
        background = UI_BG_COLOR
        border = UI_BORDER_COLOR
        if self.index == select_nr:
            background = UPGRADE_BG_COLOR_SELECTED
            
        pygame.draw.rect(surface,background,self.rect)
        pygame.draw.rect(surface,border,self.rect,4)    
        self.display_names(surface,name,cost,self.index == select_nr)