import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class that represents a single invader in the fleet"""

    def __init__(self, ai_game):
        """Initalize the invader and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the invader image and set its rect attribute.
        self.image = pygame.image.load('images/ufo.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store alien's exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """Move Invader to the left and right"""
        self.x += (self.settings.alien_speed *
                    self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edge(self):
        """Return True if a invader is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <=0:
            return True
