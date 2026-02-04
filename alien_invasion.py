"""alien_invasion game
Python Crash Course chapters 12 - 14
Creating a 2D game using python and pygame
"""
# import packages
import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from projectile import Projectile
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((1200, 800))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game stats
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.projectiles = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an active state
        self.game_active = True


    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_projectiles()
                self._update_aliens()
                self._update_screen()
                self.clock.tick(60)

    def _check_keydown_events(self, event):
        """ Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            # Move the ship right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move the ship left.
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_projectile()

    def _check_keyup_events(self, event):
        """ Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_projectile(self):
        """ Create a new projectile and add it to the projectiles group."""
        if len(self.projectiles) < self.settings.projectiles_allowed:
            new_projectile = Projectile(self)
            self.projectiles.add(new_projectile)

    def _check_events(self):
        """ Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _update_projectiles(self):
        """Update projectile position and remove old projectiles"""
        # Update projectile positions
        self.projectiles.update()

        # Get rid of projectiles that leave the screen (saves memory and resources)
        for projectile in self.projectiles.copy():
            if projectile.rect.bottom <= 0:
                self.projectiles.remove(projectile)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """ Respond to bullet-alien collisions """
        
        # Check for any projectiles that hit aliens
        # If a hit, get rid of bullet and alien
        collisions = pygame.sprite.groupcollide(self.projectiles, self.aliens, False, True)
        if not self.aliens:
            # Destroy existing projectiles and create new fleet
            self.projectiles.empty()
            self._create_fleet()
    
    def _update_aliens(self):
        """ Check if the fleet is at an edge, then update positions """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _update_screen(self):
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        for projectile in self.projectiles.sprites():
            projectile.draw_projectile() # type: ignore
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # make the most recent screen visible
        pygame.display.flip()

    def _create_fleet(self):
        """ Create a fleet of aliens """
        # Let's create an Alien and add aliens to fill screen width
        #Spacing is one alien wide and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished row; reset x and increment y
            current_x = alien_width
            current_y += 2 * alien_height
    def _create_alien(self, x_position, y_position):
        """ Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """ Respong if alien reached edge of screen """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ Drop the entire fleet and reverse direction """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """ Respond to the ship being hit by an alien """
        if self.stats.ships_left > 0:
            # Decrement shipts left
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and projectiles
            self.aliens.empty()
            self.projectiles.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """ Check if any aliens have reached the bottom of the screen """
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break
        

if __name__ == "__main__":
    # Create a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
