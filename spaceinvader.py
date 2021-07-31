import sys
from time import sleep
import math
import pygame
from settings import Settings
from gamestats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from invader import Alien
from boom import Explosion, AlienExplosion, ShipExplosion
from star import Star
from random import randint

class SpaceInvaders:
    """Overall class to manage game assets and behaviors"""

    def __init__(self, num_aliens = 36):
        """Initialize game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Space Invaders')
        # Create an instance to store game stats
        self.stats = GameStats(self)
        # Make the Play button
        self.play_button = Button(self, "Play")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self.num_aliens = num_aliens

        # Optional fullscreen mode. Replace lines 23 and 24 with lines 39 - 41
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
        star.rect.x = 2.5 * star_width + 8 * star_width * star_number
        star.rect.y = star.rect.height + 8 * star.rect.height * star_row_number

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
        # Calculate number of rows.
        alien_amount_y = math.ceil(self.num_aliens / alien_amount_x)
        # Keep count.
        count = 0
        for row_number in range(alien_amount_y):
            for alien_number in range(alien_amount_x):
                self._create_alien(alien_number, row_number)
                count +=1
                if count >= self.num_aliens:
                    break

        # Create the fleet of Invaders.
        for row_number in range(alien_amount_y):
            for alien_number in range(alien_amount_x):
                self._create_alien(alien_number, row_number)

    # Create a single invader
    def _create_alien(self, alien_number, row_number):
        """Create Invader and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    # Create an explosion where an invader is destroyed
    def _create_alien_explosion(self, x, y):
        """Create an alien explosion and place it at x, y coordinates."""
        explosion = AlienExplosion(self, x, y)
        self.explosions.add(explosion)

    # Create an explosion when the player ship is destroyed
    def _create_ship_explosion(self, x, y):
        """Create a player ship explosion and place it at x, y coordinates."""
        explosion = ShipExplosion(self, x, y)
        self.explosions.add(explosion)

    # Create an instance of the player ship being hit by an invader
    def _ship_hit(self):
        """Respond to the ship being hit by an invader."""
        # Check the game state and adjust if conditions are met.
        if self.stats.ships_left > 0:
            # Decrement the amount of ships left
            self._create_ship_explosion(self.ship.rect.x, self.ship.rect.y)
            self.stats.ships_left -= 1
            # Get rid of any remaining invaders and bullets
            self.aliens.empty()
            self.bullets.empty()
            # Spawn a new fleet and center the player ship
            self._create_fleet()
            self.ship.center_ship()
            # Pause and regroup
            sleep(0.5)
        else:
            self.stats.game_active = False

    def run_game(self):
        """Start the main game loop"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_explosions()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    # Look for play button events.
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if self.play_button.rect.collidepoint(mouse_pos):
            # Reset game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True

            # Eliminate any remaining invaders and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and recenter the player ship
            self._create_fleet()
            self.ship.center_ship()

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

    # Change the fleet direction on-screen when reaching the edge.
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
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collision events."""
        # Check for bullet collison with invaders and remove bullet and
        # invader if collison is detected.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        for bullet in collisions:
            aliens = collisions[bullet]
            for alien in aliens:
                # Create alien explosion
                self._create_alien_explosion(alien.rect.x, alien.rect.y)
        if not self.aliens:
            # Destory existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()

    # Update invaders in-game.
    def _update_aliens(self):
        """
        Check if the fleet has reached an edge, then update positions of all
            invaders in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()
        # Check if an alien reaches the bottom.
        self._check_alien_bottom()
        # Check for alien collision with ship.
        for alien in self.aliens:
            #if pygame.sprite.collide_rect(self.ship, alien):
            if pygame.sprite.spritecollideany(self.ship, self.aliens):
                # Create ship explosion
                self._create_ship_explosion(self.ship.rect.x, self.ship.rect.y)
                self._ship_hit()
                return

    # Check for invaders reaching the bottom of the screen.
    def _check_alien_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # React in the same way as if the player ship has been hit.
                self._create_ship_explosion(self.ship.rect.x, self.ship.rect.y)
                self._ship_hit()
                break

    # Update explosions.
    def _update_explosions(self):
        """Update all explosions in-game."""
        self.explosions.update()

    # Redraw the screen during each loop pass.
    def _update_screen(self):
        """Update images on screen, and flip to a new screen."""
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.explosions.draw(self.screen)
        # Draw the play button to the screen if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = SpaceInvaders()
    ai.run_game()