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
        self.screen_width = 500
        self.screen_height = 660
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3


        # Projectile settings
        self.projectiles_allowed = 7
        self.projectile_speed = 4
        self.projectile_width = 3
        self.projectile_height = 15
        self.projectile_color = (60, 60, 60)

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        
        
