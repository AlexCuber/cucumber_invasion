class GameStats:
    """Statistics for Cucumber Invasion"""
    
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        
    def reset_stats(self):
        self.cats_left = self.settings.cat_limit
        
    