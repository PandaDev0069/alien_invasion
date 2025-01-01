import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """A class to manage explosions."""

    def __init__(self, ai_game, position):
        """Initialize the explosion and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.frames = self._load_frames()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.frame_delay = 20  # milliseconds
        self.last_update = pygame.time.get_ticks()

        # Load and play explosion sound
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')
        self.explosion_sound.set_volume(0.1)  # Set explosion sound volume to 10%
        self.explosion_sound.play()

    def _load_frames(self):
        """Load explosion frames from the sprite sheet."""
        explosion_sheet = pygame.image.load('images/explosion_sheet.png')
        frame_width = explosion_sheet.get_width() // 5
        frame_height = explosion_sheet.get_height()
        frames = [explosion_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(5)]
        return frames

    def update(self):
        """Update the explosion animation."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.frame_index += 1
            if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]
            else:
                self.kill()

    def draw(self):
        """Draw the explosion to the screen."""
        self.screen.blit(self.image, self.rect)