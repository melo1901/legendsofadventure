import pygame, sys
from settings import *
from level import Level

class Menu:
    def __init__(self, options, type):
        self.font = pygame.font.Font(None, 50)
        self.options = options
        self.selected_option = 0
        self.type = type

    def draw(self, screen):
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
                text_rect = text.get_rect(center=(WIDTH // 2, start_y + i * 60))
                pygame.draw.rect(screen, color, text_rect.inflate(20, 10))
                screen.blit(text, text_rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Legends of Adventure")
        self.clock = pygame.time.Clock()

        self.level = Level()
        self.pause_menu = Menu(['Resume', 'Options', 'Help', 'Exit'], "pause")
        self.title_menu = Menu(['Start', 'Options', 'Help', 'Quit'], "title")
        self.state = 'title'

    def draw_title(self):
        self.screen.fill("black")
        font = pygame.font.Font(None, 74)
        text = font.render("Legends of Adventure", 1, (255, 255, 255))
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 100))

        self.title_menu.draw(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == 'running':
                            self.state = 'menu'
                        elif self.state == 'menu':
                            self.state = 'running'
                    if self.state == 'title':
                        result = self.title_menu.handle_input(event)
                        if result == 'Start':
                            self.state = 'running'
                        elif result == 'Help':
                            print("Help")
                        elif result == 'Quit':
                            pygame.quit()
                            sys.exit()
                    elif self.state == 'menu':
                        result = self.pause_menu.handle_input(event)
                        if result == 'Resume':
                            self.state = 'running'
                        elif result == 'Help':
                            print("Help")
                        elif result == 'Exit':
                            self.state = 'title'
                    if event.key == pygame.K_m and self.state == 'running':
                        self.level.toggle_menu()
                    if event.key == pygame.K_u and self.state == 'running':
                        self.level.toggle_shop()

            if self.state == 'title':
                self.draw_title()
            elif self.state == 'running':
                self.screen.fill("black")
                self.level.run()
            elif self.state == 'menu':
                self.pause_menu.draw(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()