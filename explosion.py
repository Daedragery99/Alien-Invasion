import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """Class that governs explosion class"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.index = 0

        self.image = pygame.image.load('C:\\Users\\Gergo\\Desktop\\Python\\Alien Invasion\\images\\explosion\\exp_0.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def update(self):
        if self.index <= 14:
            self.index += 1
            self.image = pygame.image.load(f'C:\\Users\\Gergo\\Desktop\\Python\\Alien Invasion\\images\\explosion\\exp_{self.index}.png')
        else:
            self.kill()