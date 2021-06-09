import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class that represents a single invader in the fleet"""

    def __init__(self, ai_game):
        """Initalize the invader and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen

        # Load the invader image and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store alien's exact horizontal position.
        self.x = float(self.rect.x)
