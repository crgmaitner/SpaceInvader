import sys
import pygame
from settings import Settings
from ship import Ship

class SpaceInvaders:
    """Overall class to manage game assets and behaviors"""

    def __init__(self):
        """Initialize game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Space Invaders')
        self.ship = Ship(self)

        # Optional fullscreen mode. Replace lines 14 and 15 with lines 21 - 23
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

    def run_game(self):
        """Start the main game loop"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

    # Watch for keyboard and mouse events.
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Movement controls for the starship.
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # Press Q to quit. Required for Fullscreen mode.
        elif event.key == pygame.K_q:
            sys.exit()
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # Redraw screen during each loop pass.
    def _update_screen(self):
        """Update images on screen, and flip to a new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = SpaceInvaders()
    ai.run_game()
