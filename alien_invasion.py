import sys

from time import sleep

import pygame

from setting import Setting

from game_stats import GameStats

from scoreboard import Scoreboard

from ship import Ship

from bullet import Bullet

from alien import Alien

from button import Button


class AlienInvasion:

    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Setting()

        self.screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store the game statistics.
        # And Create a Scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Creating the Game Elements.
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Creating an entire fleet of aliens
        self._create_fleet()

        # Make the Play and Difficulty Button
        self.play_button = Button(self, "PLAY", 0)
        self.dif_button = Button(self, "DIFFICULTY(DEFAULT:MEDIUM", 4)
        self.dif_1 = Button(self, "EASY", 3)
        self.dif_2 = Button(self, "MEDIUM", 2)
        self.dif_3 = Button(self, "Hard", 1)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Watch for keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pose):
        """Start a New Game When the Player Clicks Play
        or Choose the Difficulty."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pose)
        dif_clicked_1 = self.dif_1.rect.collidepoint(mouse_pose)
        dif_clicked_2 = self.dif_2.rect.collidepoint(mouse_pose)
        dif_clicked_3 = self.dif_3.rect.collidepoint(mouse_pose)

        # Operating the Play Button
        if button_clicked and not self.stats.game_active:
            # Reset the Game Settings
            self.settings.initialize_dynamic_settings()
            self._start_game()

        # Operating Difficulty Levels
        elif dif_clicked_1 and not self.stats.game_active:
            self.settings.diff_flag = 1
            self.dif_1.selected_button()
            self.dif_2.reset_button()
            self.dif_3.reset_button()
        elif dif_clicked_2 and not self.stats.game_active:
            self.settings.diff_flag = 2
            self.dif_2.selected_button()
            self.dif_1.reset_button()
            self.dif_3.reset_button()
        elif dif_clicked_3 and not self.stats.game_active:
            self.settings.diff_flag = 3
            self.dif_3.selected_button()
            self.dif_1.reset_button()
            self.dif_2.reset_button()

    def _check_keydown_events(self, event):
        """Respond to keypress."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                # Reset the Game Settings.
                self.settings.initialize_dynamic_settings()
                self._start_game()

    def _check_keyup_events(self, event):
        """Respond to key release."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Creating a new bullet and adding it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullets positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien collision."""
        # Remove any bullets and aliens that have collided.
        collision = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collision:
            for aliens in collision.values():
                self.stats.score += self.settings.alien_points*len(aliens)
            self.sb.prep_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

        # For test
        # print(len(self.bullets))

    def _update_aliens(self):
        """Check if the fleet is at an edge,
        then update the position of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collision.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create a fleet of aliens"""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - 2*alien_width
        number_aliens_x = available_space_x // (2*alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3*alien_height) - ship_height)
        number_rows = available_space_y // (2*alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in a row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Check if any aliens have reached
        the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships left.
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and Center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _start_game(self):
        """Start a New Game When a Player Clicks the Play Button
        or Presses P on Keyboard"""
        # Reset the Game Statistics
        self.stats.reset_status()
        self.stats.game_active = True
        self.sb.prep_score()

        # Get Rid of Any Remaining Aliens and Bullets
        self.aliens.empty()
        self.bullets.empty()

        # Create a New Fleet and Center the Ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the Mouse Cursor
        pygame.mouse.set_visible(False)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        """Redraw the screen during each pass of the loop"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the Score Information.
        self.sb.show_score()

        # Draw the Play and Difficulty Buttons if the Game Is Inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.dif_button.draw_button()
            self.dif_1.draw_button()
            self.dif_2.draw_button()
            self.dif_3.draw_button()

        """Make the most recently drawn screen visible."""
        pygame.display.flip()


if __name__ == '__main__':
    """Make a game instance, and run the game."""
    ai = AlienInvasion()
    ai.run_game()
