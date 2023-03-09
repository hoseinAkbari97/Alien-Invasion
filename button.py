import pygame.font


class Button:
    def __init__(self, ai_game, msg, num):
        """Initialize Button Attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the Dimensions and Properties of the Button
        self.width, self.height = 500, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('None', 48)

        # Build the Button Rect Object and Center It.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = \
            self.screen_rect.centery + (num*self.height)

        # The Button Message Needs to Be Prepped Only Once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg Into a Rendered Image and Center Text on the Button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def selected_button(self):
        """Changing the Color of the Selected Button."""
        self.button_color = (255, 0, 0)
        self.text_color = (100, 100, 100)

    def reset_button(self):
        """Resetting the Color of the Button"""
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)

    def draw_button(self):
        """Draw Blank Button and Then Draw Message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)