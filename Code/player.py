import pygame
from pygame.sprite import Group
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(
            "graphics/character/main_char.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.hitbox = self.rect.inflate(-8, -26)

        self.direction = pygame.math.Vector2()

        self.obstacle_sprites = obstacle_sprites

        #stats
        self.stats = {'health' : 100, 'stamina': 75, 'attack': 10,'mana': 50, 'speed': 5}
        self.health = self.stats['health']
        self.stamina = self.stats['stamina']
        self.exp = 150
        self.speed = self.stats['speed']
        self.money = 5

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def collision(self, direction, speed):
        future_rect = self.rect.copy()
        if direction == "horizontal":
            future_rect.x += self.direction.x * speed
        else:
            future_rect.y += self.direction.y * speed

        for sprite in self.obstacle_sprites:
            offset_x = sprite.rect.x - future_rect.x
            offset_y = sprite.rect.y - future_rect.y
            if self.mask.overlap(sprite.mask, (offset_x, offset_y)):
                return True
        return False

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        if not self.collision("horizontal", speed):
            self.rect.x += self.direction.x * speed
        if not self.collision("vertical", speed):
            self.rect.y += self.direction.y * speed

    def update(self):
        self.input()
        self.move(self.speed)
