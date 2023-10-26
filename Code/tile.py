import pygame
from pygame.sprite import Group
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale(pygame.image.load('graphics/character/main.png').convert_alpha(), (64, 64))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
