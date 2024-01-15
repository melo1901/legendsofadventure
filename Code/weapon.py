import pygame

# Deklaracja klasy Weapon
class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups) -> None:
        super().__init__(groups)
        self.sprite_type = "weapon"
        direction_mapping = {
            (1, 0): "right",
            (-1, 0): "left",
            (0, 1): "down",
            (0, -1): "up",
        }
        direction = direction_mapping.get(
            (player.direction.x, player.direction.y),
            player.status.replace("_attack", "").replace("_idle", ""),
        )

        full_path = f"./graphics/weapons/{player.weapon}/{direction}.png"
        self.image = pygame.image.load(full_path)
        self.image.set_colorkey((255, 255, 255))
        self.image.convert_alpha()

        if direction == "right":
            self.rect = self.image.get_rect(
                midleft=player.rect.midright + pygame.math.Vector2(0, 16)
            )
        elif direction == "left":
            self.rect = self.image.get_rect(
                midright=player.rect.midleft + pygame.math.Vector2(0, 16)
            )
        elif direction == "down":
            self.rect = self.image.get_rect(
                midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0)
            )
        else:
            self.rect = self.image.get_rect(
                midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0)
            )
