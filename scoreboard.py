import pygame.font


class Scoreboard:
    """A Class to Report Scoring Information."""

    def __init__(self, ai_game):
        """Initialize the Score-keeping Attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font Settings For Scoring Information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont("None", 48)

        # Prepare the Initial Score Image.
        self.prep_score()

    def prep_score(self):
        """Turn the Score into a Rendered Image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # Display the Score at the Top Right of the Screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw Score to the Screen."""
        self.screen.blit(self.score_image, self.score_rect)