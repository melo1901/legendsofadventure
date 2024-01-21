""" Główny plik wykonywalny gry "Legends of Adventure"
    Celem gry jest pokonanie głównego przeciwnika, znajdującego się w lewym, górnym rogu mapy.
    Aby mieć możliowść starcia z głównym bossem trzeba najpierwiej pokonać jego popleczników.
    Poplecznicy znajdują się w pozostałych rejonach mapy i znacząco różnią się od podstawowych przeciwników
    Walcz, nabieraj doświadczenia i rozwijaj swoje umiejętności, aby zostać prawdziwą Legendą Przygody!
"""
import pygame
import sys
from settings import *
from level import Level
import pygame_gui
import time


class HelpScreen:
    def __init__(self):
        self.font = pygame.font.Font("graphics/fonts/prstartk.ttf", 16)
        self.lines = [
            "WASD - Move",
            "Spacebar - Hit",
            "Left CTRL - Use Magic",
            "E - Change Spell",
            "Q - Change Weapon",
            "ESC - Exit / Menu",
            "U - Shop",
            "M - Enhance Skills" 
        ]
        self.image = pygame.image.load("graphics/ui_elem/Instrukcja.png").convert_alpha()

    def draw(self, screen):
        # Ładowanie obrazu tła z przezroczystością (PNG z kanałem alfa)
        background_image = pygame.image.load(
            "graphics/ui_elem/background.jpg"
        ).convert_alpha()
        screen.blit(background_image, (0, 0))

        # Rysowanie obrazka nad tekstem
        image_rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(self.image, image_rect)

        # Rysowanie tekstu
        y = HEIGHT // 1.7
        for line in self.lines:
            text = self.font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, y))
            screen.blit(text, text_rect)
            y += 30


# NOWE mission
class missionScreen:
    def __init__(self):
        self.font = pygame.font.Font("graphics/fonts/prstartk.ttf", 16)
        self.lines = [
            "What is your mission",
            "in Legends of Adventure?",
            "",
            "KILL THE FINAL BOSS AND FINISH THE GAME!",
            "",
            "Earn Experience and Money by killing enemies,",
            "Upgrade your abilities and Strength,",
            "this will help you to defeat the Devil!",
            "",
            "Maybe you will become the Legend of Adventure?",
            "",
            "Good Luck!"
        ]
        self.image = pygame.image.load("graphics/ui_elem/cel.png").convert_alpha()

    def draw(self, screen):
        # Ładowanie obrazu tła z przezroczystością (PNG z kanałem alfa)
        background_image = pygame.image.load(
            "graphics/ui_elem/background.jpg"
        ).convert_alpha()
        screen.blit(background_image, (0, 0))

        # Rysowanie obrazka nad tekstem
        image_rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(self.image, image_rect)

        # Rysowanie tekstu
        y = HEIGHT // 2.5
        for line in self.lines:
            text = self.font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, y))
            screen.blit(text, text_rect)
            y += 30

        
