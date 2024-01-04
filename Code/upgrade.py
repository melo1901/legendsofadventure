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

    def get_exp_amounts_by_index(self,name):
        return upgrade_exp_data[name]['actual'], upgrade_exp_data[name]['max']

    def display(self):
        self.input()
        self.select_cooldown()
        
        for index, item in enumerate(self.item_list):
            name = self.attrib_names[index].upper()
            cost = self.player.get_exp_cost_by_index(index)
            amount, max_amount = self.get_exp_amounts_by_index(name.lower())
            item.display(self.display_surface,self.select_index,name,cost,amount,max_amount)

class Shop:
    def __init__(self,player):

        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attrib_nr = len(player.upgrade_gold_names)
        self.attrib_names = list(player.upgrade_gold_names.keys())
        self.name_amount = list(self.player.upgrade_gold_cost.keys())
        self.max_values = list(player.upgrade_gold_max_values)
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
            item = ShopItem(left, top, self.width, self.height, index,self.font)
            self.item_list.append(item)

    def get_gold_amounts_by_index(self,name):
        return upgrade_gold_data[name]['actual'], upgrade_gold_data[name]['max']

    def display(self):
        self.input()
        self.select_cooldown()
        
        for index, item in enumerate(self.item_list):
            name = self.attrib_names[index].upper()
            cost = self.player.get_gold_cost_by_index(index)
            names = self.name_amount[index]
            amount, max_amount = self.get_gold_amounts_by_index(names)
            item.display(self.display_surface,self.select_index,name,cost,amount,max_amount)

class ShopItem:
    def __init__(self,l,t,w,h,index,font):
            self.rect = pygame.Rect(l,t,w,h)
            self.index = index
            self.font = font

    def display_names(self,surface,name,cost,amount,max_amount,selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # title
        title_surf = self.font.render(name,False,color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        # amount
        amount_str = "LEVEL " + str(amount) + "/" + str(max_amount)
        amount_surf = self.font.render(amount_str,False,color)
        amount_rect = amount_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,title_rect[1] + 20))        
        # cost
        cost_surf = self.font.render(f'{int(cost)} $',False,color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))
        surface.blit(title_surf,title_rect)
        surface.blit(amount_surf,amount_rect)
        surface.blit(cost_surf,cost_rect)

    def trigger(self,player):
        upgrade_attrib = list(player.upgrade_gold_cost.keys())[self.index]

        if upgrade_attrib == "sword" or upgrade_attrib == "axe":
            if player.gold >= player.upgrade_gold_cost[upgrade_attrib] and weapon_data[upgrade_attrib]['damage'] < player.upgrade_gold_max_values[upgrade_attrib]:
                weapon_data[upgrade_attrib]['damage'] += player.upgrade_gold_value[upgrade_attrib]
                player.gold -= player.upgrade_gold_cost[upgrade_attrib]
                player.upgrade_gold_cost[upgrade_attrib] += 5
                upgrade_gold_data[upgrade_attrib]['actual'] += 1
            if weapon_data[upgrade_attrib]['damage'] > player.upgrade_gold_max_values[upgrade_attrib]:
                weapon_data[upgrade_attrib]['damage'] = player.upgrade_gold_max_values[upgrade_attrib]
        elif upgrade_attrib == "heal":
            if player.gold >= player.upgrade_gold_cost[upgrade_attrib] and magic_data[upgrade_attrib]['strength'] < player.upgrade_gold_max_values[upgrade_attrib]:
                magic_data[upgrade_attrib]['strength'] += player.upgrade_gold_value[upgrade_attrib]
                player.gold -= player.upgrade_gold_cost[upgrade_attrib]
                player.upgrade_gold_cost[upgrade_attrib] += 5
                upgrade_gold_data[upgrade_attrib]['actual'] += 1
            if magic_data[upgrade_attrib]['strength'] > player.upgrade_gold_max_values[upgrade_attrib]:
                magic_data[upgrade_attrib]['strength'] = player.upgrade_gold_max_values[upgrade_attrib]
        elif upgrade_attrib == "flame_damage":
            if player.gold >= player.upgrade_gold_cost[upgrade_attrib] and magic_data['flame']['damage'] < player.upgrade_gold_max_values[upgrade_attrib]:
                magic_data['flame']['damage'] += player.upgrade_gold_value[upgrade_attrib]
                player.gold -= player.upgrade_gold_cost[upgrade_attrib]
                player.upgrade_gold_cost[upgrade_attrib] += 5
                upgrade_gold_data[upgrade_attrib]['actual'] += 1
            if magic_data['flame']['damage'] > player.upgrade_gold_max_values[upgrade_attrib]:
                magic_data['flame']['damage'] = player.upgrade_gold_max_values[upgrade_attrib]
        elif upgrade_attrib == "flame_range":
            if player.gold >= player.upgrade_gold_cost[upgrade_attrib] and player.magic_range < player.upgrade_gold_max_values[upgrade_attrib]:
                player.magic_range += player.upgrade_gold_value[upgrade_attrib]
                player.gold -= player.upgrade_gold_cost[upgrade_attrib]
                player.upgrade_gold_cost[upgrade_attrib] += 10
                upgrade_gold_data[upgrade_attrib]['actual'] += 1
            if player.magic_range > player.upgrade_gold_max_values[upgrade_attrib]:
                player.magic_range = player.upgrade_gold_max_values[upgrade_attrib]

    def display(self,surface,select_nr,name,cost,amount,max_amount):
        background = UI_BG_COLOR
        border = UI_BORDER_COLOR
        if self.index == select_nr:
            background = UPGRADE_BG_COLOR_SELECTED
            
        pygame.draw.rect(surface,background,self.rect)
        pygame.draw.rect(surface,border,self.rect,4)    
        self.display_names(surface,name,cost,amount,max_amount,self.index == select_nr)

