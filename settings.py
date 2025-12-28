class Settings:
    """Define and store all the game settings"""
    def __init__(self):
        self.screen_widht = 1200
        self.screen_height = 800
        self.bg_colort = (255, 255, 255)

        #Ship settings
        self.ship_speed = 1.5