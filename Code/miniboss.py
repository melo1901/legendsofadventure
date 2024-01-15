import pygame
from enemy import Enemy
from settings import global_settings

class MiniBoss(Enemy):
    def __init__(self, name, pos, groups, obstacles, damage_func):
        super().__init__(name, pos, groups, obstacles, damage_func)
        self.hitbox = self.rect.inflate(-10, -10)
        self.miniboss_killed = False
        self.rect = pygame.transform.scale(self.image, (self.rect.width * 0.9, self.rect.height * 0.9)).get_rect(topleft=pos)

    def check_if_killed(self):
        global miniboss_kill_count
        if self.health <= 0 and self.miniboss_killed == False:
            self.miniboss_killed = True
            global_settings.miniboss_kill_count += 1

    def update(self):
        super().update()
        self.check_if_killed()