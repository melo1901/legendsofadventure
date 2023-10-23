import pygame
from pygame.sprite import _Group
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super.__init__(groups)
        self.image = pygame.image.load('graphics/regions/cave_/cave_ [fountain].png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
