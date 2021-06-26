import pygame

class GameStats:
    """Track in-game statistics."""

    def __init__(self, ai_game):
        """Initialize game statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        # Start the game in an inactive state.
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics which change in-game"""
        self.ships_left = self.settings.ship_limit
