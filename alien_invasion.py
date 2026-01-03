import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """The class that manages game assests and logic"""

    def __init__(self):
        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_widht = self.screen.get_rect().width
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()


    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()          
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
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
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
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _key_up_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()

        #get rid of bullets that escape the frame
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            #print(len(self.bullets))



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()