import pygame
from enemy import Enemy
from settings import UI_FONT, UI_FONT_SIZE

class MiniBoss(Enemy):
    def __init__(self, name, pos, groups, obstacles, damage_func):
        super().__init__(name, pos, groups, obstacles, damage_func)
        self.hitbox = self.rect.inflate(-10, -10)

    def update(self):
        super().update()