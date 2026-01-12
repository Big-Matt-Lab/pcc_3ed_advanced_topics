"""
alien_invasion game
Python Crash Course chapters 12 - 14
Creating a 2D game using python and pygame
"""
# import packages
import sys

import pygame

from settings import Settings
from ship import Ship
from projectile import Projectile

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.projectiles = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self.ship.update()
            self.projectiles.update()

            # Get rid of projectiles that leave the screen (saves memory and resources)
            for projectile in self.projectiles.copy():
                if projectile.rect.bottom <= 0:
                    self.projectiles.remove(projectile)
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

    def _update_screen(self):
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        for projectile in self.projectiles.sprites():
            projectile.draw_projectile()
        self.ship.blitme()

        # make the most recent screen visible
        pygame.display.flip()


if __name__ == "__main__":
    # Create a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
