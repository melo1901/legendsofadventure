import pygame
from enemy import Enemy

class MiniBoss(Enemy):
    def __init__(self, name, pos, groups, obstacles, damage_func):
        super().__init__(name, pos, groups, obstacles, damage_func)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.rect = self.image.get_rect(center=self.rect.center) 

    def update(self):
        super().update()