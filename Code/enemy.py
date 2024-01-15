import pygame
from settings import *
from entity import Entity
from support import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player):
        # general setup
        super().__init__(groups)
        self.sprite_type = "enemy"

        # graphic setup
        self.import_graphics(monster_name)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info["health"]
        self.max_health = monster_info["health"]
        self.exp = monster_info["exp"]
        self.gold = monster_info["gold"]
        self.speed = monster_info["speed"]
        self.attack_damage = monster_info["damage"]
        self.resistance = monster_info["resistance"]
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]
        self.attack_type = monster_info["attack_type"]

        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 700
        self.damage_player = damage_player

        self.vulnerable = True
        self.hit_time = None
        self.invincible_duration = 200

        self.mob_hit_sound = pygame.mixer.Sound("Resources/mob_hit.wav")

    def import_graphics(self, name):
        self.animations = {"idle": [], "move": [], "attack": []}
        main_path = f"graphics/monsters/{name}/"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius:
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self, player):
        if self.status == "attack":
            self.damage_player(damage=self.attack_damage, attack_type=self.attack_type)
        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        # self.rect = self.image.get_rect(center = self.hitbox.center)
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincible_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == "weapon":
                damage = player.get_full_weapon_damage()
                self.mob_hit_sound.play()
            elif attack_type == "magic":
                damage = player.get_full_magic_damage()
                self.mob_hit_sound.play()
            else:
                damage = 0

            self.health -= damage
            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()

    def check_death(self, player):
        if self.health <= 0:
            self.kill()
            player.exp += self.exp
            player.gold += self.gold

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def collision(self, direction, speed):
        future_rect = self.rect.copy()
        if direction == "horizontal":
            future_rect.x += self.direction.x * speed
        else:
            future_rect.y += self.direction.y * speed

        for sprite in self.obstacle_sprites:
            if future_rect.colliderect(sprite.rect):
                return True

        return False

    def move(self, player):
        max_distance = 500
        distance, _ = self.get_player_distance_direction(player)

        if distance <= max_distance:
            if not self.collision("horizontal", self.speed):
                self.rect.x += self.direction.x * self.speed

            if not self.collision("vertical", self.speed):
                self.rect.y += self.direction.y * self.speed

    def update(self):
        self.animate()
        self.cooldowns()
        self.mob_hit_sound.set_volume(settings["sound_volume"])

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        self.check_death(player)
        self.hit_reaction()
        self.move(player)
