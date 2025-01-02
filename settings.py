class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (211, 211, 211)  # Light gray color

        # Ship settings
        self.ship_speed = 3
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 5.0
        self.bullets_allowed = 5

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Difficulty settings
        self.difficulty = 'medium'

        # Speedup scale
        self.speedup_scale = 1.1

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        if self.difficulty == 'easy':
            self.ship_speed = 1.5
            self.bullet_speed = 3.0
            self.alien_speed = 1.0
        elif self.difficulty == 'medium':
            self.ship_speed = 3.0
            self.bullet_speed = 5.0
            self.alien_speed = 1.5
        elif self.difficulty == 'hard':
            self.ship_speed = 4.5
            self.bullet_speed = 7.0
            self.alien_speed = 2.0

        # Scoring settings
        

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
