"""
Settings file for pygame
Python Crash Course chapters 12 - 14
Creating a 2D game using python and pygame
"""
class Settings:
    """
    Settings class for Alien Invasion
    """
    def __init__(self):
        """
        Init method for settings class
        """
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 660
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5

        # Projectile settings
        self.projectiles_allowed = 7
        self.projectile_speed = 2.5
        self.projectile_width = 3
        self.projectile_height = 15
        self.projectile_color = (60, 60, 60)
