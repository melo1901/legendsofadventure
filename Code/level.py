import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug_text

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()
    
    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TITLESIZE
                y = row_index * TITLESIZE
                if col == 'x':
                    Tile((x,y),[self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((2000,3000),[self.visible_sprites], self.obstacle_sprites)
        #self.player = Player((2000,3000),[self.visible_sprites], self.obstacle_sprites)
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.zoom_scale = 4
        
        #podłoże
        self.floor_surf = pygame.image.load('graphics/tilemap/map.png').convert()
        
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
        self.scaled_surf = pygame.transform.scale(self.floor_surf, (self.floor_rect.width * self.zoom_scale, self.floor_rect.height * self.zoom_scale))
    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom_scale += 0.01
        if keys[pygame.K_e]:
            self.zoom_scale -= 0.01

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        floot_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.scaled_surf, floot_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image,offset_pos)

