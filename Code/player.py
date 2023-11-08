import pygame
from pygame.sprite import Group
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/character/main_char.png.').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_rect = self.mask.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-8, -26)

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

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

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #kolizja z prawej
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #kolizja z lewej
                        self.hitbox.left = sprite.hitbox.right
                    
        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #kolizja z prawej
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #kolizja z lewej
                        self.hitbox.top = sprite.hitbox.bottom

    # def collision(self, direction):
    #     if direction == "horizontal":
    #         for sprite in self.obstacle_sprites:
    #             if pygame.sprite.collide_mask(self, sprite):
    #                 if self.direction.x > 0:  # kolizja z prawej
    #                     self.hitbox.right = sprite.hitbox.left
    #                 if self.direction.x < 0:  # kolizja z lewej
    #                     self.hitbox.left = sprite.hitbox.right

    #     if direction == "vertical":
    #         for sprite in self.obstacle_sprites:
    #             if pygame.sprite.collide_mask(self, sprite):
    #                 if self.direction.y > 0:  # kolizja z dolu
    #                     self.hitbox.bottom = sprite.hitbox.top
    #                 if self.direction.y < 0:  # kolizja z gory
    #                     self.hitbox.top = sprite.hitbox.bottom


    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
        

    def update(self):
        self.input()
        self.move(self.speed)
        
