import pygame
from pygame.sprite import Group
from settings import *
from support import import_folder
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load(
            "graphics/character/main_char.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.hitbox = self.rect.inflate(-8, -26)

        #graphics setup
        self.import_player_assets()
        self.status = 'down'
        
        self.obstacle_sprites = obstacle_sprites

        #stats
        self.stats = {'health' : 100, 'attack': 10,'mana': 75, 'magic': 10, 'speed': 5}
        self.max_stats = {'health' : 400, 'attack': 40,'mana': 300, 'magic': 40, 'speed': 8}
        self.upgrade_exp_cost = {'health' : 100, 'attack' : 100, 'mana' : 100, 'magic' : 100, 'speed' : 100}
        self.upgrade_exp_value = {'health' : 100, 'attack' : 10, 'mana' : 75, 'magic' : 10, 'speed' : 1}
        self.upgrade_gold_names = {'sword damage', 'axe damage', 'heal', 'flame damage', 'flame range'}
        self.upgrade_gold_cost = {'sword' : 5, 'axe' : 5, 'heal' : 5, 'flame_damage' : 5, 'flame_range' : 10}
        self.max_health = self.stats['health']
        self.health = self.stats['health']
        self.target_health = self.stats['health']
        self.mana = self.stats['mana']
        self.exp = 500
        self.speed = self.stats['speed']
        self.money = 5

        self.vulnerable = True
        self.hit_time = None
        self.invulnerability_duration = 200

        self.attacking = False
        self.attack_time = None
        self.attack_cooldown = 400
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        # weapon
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # magic
        self.create_magic = create_magic
        self.magic_index = 1
        self.magic_range = 3
        self.max_magic_range = 6
        self.magic_regen = 0.02
        self.max_magic_regen = 0.05
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.magic_casted = False

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [], 'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()


        # magic input
        if keys[pygame.K_LCTRL] and not self.magic_casted:
            self.attacking = True
            self.magic_casted = True
            self.attack_time = pygame.time.get_ticks()
            style = list(magic_data.keys())[self.magic_index]
            strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
            cost = list(magic_data.values())[self.magic_index]['cost']
            self.create_magic(style,strength,cost)

        if keys[pygame.K_q] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            
            if self.weapon_index < len(list(weapon_data.keys())) - 1:
                self.weapon_index += 1
            else:
                self.weapon_index = 0
                
            self.weapon = list(weapon_data.keys())[self.weapon_index]

        if keys[pygame.K_e] and self.can_switch_magic:
            self.can_switch_magic = False
            self.magic_switch_time = pygame.time.get_ticks()
            
            if self.magic_index < len(list(magic_data.keys())) - 1:
                self.magic_index += 1
            else:
                self.magic_index = 0
                
            self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')      

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
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if self.magic_casted and current_time - self.attack_time >= self.attack_cooldown:
            self.magic_casted = False  # Zresetuj zmienną magic_casted

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invulnerability_duration:
                self.vulnerable = True

    def move(self, speed):
        if self.attacking:
            return
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        if not self.collision("horizontal", speed):
            self.rect.x += self.direction.x * speed
        if not self.collision("vertical", speed):
            self.rect.y += self.direction.y * speed

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

    def get_full_weapon_damage(self):
        return self.stats['attack'] + weapon_data[self.weapon]['damage']
    
    def get_full_magic_damage(self):
        return magic_data[self.magic]['damage'] + self.stats['magic']

    def get_value_by_index(self,index):
        return list(self.stats.values())[index]

    def get_exp_cost_by_index(self,index):
        return list(self.upgrade_exp_cost.values())[index]
    
    def get_gold_cost_by_index(self,index):
        pass

    def energy_recovery(self):
        if self.mana < self.stats['mana']:
            self.mana += self.magic_regen
        else:
            self.mana = self.stats['mana']

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()
