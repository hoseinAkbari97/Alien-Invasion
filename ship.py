import pygame


class Ship:
    """A general class to manage the ship behaviour."""

    def __init__(self, ai_game):
        """Initializing the ship and setting its starting position."""

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        """loading the ship's image and getting its rect."""
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        """Start each new ship at the bottom center of the screen"""
        self.rect.midbottom = self.screen_rect.midbottom

        """Movement Flags"""
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag"""
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1

    def blitme(self):
        """Draw the ship at its current location."""

        self.screen.blit(self.image, self.rect)