import pygame
import sys
from settings import *
from level import Level
import pygame_gui

class HelpScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.lines = [
            "WASD - Poruszanie się",
            "Spacja - Uderzenie",
            "Lewy CTRL - Użycie Magii",
            "E - Zmiana zaklęcia",
            "Q - Zmiana broni",
            "ESC - Wyjście",
            "U - Sklep",
            "M - Ulepszanie Zaklęć" 
        ]
        self.image = pygame.image.load("graphics/ui_elem/Instrukcja.png").convert_alpha()

    def draw(self, screen):
        # Ładowanie obrazu tła z przezroczystością (PNG z kanałem alfa)
        background_image = pygame.image.load("graphics/ui_elem/background.jpg").convert_alpha()
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

# NOWE OPTIONS
class OptionsScreen:
    def __init__(self, manager, clock):
        self.font = pygame.font.Font(None, 36)
        self.lines = [
            "Witaj w",
            "Legends of Adventure!",
            "",
            "Instrukcja gry:",
            "",
            "   - W : Idź w górę",
            "   - A : Idź w lewo",
            "   - S  : Idź w dół",
            "   - D : Idź w prawo",
            "   - Esc: Pauza/Menu",
            "   - M: Otwórz sklep",
            "   - U: Ulepsz magię",
            "   - Q: Quit game",
            "",
            "Miłej zabawy!",
        ]

        # Inicjalizacja managera GUI
        self.manager = manager

        # Przekazanie zegara
        self.clock = clock

        # Tworzenie suwaka do regulacji głośności muzyki
        self.music_volume_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
            pygame.Rect((WIDTH // 4, HEIGHT // 2), (300, 20)),
            start_value=pygame.mixer.music.get_volume(),
            value_range=(0, 1),
            manager=self.manager
        )

    def draw(self, screen):
        # Ładowanie obrazu tła z przezroczystością (PNG z kanałem alfa)
        background_image = pygame.image.load("graphics/ui_elem/background.jpg").convert_alpha()
        screen.blit(background_image, (0, 0))

        y = HEIGHT // 4
        for line in self.lines:
            text = self.font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, y))
            screen.blit(text, text_rect)
            y += 30

        # Aktualizacja i rysowanie elementów GUI
        self.manager.update(self.clock.tick(FPS) / 1000.0)
        self.manager.draw_ui(screen)

class Menu:
    def __init__(self, options, type):
        self.font = pygame.font.Font(None, 50)
        self.options = options
        self.selected_option = 0
        self.type = type
        self.background_image = pygame.image.load("graphics/ui_elem/background.jpg")  # Ścieżka do obrazu tła menu
        self.logo_image = pygame.image.load("graphics/ui_elem/logo.png")  # Ścieżka do obrazu logo

    def draw(self, screen):
        # Rysowanie tła
        screen.blit(self.background_image, (0, 0))

        # Rysowanie logo na środku ekranu
        logo_rect = self.logo_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(self.logo_image, logo_rect)

        for i, option in enumerate(self.options):
            color = (160, 160, 160) if i == self.selected_option else (100, 100, 100)
            text = self.font.render(option, 1, (255, 255, 255))

            if self.type == "title":
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
                pygame.draw.rect(screen, color, text_rect.inflate(20, 10))
                screen.blit(text, text_rect)
            elif self.type == "pause":
                total_height = len(self.options) * 60
                start_y = HEIGHT // 2 - total_height // 2
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
                pygame.draw.rect(screen, color, text_rect.inflate(20, 10))
                screen.blit(text, text_rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.options[self.selected_option] == "Options":
                    print("Options")
                    return "Options"
                elif self.options[self.selected_option] == "Help":
                    print("Help")
                    return "Help"
                else:
                    return self.options[self.selected_option]
            elif event.key == pygame.K_ESCAPE:
                return "Escape"

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("Resources/background.wav")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Legends of Adventure")
        self.clock = pygame.time.Clock()

        self.level = Level()
        self.pause_menu = Menu(["Resume", "Options", "Help", "Exit"], "pause")
        self.title_menu = Menu(["Start", "Options", "Help", "Quit"], "title")
        self.state = "title"
        self.options_screen = OptionsScreen(pygame_gui.UIManager((WIDTH, HEIGHT)), self.clock)
        self.help_screen = HelpScreen()

    def draw_title(self):
        # Rysowanie tła
        self.screen.blit(self.title_menu.background_image, (0, 0))

        self.title_menu.draw(self.screen)

    def draw_options(self):
        # Rysowanie tła
        self.screen.blit(self.pause_menu.background_image, (0, 0))

        self.pause_menu.draw(self.screen)

        # Rysowanie ekranu opcji
        #self.options_screen.draw(self.screen)

    def draw_help(self):
        # Rysowanie tła
        self.screen.blit(self.pause_menu.background_image, (0, 0))

        self.help_screen.draw(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "running":
                            self.state = "menu"
                        elif self.state == "menu" or self.state == "options" or self.state == "help":
                            self.state = self.previous_state
                            if self.state == "title":
                                self.level = Level()
                    if self.state == "title":
                        result = self.title_menu.handle_input(event)
                        if result == "Start":
                            self.state = "running"
                        elif result == "Options":
                            self.previous_state = "title"
                            self.state = "options"
                        elif result == "Help":
                            self.previous_state = "title"
                            self.state = "help"
                        elif result == "Quit":
                            pygame.quit()
                            sys.exit()
                    elif self.state == "menu":
                        result = self.pause_menu.handle_input(event)
                        if result == "Resume":
                            self.state = "running"
                        elif result == "Options":
                            self.previous_state = "menu"
                            self.state = "options"
                        elif result == "Help":
                            self.previous_state = "menu"
                            self.state = "help"
                        elif result == "Exit":
                            self.state = "title"
                            self.level = Level()
                    elif self.state == "options":
                        if result == "Escape":
                            self.state = self.previous_state
                    elif self.state == "help":
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
            elif self.state == "menu":
                self.draw_options()
            elif self.state == "options":
                self.options_screen.draw(self.screen)
            elif self.state == "help":
                self.draw_help()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
