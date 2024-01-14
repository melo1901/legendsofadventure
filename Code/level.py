import pygame
from settings import *
from tile import Tile
from player import Player
from weapon import Weapon
from debug import debug_text
from support import *
from ui import UI
from particles import AnimationPlayer
from magic import MagicPlayer
from enemy import Enemy
from miniboss import MiniBoss
from upgrade import Upgrade, Shop
from convert import generate_mobs_position

# Inicjalizacja klasy odpowiedzialnej za generowanie poziomu gry
class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.game_paused = False
        self.game_shop_paused = False

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Grupy sprite'ów związane z walką
        self.current_attack = None  # Aktualny atak gracza
        self.attack_sprites = pygame.sprite.Group()  # Grupa sprite'ów związanych z atakiem
        self.attackable_sprites = pygame.sprite.Group()  # Grupa sprite'ów, które można zaatakować

        self.create_map()

        # interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        self.shop = Shop(self.player)

        # particle
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        self.player_hit_sound = pygame.mixer.Sound(sounds["player_hit"])

    def create_map(self):
        generate_mobs_position()
        layouts = {
            "boundary": import_csv_layout("level/level_data/map_boundaries.csv"),
            "desert_elements": import_csv_layout(
                "level/level_data/map_desert_elements.csv"
            ),
            "forest_elements": import_csv_layout(
                "level/level_data/map_forest_elements.csv"
            ),
            "swamp_elements": import_csv_layout(
                "level/level_data/map_swamp_elements.csv"
            ),
            "tundra_elements": import_csv_layout(
                "level/level_data/map_tundra_elements.csv"
            ),
            "entities": import_csv_layout("level/level_data/map_enemiesmodified2.csv"),
        }
        resource = create_graphics_dict()

        # Pętla przeglądająca elementy mapy i tworząca odpowiednie obiekty
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites], "invisible")
                        
                        # Tworzenie przeciówników (Enemy)
                        if style == "entities":
                            if col == "68":
                                monster_name = "fire"
                            elif col == "38":
                                monster_name = "ghost"
                            elif col == "41":
                                monster_name = "bee"
                            elif col == "99":
                                monster_name = "miniboss"
                            else:
                                monster_name = None
                            if monster_name != "miniboss" and monster_name is not None:
                                # Stworzenie obiektu klasy Enemy
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                )
                            elif monster_name == "miniboss":
                                # Stworzenie obiektu klasy MiniBoss
                                MiniBoss(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                )               
                        else:
                            if style in resource:
                                resource_index = int(col)
                                if 0 <= resource_index < len(resource[style]):
                                    surf = resource[style][resource_index]
                                    Tile(
                                        (x, y),
                                        [self.visible_sprites, self.obstacle_sprites],
                                        "object",
                                        surf,
                                    )
                    if col == "p":
                        self.player = Player(
                            (1374, 4187),
                            [self.visible_sprites],
                            self.obstacle_sprites,
                            self.create_attack,
                            self.destroy_attack,
                            self.create_magic,
                        )
        self.player = Player(
            (1374, 4187),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.create_attack,
            self.destroy_attack,
            self.create_magic,
        )

    # Tworzenie ataku gracza na warstwie poziomu
    def create_attack(self):
        # Przypisanie do zmiennej obiektu klasy Weapon
        self.current_attack = Weapon(
            self.player, [self.visible_sprites, self.attack_sprites]
        )
    # Tworzenie zaklęcia (Leczenie lub Płomień)
    def create_magic(self, style, strength, cost):
        if style == "heal":
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == "flame":
            self.magic_player.flame(
                self.player, cost, [self.visible_sprites, self.attack_sprites]
            )
    # Niszczenie aktualnego ataku gracza
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    # Obsługa logiki ataku gracza - sprawdzanie kolizji z przeciwnikami
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False
                )
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player, attack_sprite.sprite_type)
    # Obsługa zdarzenia otrzymania obrażeń
    def damage_player(self, damage, attack_type):
        if self.player.vulnerable:
            if self.player.target_health >= damage:
                self.player.target_health -= damage
                pygame.mixer.Sound.play(self.player_hit_sound)
            else:
                self.player.target_health = 0
            self.player.vulnerable = False
            self.player.hit_time = pygame.time.get_ticks()

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def toggle_shop(self):
        self.game_shop_paused = not self.game_shop_paused

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        
        self.player_hit_sound.set_volume(settings["sound_volume"])
        if self.game_paused:
            self.upgrade.display()
            # display upgrade menu

        elif self.game_shop_paused:
            self.shop.display()

        else:
            # run the game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.zoom_scale = 4

        # podłoże
        self.floor_surf = pygame.image.load("graphics/tilemap/map.png").convert()

        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
        self.scaled_surf = pygame.transform.scale(
            self.floor_surf,
            (
                self.floor_rect.width * self.zoom_scale,
                self.floor_rect.height * self.zoom_scale,
            ),
        )

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floot_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.scaled_surf, floot_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

            if hasattr(sprite, "monster_name"):
                if sprite.health != sprite.max_health:
                    # Pasek zdrowia
                    health_bar_length = 50
                    health_bar_height = 7
                    health_ratio = sprite.health / sprite.max_health
                    filled_health = health_bar_length * health_ratio
                    health_bar_color = (255, 0, 0)  # Zielony kolor paska zdrowia
                    pygame.draw.rect(
                        self.display_surface,
                        health_bar_color,
                        (
                            offset_pos[0],
                            offset_pos[1] - 25,
                            filled_health,
                            health_bar_height,
                        ),
                    )
                    pygame.draw.rect(
                        self.display_surface,
                        (0, 0, 0),
                        (
                            offset_pos[0] + filled_health,
                            offset_pos[1] - 25,
                            health_bar_length - filled_health,
                            health_bar_height,
                        ),
                    )
    # Aktuallizacja statusu przeciwnika
    def enemy_update(self, player):
        enemy_sprites = [
            sprite
            for sprite in self.sprites()
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"
        ]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
