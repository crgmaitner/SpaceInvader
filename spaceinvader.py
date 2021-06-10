import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from invader import Alien
from star import Star
from random import randint

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
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        # Optional fullscreen mode. Replace lines 16 and 17 with lines 24 - 26
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self._create_fleet()
        self._create_stars()

    def _create_stars(self):
        """Create a starmap"""
        # Create a star and find the number of stars in a row.
        # Spacing between each star is equal to two star width.
        star = Star(self)
        star_width, star_height = star.rect.size
        # Calculate horizontal space between each star.
        available_space_x = self.settings.screen_width - (star_width)
        # Calculate number of stars per row across the screen.
        star_amount_x = available_space_x // (2 * star_width)
        # Determine the number of rows of stars that fit on the screen.
        available_space_y = (self.settings.screen_height -
                                (2 * star_height))
        number_rows = available_space_y // (2 * star_height)

        # Create the star map.
        for star_row_num in range(number_rows):
            for star_number in range(star_amount_x):
                self._create_star(star_number, star_row_num)

    def _create_star(self, star_number, star_row_number):
        """Create stars and place them in the star map."""
        star = Star(self)
        star_width, star_height = star.rect.size
        star.rect.x = 2.5 * star_width + 6 * star_width * star_number
        star.rect.y = star.rect.height + 6 * star.rect.height * star_row_number

        # Randomize star locations on screen.
        star.rect.x += randint(-15, 15)
        star.rect.y += randint(-15, 15)

        self.stars.add(star)

    def _create_fleet(self):
        """Create the Invader Fleet"""
        # Make an Invader Fleet by finding the number of invaders per row.
        # Space between Invaders is equal to one Invader width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # Calculate horizontal space between Invaders.
        space_available_x = self.settings.screen_width - (2 * alien_width)
        # Calculate number of Invaders per horizontal space.
        alien_amount_x = space_available_x // (2 * alien_width)

        # Determine the number of rows of Invaders that fit on screen.
        ship_height = self.ship.rect.height
        space_available_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = space_available_y // (2 * alien_height)

        # Create the fleet of Invaders.
        for row_number in range(number_rows):
            for alien_number in range(alien_amount_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create Invader and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def run_game(self):
        """Start the main game loop"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    # Look for keyboard and mouse events.
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

    # Actions take when keys are pressed down.
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # Press Q to quit. Required for Fullscreen mode.
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    # Actions taken when keys are released.
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # Check if the fleet has reached an edge of the screen.
    def _check_fleet_edges(self):
        """Respond appropriately if an invader reaches an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_direction()
                break

    # Change the fleet direction on-screen.
    def _change_direction(self):
        """Drop entire fleet and change movement direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # Firing a bullet functionality.
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    # Update bullets in-game.
    def _update_bullets(self):
        """Update the position of bullets and delete old bullets"""
        self.bullets.update()
        # Delete bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # Check for bullet collison with invaders and remove bullet and
        # invader if collison is detected.
        collision = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

    # Update invaders in-game.
    def _update_aliens(self):
        """
        Check if the fleet has reached an edge, then update positions of all
            invaders in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

    # Redraw screen during each loop pass.
    def _update_screen(self):
        """Update images on screen, and flip to a new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.stars.draw(self.screen)

        # Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = SpaceInvaders()
    ai.run_game()
