import pygame
from subprocess import run
import os

display_width = 450
display_height = 300

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

bg_location = 'D:/Desktop/pygame/game_menu/images/background2.jpg'

pygame.init()

class Button(object):
    def __init__(self, text, color, x=None, y=None, **kwargs):
        self.surface = font.render(text, True, color)

        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()

        if 'centered_x' in kwargs and kwargs['centered_x']:
            self.x = display_width // 2 - self.WIDTH // 2
        else:
            self.x = x

        if 'centered_y' in kwargs and kwargs['cenntered_y']:
            self.y = display_height // 2 - self.HEIGHT // 2
        else:
            self.y = y

    def display(self):
        screen.blit(self.surface, (self.x, self.y))

    def check_click(self, position):
        x_match = self.x < position[0] < self.x + self.WIDTH
        y_match = self.y < position[1] < self.y + self.HEIGHT

        if x_match and y_match:
            return True
        else:
            return False


def starting_screen():
    screen.blit(bg, (0, 0))

    game_title = font1.render('Game Menu', True, BLACK)

    screen.blit(game_title, (display_width // 2 - game_title.get_width() // 2, 50))

    Airplane_button = Button('Airplane', WHITE, None, 150, centered_x=True)
    Dragon_button = Button('Dragon', WHITE, None, 200, centered_x=True)
    Quit_button = Button('Quit', WHITE, None, 250, centered_x=True)

    Airplane_button.display()
    Dragon_button.display()
    Quit_button.display()

    pygame.display.update()

    while True:

        if Airplane_button.check_click(pygame.mouse.get_pos()):
            Airplane_button = Button('Airplane', RED, None, 150, centered_x=True)
        else:
            Airplane_button = Button('Airplane', WHITE, None, 150, centered_x=True)

        if Dragon_button.check_click(pygame.mouse.get_pos()):
            Dragon_button = Button('Dragon', RED, None, 200, centered_x=True)
        else:
            Dragon_button = Button('Dragon', WHITE, None, 200, centered_x=True)

        if Quit_button.check_click(pygame.mouse.get_pos()):
            Quit_button = Button('Quit', RED, None, 250, centered_x=True)
        else:
            Quit_button = Button('Quit', WHITE, None, 250, centered_x=True)

        Airplane_button.display()
        Dragon_button.display()
        Quit_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        if pygame.mouse.get_pressed()[0]:
            if Airplane_button.check_click(pygame.mouse.get_pos()):
                # run("python D:\\Desktop\\pygame\\Airplane\\6game.py", shell=True)
                os.system("D:\\Desktop\\pygame\\game_menu\\Airplane.exe")
            if Dragon_button.check_click(pygame.mouse.get_pos()):
                # run("python D:\\Desktop\\pygame\\Dragon\\5game.py", shell=True)
                os.system("D:\\Desktop\\pygame\\game_menu\\Dragon.exe")
            if Quit_button.check_click(pygame.mouse.get_pos()):
                break


screen = pygame.display.set_mode((display_width, display_height))
bg = pygame.image.load(bg_location)
# font_addr = pygame.font.get_default_font()
font = pygame.font.Font(None, 40)
font1 = pygame.font.Font(None, 50)

starting_screen()
