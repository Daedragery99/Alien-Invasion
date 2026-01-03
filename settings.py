class Settings:
    """Define and store all the game settings"""
    def __init__(self):
        self.screen_widht = 1200
        self.screen_height = 800
        self.bg_colort = (127, 127, 127)

        #Ship settings
        self.ship_speed = 6.5

        #bullet settings
        self.bullet_speed = 12.0
        self.bullet_widht = 3
        self.bullet_height = 15
        self.bullet_color = (0, 172, 245)
        self.bullets_allowed = 3