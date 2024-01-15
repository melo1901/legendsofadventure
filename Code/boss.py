from enemy import Enemy
from settings import global_settings, settings


class Boss(Enemy):
    def __init__(self, name, pos, groups, obstacles, damage_func):
        super().__init__(name, pos, groups, obstacles, damage_func)
        self.boss_killed = False
        self.hitbox = self.rect.inflate(-10, -10)

    def check_if_killed(self):
        if self.health <= 0 and self.boss_killed == False:
            self.boss_killed = True
            global_settings.miniboss_kill_count = 0
            global_settings.end_game = True

    def update(self):
        super().update()
        self.check_if_killed()
