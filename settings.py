class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (211, 211, 211)  # Light gray color

        # Ship setting
        self.ship_speed = 3

        # Bullet settings
        self.bullet_speed = 5.0
        self.bullets_allowed = 5