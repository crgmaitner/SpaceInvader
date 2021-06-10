import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """A class that represents a single explosion"""

    def __init__(self, ai_game):
        """Initalize the explosion and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

    def update(self):
        """Decrement explosion time"""
        self.explosion_time = self.explosion_time - 1
        if self.explosion_time <= 0:
            self.kill()
        self.rect.x = self.x

class AlienExplosion(Explosion):
    """A class that represents a single explosion"""

    def __init__(self, ai_game, x, y):
        """Initalize the explosion and set its starting position"""
        super().__init__(ai_game)

        # Load the explosion image and set its rect attribute.
        self.image = pygame.image.load('images/alienboom.bmp')
        self.rect = self.image.get_rect()

        # Start each new explosion at defined position.
        self.rect.x = x
        self.rect.y = y

        # Store explosion's exact horizontal position.
        self.x = float(self.rect.x)

        # Store explosion's time
        self.explosion_time = 40

    def update(self):
        """Decrement explosion time"""
        self.explosion_time -= 1
        if self.explosion_time <= 0:
            self.kill()
        self.rect.x = self.x

class ShipExplosion(Explosion):
    """A class that represents a single ship explosion"""

    def __init__(self, ai_game, x, y):
        """Initalize the explosion and set its starting position"""
        super().__init__(ai_game)

        # Load the explosion image and set its rect attribute.
        self.image = pygame.image.load('images/boom.bmp')
        self.rect = self.image.get_rect()

        # Start each new explosion at defined position.
        self.rect.x = x
        self.rect.y = y

        # Store explosion's exact horizontal position.
        self.x = float(self.rect.x)

        # Store explosion's time
        self.explosion_time = 40

    def update(self):
        """Decrement explosion time"""
        self.explosion_time -= 1
        if self.explosion_time <= 0:
            self.kill()
        self.rect.x = self.x
