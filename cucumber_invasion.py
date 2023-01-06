import sys
import pygame
from time import sleep

from settings import Settings
from cat import Cat
from bullet import Bullet
from cucumber import Cucumber
from game_stats import GameStats
from button import Button

class CucumberInvasion:

    def __init__(self):

        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Cucumber Invasion")
        
        self.bg_color = self.settings.bg_color

        self.cat = Cat(self)
        self.bullets = pygame.sprite.Group()
        self.cucumbers = pygame.sprite.Group()
        
        self._create_fleet()
        
        self.stats = GameStats(self)
        
        self.play_button = Button(self, "Play")
        
    def run_game(self):

        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.cat.update()
                self._update_bullets()
                self._update_cucumber()
            
            self._update_screen()
            
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True
            
            self.cucumbers.empty()
            self.bullets.empty()
            
            self._create_fleet()
            self.cat.center_cat()
            
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
           # self.cat.rect.x += 1
            self.cat.moving_right = True
        elif event.key == pygame.K_LEFT:
           # self.cat.rect.x -= 1
            self.cat.moving_left = True 
        elif event.key == pygame.K_q:
            sys.exit()  
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.cat.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.cat.moving_left = False

    def _fire_bullet(self):
        
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.cat.blitme()
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            
        self.cucumbers.draw(self.screen)
        
        if not self.stats.game_active:
            self.play_button.draw_button()
        
        pygame.display.flip()
            
    def _update_bullets(self):
        
        self.bullets.update()

        #Get rid of bullets that have disapeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_cucumber_collisions()


               
    def _check_bullet_cucumber_collisions(self):
        
        collisions = pygame.sprite.groupcollide(self.bullets, self.cucumbers, True, True)
        
        if not self.cucumbers:
            self.bullets.empty()
            self._create_fleet()
               
               
    def _update_cucumber(self):
        self._check_fleet_edges()
        self.cucumbers.update()
        
        if pygame.sprite.spritecollideany(self.cat, self.cucumbers):
            print("Cat hit by a cucumber!!!")
            self._cat_hit()
            
        self._check_cucumbers_bottom()
    
    def _create_fleet(self):
        
        cucumber = Cucumber(self)
        #self.cucumbers.add(cucumber)
        cucumber_width, cucumber_height = cucumber.rect.size
        
        available_space_x = self.settings.screen_width - (2 * cucumber_width) * 0
        number_cucumbers_x = available_space_x // (2  * cucumber_width)
        
        # N rows to fit on the screen
        cat_height = self.cat.rect.height
        available_space_y = self.settings.screen_height - (2 * cucumber_height) - cat_height
        number_rows = available_space_y // (2 * cucumber_height)
        
        for row_number in range(number_rows):
            for cucumber_number in range(number_cucumbers_x):
                self._create_cucumber(cucumber_number, row_number)
            
            
            

    def _create_cucumber(self,cucumber_number, row_number):
            cucumber = Cucumber(self)
            cucumber_width, cucumber_height = cucumber.rect.size
            cucumber.x = cucumber_width + 2 * cucumber_width * cucumber_number
            cucumber.rect.x = cucumber.x
            
            cucumber.rect.y = cucumber_height + 2 * cucumber_height * row_number
            
            self.cucumbers.add(cucumber)
        

    def _check_fleet_edges(self):
        for cucumber in self.cucumbers.sprites():
            if cucumber.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        for cucumber in self.cucumbers.sprites():
            cucumber.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _cat_hit(self):
        
        if self.stats.cats_left > 0:
            self.stats.cats_left -= 1
            
            self.cucumbers.empty()
            self.bullets.empty()

            self._create_fleet()
            self.cat.center_cat()
        
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
        
    def _check_cucumbers_bottom(self):
        screen_rect = self.screen.get_rect()
        for cucumber in self.cucumbers.sprites():
            if cucumber.rect.bottom >= screen_rect.bottom:
                self._cat_hit()
                break
            
    
    
if __name__ == "__main__":
    ai = CucumberInvasion()
    ai.run_game()
    

