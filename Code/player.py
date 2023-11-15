import pygame
from pygame.sprite import Group
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
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

        self.attacking = False
        self.attack_time = None
        self.attack_cooldown = 400
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        self.weapon_index = 1
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

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

        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()

        if keys[pygame.K_q] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            
            if self.weapon_index < len(list(weapon_data.keys())) - 1:
                self.weapon_index += 1
            else:
                self.weapon_index = 0
                
            self.weapon = list(weapon_data.keys())[self.weapon_index]

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

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

    def move(self, speed):
        if self.attacking:
            return
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        if not self.collision("horizontal", speed):
            self.rect.x += self.direction.x * speed
        if not self.collision("vertical", speed):
            self.rect.y += self.direction.y * speed

    def update(self):
        self.input()
        self.cooldowns()
        self.move(self.speed)
