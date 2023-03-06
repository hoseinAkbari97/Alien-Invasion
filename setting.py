class Setting:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the Game's Static Settings."""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        # Ship settings
        # self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet Settings
        # self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien Settings
        # self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # Fleet direction of 1 represent right, -1 represent left.
        # self.fleet_direction = 1

        # How Quicly the Game Speeds Up
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initializing Settings that Change Throughout the Game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # Fleet Direction of 1 Represents Right, -1 Represents Left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase Speed Settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale