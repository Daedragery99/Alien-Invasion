import pygame
from pygame.sprite import Sprite
from random import randint

class Galaxy(Sprite):
    """Class that holds the backround galaxys"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen

        decider = randint(0,1)
        if decider == 0:
            self.image = pygame.image.load('C:\\Users\\Gergo\\Desktop\\Python\\Alien Invasion\\images\\galaxy_2.png')
        elif decider == 1:
            self.image = pygame.image.load('C:\\Users\\Gergo\\Desktop\\Python\\Alien Invasion\\images\\galaxy_4.png')

        angle = randint(0,3) * 90
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height