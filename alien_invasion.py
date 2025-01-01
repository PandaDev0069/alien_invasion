import sys
from time import sleep

import pygame

from random import randint, uniform
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from explosion import Explosion

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height), pygame.DOUBLEBUF)
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self._create_fleet()

        # Load and play background music
        pygame.mixer.music.load('sounds/background_music.mp3')
        pygame.mixer.music.set_volume(0.5)  # Set background music volume to 50%
        pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

        # Load explosion sound
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')

        # Load explosion sprite sheet
        self.explosion_sheet = pygame.image.load('images/explosion_sheet.png')

        # Extract explosion frames from the sprite sheet
        self.explosion_frames = self._get_explosion_frames()

        # Start Alien Invasion in an active state.
        self.game_active = True

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_explosions()

            self._update_screen()
            self.clock.tick(60)


    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets."""
        # Update bullet positons.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisons."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    self._show_explosion(alien)
        
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()


    def _show_explosion(self, alien):
        """Show an explosion at the alien's position."""
        explosion = Explosion(self, alien.rect.center)
        self.explosions.add(explosion)


    def _update_explosions(self):
        """Update the position of explosions."""
        self.explosions.update()


    def _update_screen(self):
        """Update images on screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        for explosion in self.explosions.sprites():
            explosion.draw()

        pygame.display.flip()
    

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size


        current_x , current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 8 * alien_height):
            while current_x < (self.settings.screen_width - 2* alien_width):
                self._create_alien(current_x, current_y)
                current_x += uniform(1, 1.9) * alien_width
            
            # Finished a row, reset x value , and increment y value.
            current_x = alien_width + uniform(0, 8)
            current_y += uniform(1, 1.9) * alien_width


    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
        

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    
    def _change_fleet_direction(self):
        """Droop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
                    

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Play explosion sound
        self.explosion_sound.play()

        # Display explosion animation
        for frame in self.explosion_frames:
            self.screen.blit(frame, self.ship.rect)
            pygame.display.flip()
            pygame.time.delay(100)

        # Decrement ships_left.
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _get_explosion_frames(self):
        """Extract frames from the explosion sprite sheet."""
        frames = []
        sheet_width, sheet_height = self.explosion_sheet.get_size()
        frame_width = sheet_width // 5  # Assuming 5 frames in the sheet
        frame_height = sheet_height

        for i in range(5):
            frame = self.explosion_sheet.subsurface(pygame.Rect(
                i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)

        return frames


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this same as if the ship got hit. 
                self._ship_hit()
                break

if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
