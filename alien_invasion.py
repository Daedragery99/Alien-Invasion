import sys
from time import sleep

import pygame

from random import randint

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from galaxy import Galaxy
from gamestat import GameStats
from explosion import Explosion
from button import Button


class AlienInvasion:
    """The class that manages game assests and logic"""

    def __init__(self):
        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        #Press play to be in an active state
        self.game_active = False

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.play_button = Button(self, "Play")
        
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_widht = self.screen.get_rect().width
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.galaxies = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self._create_fleet()
        self._create_solar_system()

        

    def run_game(self):
        while True:
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_explosions()
                self._update_aliens()          

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                    

    def _update_screen(self):
        self.screen.fill(self.settings.bg_colort)
        self.galaxies.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.explosions.draw(self.screen)

        if not self.game_active:
            self.play_button.draw_button()

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
        elif event.key == pygame.K_p:
            self._start_game()
        

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
        self._check_bullet_alien_collison()       
        
    def _check_bullet_alien_collison(self):
         #get rid of bullets and aliens if they collide
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        #make hit aliens explode
        for hit_aliens in collisions.values():
            for hit_alien in hit_aliens:
                self._make_it_explode(hit_alien)

        #respawn the fleet after they goqt cleared out
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_heigt = alien.rect.size

        current_x, current_y = alien_width, alien_heigt
        while current_y < (self.settings.screen_height - 4 * alien_heigt):
            while current_x < (self.settings.screen_widht - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += alien_heigt * 2

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        #look for enemy-player collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_alien_hit_bottom()

    def _create_galaxy(self, x_position, y_position):
        new_galaxy = Galaxy(self)
        new_galaxy.rect.x = x_position
        new_galaxy.rect.y = y_position
        self.galaxies.add(new_galaxy)

    def _create_solar_system(self): #TODO implement greater variety
        galaxy = Galaxy(self)
        galaxy_widht, galaxy_height = galaxy.rect.size

        current_x, current_y = galaxy_widht, galaxy_height
        while current_y < (self.settings.screen_height - galaxy_height):
            while current_x < (self.settings.screen_widht - galaxy_widht):
                #draw a galaxy with settings chance
                decider = randint(1,self.settings.dawing_chance)
                if decider == 1:
                    self._create_galaxy(current_x, current_y)
                current_x += 2 * galaxy_widht
            current_x = galaxy_widht
            current_y += 2 * galaxy_height

    def _ship_hit(self):

        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_alien_hit_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _update_explosions(self):
        self.explosions.update()

    def _make_it_explode(self, explode_object):
        new_exposion = Explosion(self)
        new_exposion.rect.x = explode_object.rect.x
        new_exposion.rect.y = explode_object.rect.y
        self.explosions.add(new_exposion)

    def _check_play_button(self, mousepos):
        if self.play_button.rect.collidepoint(mousepos) and not self.game_active:
           self._start_game()

    def _start_game(self):
        self.stats.reset_stats()
        self.game_active = True

        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)
            


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()