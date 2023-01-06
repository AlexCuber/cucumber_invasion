import pygame

class Cat:
    
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        
        # Movement flag
        self.moving_right = False
        self.moving_left = False
        
        self.image = pygame.image.load("images/cat3.bmp")
        self.image = pygame.transform.scale(self.image, (85,85))
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        
        self.x = float(self.rect.x)
        
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += 1
            self.x += self.settings.cat_speed
        elif self.moving_left and self.rect.left > 0:
            self.rect.x -= 1
            self.x -= self.settings.cat_speed
        self.rect.x = self.x
        
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
    def center_cat(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)