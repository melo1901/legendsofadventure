import pygame
from pygame.sprite import Group
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        surface = pygame.transform.scale(surface, (TILESIZE, TILESIZE))
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(surface)
        self.mask_rect = self.mask.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-10, -10)
