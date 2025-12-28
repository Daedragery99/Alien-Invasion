import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    """The class that manges game assests and logic"""

    def __init__(self):
        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_widht = self.screen.get_rect().width
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)


    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()            
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._key_down_events(event)
                elif event.type == pygame.KEYUP:
                    self._key_up_events(event)
                    

    def _update_screen(self):
        self.screen.fill(self.settings.bg_colort)
        self.ship.blitme()

        pygame.display.flip() 
    
    def _key_down_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_KP_PLUS:
            self.settings.ship_speed += 1.5
        elif event.key == pygame.K_q:
            sys.exit()

    def _key_up_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()