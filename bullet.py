import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Creat a bullet object at the ship'S current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Load the bullet image and set its rect attribue.
        self.image = pygame.image.load(r"images\bullet.bmp")
        self.rect = self.image.get_rect()

        # Create a bullet rect at (0, 0) and then set correct positon.
        self.rect = pygame.Rect(0, 0, self.rect.width,
                                self.rect.height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as float.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        # Update the exact position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update rect positon.
        self.rect.y = self.y
    
    def draw_bullet(self):
        """Draw the bullet to he screen"""
        self.screen.blit(self.image, self.rect)