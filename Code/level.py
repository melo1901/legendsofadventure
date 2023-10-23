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
                    self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites)

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
        self.zoom_scale = 1
        self.internal_surf_size = (2500, 2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center = (self.half_width, self.half_width))
        self.internal_surf_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_width
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_height

        #podłoże

        self.floor_surf = pygame.image.load('graphics/tilemap/map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom_scale += 0.01
        if keys[pygame.K_e]:
            self.zoom_scale -= 0.01

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        self.zoom_keyboard_control()
        self.internal_surf.fill('#71ddee')

        #rysowanie podłoża
        floot_offset_pos = self.floor_rect.topleft - self.offset + self.internal_offset
        self.internal_surf.blit(self.floor_surf, floot_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf,self.internal_surf_size_vector * self.zoom_scale)    
        scaled_rect = scaled_surf.get_rect(center = (self.half_width, self.half_height))

        self.display_surface.blit(scaled_surf, scaled_rect)