class Item:
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font

    def display_names(self,surface,name,cost,amount,max_amount,selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # title
        title_surf = self.font.render(name,False,color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        # amount
        amount_str = "LEVEL " + str(amount) + "/" + str(max_amount)
        amount_surf = self.font.render(amount_str,False,color)
        amount_rect = amount_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,title_rect[1] + 20))

        # cost
        cost_surf = self.font.render(f'{int(cost)} EXP',False,color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))
        surface.blit(title_surf,title_rect)
        surface.blit(amount_surf,amount_rect)
        surface.blit(cost_surf,cost_rect)

    def trigger(self,player):
        upgrade_attrib = list(player.stats.keys())[self.index]

        if upgrade_attrib == "health":
            if player.exp >= player.upgrade_exp_cost[upgrade_attrib] and player.max_health < player.max_stats[upgrade_attrib]:
                player.max_health += player.upgrade_exp_value[upgrade_attrib]
                player.exp -= player.upgrade_exp_cost[upgrade_attrib]
                player.upgrade_exp_cost[upgrade_attrib] += 50
                upgrade_exp_data[upgrade_attrib]['actual'] += 1

            if player.max_health > player.max_stats[upgrade_attrib]:
                player.max_health = player.max_stats[upgrade_attrib]
        
        else:
            if player.exp >= player.upgrade_exp_cost[upgrade_attrib] and player.stats[upgrade_attrib] < player.max_stats[upgrade_attrib]:
                if upgrade_attrib == 'mana':
                    player.magic_regen += 0.07
                player.stats[upgrade_attrib] += player.upgrade_exp_value[upgrade_attrib]
                player.exp -= player.upgrade_exp_cost[upgrade_attrib]
                player.upgrade_exp_cost[upgrade_attrib] += 50
                upgrade_exp_data[upgrade_attrib]['actual'] += 1

            if player.stats[upgrade_attrib] > player.max_stats[upgrade_attrib]:
                player.stats[upgrade_attrib] = player.max_stats[upgrade_attrib]

    def display(self,surface,select_nr,name,cost,amount,max_amount):
        background = UI_BG_COLOR
        border = UI_BORDER_COLOR
        if self.index == select_nr:
            background = UPGRADE_BG_COLOR_SELECTED
            
        pygame.draw.rect(surface,background,self.rect)
        pygame.draw.rect(surface,border,self.rect,4)    
        self.display_names(surface,name,cost,amount,max_amount,self.index == select_nr)