class Settings:
    """Class to store all settings for Space Invader."""

    def __init__(self):
        """Initialize the game's settings."""

        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (0, 0, 0)

        # Ship Settings
        self.ship_speed = 2.5
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 4

        # Invader Settings
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1
