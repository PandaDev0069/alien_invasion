class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        # Read high score from file
        self.high_score = self._read_high_score()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _read_high_score(self):
        """Read the high score from a file."""
        try:
            with open('high_score.txt', 'r') as file:
                high_score = file.read().strip()
                return int(high_score) if high_score else 0
        except (FileNotFoundError, ValueError):
            return 0

    def _write_high_score(self):
        """Write the high score to a file."""
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))