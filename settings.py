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
        self.bg_color = (100, 100, 200)

        # Ship settings
        self.ship_speed = 1.5
