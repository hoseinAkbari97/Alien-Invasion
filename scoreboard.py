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

        # Prepare the Initial Score Images.
        self.prep_score()
        self.prep_high_score()

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

    def prep_high_score(self):
        """Turn the High Score into a Rendered Image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color,
            self.settings.bg_color)

        # Center the High Score at the Top of the Screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check to See If There's a New High Score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Draw Score to the Screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)