class Menu:
    def __init__(self, mission, type):
        self.font = pygame.font.Font("graphics/fonts/prstartk.ttf", 22)
        self.mission = mission
        self.selected_option = 0
        self.type = type
        self.background_image = pygame.image.load(
            "graphics/ui_elem/background.jpg"
        )  # Ścieżka do obrazu tła menu
        self.logo_image = pygame.image.load(
            "graphics/ui_elem/logo.png"
        )  # Ścieżka do obrazu logo

    def draw(self, screen):
        # Rysowanie tła
        screen.blit(self.background_image, (0, 0))

        # Rysowanie logo na środku ekranu
        logo_rect = self.logo_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(self.logo_image, logo_rect)

        for i, option in enumerate(self.mission):
            color = (240, 163, 53) if i == self.selected_option else (81, 53, 32)
            text = self.font.render(option, 1, (255, 255, 255))

            if self.type == "title":
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
                pygame.draw.rect(screen, color, text_rect.inflate(20, 10))
                screen.blit(text, text_rect)
            elif self.type == "pause":
                total_height = len(self.mission) * 60
                start_y = HEIGHT // 2 - total_height // 2
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
                pygame.draw.rect(screen, color, text_rect.inflate(20, 10))
                screen.blit(text, text_rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.mission)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.mission)
            elif event.key == pygame.K_RETURN:
                if self.mission[self.selected_option] == "Mission":
                    print("Mission")
                    return "Mission"
                elif self.mission[self.selected_option] == "Help":
                    print("Help")
                    return "Help"
                else:
                    return self.mission[self.selected_option]
            elif event.key == pygame.K_ESCAPE:
                return "Escape"


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("Resources/background.wav")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Legends of Adventure")
        self.clock = pygame.time.Clock()

        self.level = Level()
        self.pause_menu = Menu(["Resume", "Mission", "Help", "Exit"], "pause")
        self.title_menu = Menu(["Start", "Mission", "Help", "Quit"], "title")
        self.state = "title"
        self.mission_screen = missionScreen()
        self.help_screen = HelpScreen()
        self.start_time = None
        self.end_time = None
        self.font = pygame.font.Font(UPGRADE_UI_FONT, 22)
        self.boss_spawn_message_time = None

    def draw_text_with_outline(self, text, font, color, outline_color, x, y):
        outline = font.render(text, True, outline_color)
        for dx, dy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            self.screen.blit(outline, (x + dx, y + dy))
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def draw_title(self):
        # Rysowanie tła
        self.screen.blit(self.title_menu.background_image, (0, 0))

        self.title_menu.draw(self.screen)

    def draw_mission(self):
        # Rysowanie tła
        self.screen.blit(self.pause_menu.background_image, (0, 0))


        self.mission_screen.draw(self.screen)
        #self.pause_menu.draw(self.screen)
    
    def draw_menu(self):
        # Rysowanie tła
        self.screen.blit(self.pause_menu.background_image, (0, 0))

        self.pause_menu.draw(self.screen)

    def draw_help(self):
        # Rysowanie tła
        self.screen.blit(self.pause_menu.background_image, (0, 0))

        self.help_screen.draw(self.screen)

    def run(self):
        while True:
            if pygame.mouse.get_focused():
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
            pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "running":
                            self.state = "menu"
                        elif (
                            self.state == "menu"
                            or self.state == "mission"
                            or self.state == "help"
                        ):
                            self.state = self.previous_state
                    if self.state == "title":
                        result = self.title_menu.handle_input(event)
                        if result == "Start":
                            self.state = "running"
                            global_settings.miniboss_kill_count = 0
                            global_settings.boss_alive = False
                            global_settings.end_game = False
                            global_settings.boss_spawn_message = False
                            self.boss_spawn_message_time = None
                            global_settings.player_dead == False
                            self.start_time = time.time()
                            self.level = Level()
                        elif result == "Help":
                            self.previous_state = "title"
                            self.state = "help"
                        elif result == "Mission":
                            self.previous_state = "title"
                            self.state = "mission"
                        elif result == "Quit":
                            pygame.quit()
                            sys.exit()
                    elif self.state == "menu":
                        result = self.pause_menu.handle_input(event)
                        if result == "Resume":
                            self.state = "running"
                        elif result == "Help":
                            self.previous_state = "menu"
                            self.state = "help"
                        elif result == "Mission":
                            self.previous_state = "menu"
                            self.state = "mission"
                        elif result == "Exit":
                            self.state = "title"
                            self.level = Level()
                    elif self.state == "help":
                        if result == "Escape":
                            self.state = self.previous_state
                    elif self.state == "mission":
                        if result == "Escape":
                            self.state = self.previous_state
                    if event.key == pygame.K_m and self.state == "running":
                        self.level.toggle_menu()
                    if event.key == pygame.K_u and self.state == "running":
                        self.level.toggle_shop()

            if self.state == "title":
                self.draw_title()
            elif self.state == "running":
                self.screen.fill(WATER_COLOR)
                self.level.run()
                if global_settings.end_game == True:
                    self.state = "end_game"
                    if self.end_time is None:
                        self.end_time = time.time()
                    elapsed_time = round(self.end_time - self.start_time, 4)

                    time_text = f"Time of run: {elapsed_time} seconds"
                    instruction_text = "Press Enter to continue"
                    text_width, text_height = self.font.size(time_text)

                    x = (WIDTH - text_width) / 2
                    y = (HEIGHT - text_height) / 2

                    self.draw_text_with_outline(
                        time_text, self.font, (255, 255, 255), (0, 0, 0), x, y - 25
                    )
                    self.draw_text_with_outline(
                        instruction_text,
                        self.font,
                        (255, 255, 255),
                        (0, 0, 0),
                        x,
                        y + 25,
                    )

                    pygame.display.update()
                elif global_settings.player_dead == True:
                    self.state = "you_died"
                    font = pygame.font.Font(UPGRADE_UI_FONT, 50)
                    death_text = font.render(f"YOU DIED", True, (255, 0, 0))
                    continue_text = self.font.render(
                        f"Press Enter to continue", True, (255, 255, 255)
                    )
                    text_width, text_height = death_text.get_size()

                    x = (WIDTH - text_width) / 2
                    y = (HEIGHT - text_height) / 3

                    self.screen.blit(death_text, (x, y))
                    self.screen.blit(continue_text, (x, y + 100))

                    pygame.display.update()

            elif self.state == "menu":
                self.draw_menu()
            elif self.state == "help":
                self.draw_help()
            elif self.state == "mission":
                self.draw_mission()
            elif self.state == "end_game":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    self.state = "title"
                    global_settings.end_game = False
                    self.end_time = None
            elif self.state == "you_died":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    self.state = "title"
                    global_settings.end_game = False
                    global_settings.player_dead = False

            if (
                global_settings.miniboss_kill_count == 2
                and global_settings.boss_spawn_message == False
            ):
                if self.boss_spawn_message_time == None:
                    self.boss_spawn_message_time = time.time()
                if time.time() - self.boss_spawn_message_time <= 3:
                    boss_spawn_text = self.font.render(
                        "Boss is coming!", True, (255, 0, 0)
                    )
                    text_width, text_height = boss_spawn_text.get_size()

                    x = (WIDTH - text_width) / 2
                    y = (HEIGHT - text_height) / 3

                    self.screen.blit(boss_spawn_text, (x, y))

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
