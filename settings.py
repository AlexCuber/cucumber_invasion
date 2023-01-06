
class Settings:
    
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 240, 241)
        self.cat_speed = 3.5
        self.cat_limit = 3
        
        # Bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 10
        self.bullet_height = 10
        self.bullet_color = (230,40,160)
        self.bullets_allowed = 5
        
        # Cucumber settings
        self.cucumber_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
