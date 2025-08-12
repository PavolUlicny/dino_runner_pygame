#imports
import pygame
import os
import sys
import random

class DinoRunner: 
    
    def __init__(self):
        
        #initialize pygame
        pygame.init()
        
        #create window
        WINDOW_WIDTH = 700
        WINDOW_HEIGHT = 350
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Dino runner")
        
        #variables
        self.folder = "dino_runner_pygame/dino_runner/"
        self.KEY = 110
        self.score = 0
        self.high_score = 0
        self.clock = pygame.time.Clock()
        self.dinox = 75
        self.dinoy = 223
        self.cactus1y = 215
        self.cactus2y = 215
        self.cactus3y = 215
        self.cactus1x = 900
        self.cactus2x = 1500
        self.cactus3x = 2100
        self.dino_width = 50
        self.dino_height = 52
        self.dino_down_width = 63
        self.dino_down_height = 34
        self.single_cactus_width = 31
        self.cactus_height = 60
        self.double_cactus_width = 61
        self.triple_cactus_width = 55
        self.bird_width = 51
        self.bird_up_height = 33
        self.bird_down_height = 37
        
        #load fonts and texts
        self.TEXT_COLOR = (0, 0, 0)
        self.large_font = pygame.font.SysFont("Courier", 60)
        self.small_font = pygame.font.SysFont("Arial", 30)
        
        #load cactus images 
        single_cactus_img1 = pygame.image.load((f"{self.folder}single_cactus.png"))
        double_cactus_img1 = pygame.image.load((f"{self.folder}double_cactus.png"))
        triple_cactus_img1 = pygame.image.load((f"{self.folder}triple_cactus.png"))
        self.single_cactus_img = pygame.transform.scale(single_cactus_img1, (31, 60))
        self.double_cactus_img = pygame.transform.scale(double_cactus_img1, (61, 60))
        self.triple_cactus_img = pygame.transform.scale(triple_cactus_img1, (62, 60))
        self.cactus_imgs = (self.single_cactus_img, self.double_cactus_img, self.triple_cactus_img)
        self.cactus1_hit = pygame.Rect(self.cactus1x, self.cactus1y, self.single_cactus_width, self.cactus_height)
        self.cactus2_hit = pygame.Rect(self.cactus2x, self.cactus2y, self.triple_cactus_width, self.cactus_height)
        self.cactus3_hit = pygame.Rect(self.cactus3x, self.cactus3y, self.double_cactus_width, self.cactus_height)
        self.cactus1_sprite_img = self.cactus_imgs[0]
        self.cactus2_sprite_img = self.cactus_imgs[2]
        self.cactus3_sprite_img = self.cactus_imgs[1]
        
        #load dino images
        self.dino_img_def = pygame.image.load((f"{self.folder}trex.png"))
        self.dino_img_left = pygame.image.load((f"{self.folder}trex_left.png"))
        self.dino_img_right = pygame.image.load((f"{self.folder}trex_right.png"))
        self.dino_img_down_left = pygame.image.load((f"{self.folder}trex_down_left.png"))
        self.dino_img_down_right = pygame.image.load((f"{self.folder}trex_down_right.png"))
        self.dino_hit = pygame.Rect(self.dinox + 3, self.dinoy - 3, self.dino_width - 13, self.dino_height - 5)
        self.dino_sprite_img = self.dino_img_def
        
        #load bird images
        bird_down1 = pygame.image.load((f"{self.folder}bird_down.png"))
        bird_up1 = pygame.image.load((f"{self.folder}bird_up.png"))
        self.bird_down = pygame.transform.scale(bird_down1, (51, 37))
        self.bird_up = pygame.transform.scale(bird_up1, (51, 33))
        
        #load text
        self.game_over_text = self.large_font.render("Game over", False, self.TEXT_COLOR)
        self.restart_text = self.small_font.render(f"Press Space to restart", False, self.TEXT_COLOR)
        self.high_score_text = self.small_font.render(f"High score: {int(self.high_score)}", False, self.TEXT_COLOR)

    #func that checks if a txt file is empty
    def is_empty(self, file):
        return os.stat(file).st_size == 0
    
    #func that encrypts the high score
    def encrypt(self, num):
        digits = [chr(int(d) + self.KEY) for d in str(num)]
        return ''.join(reversed(digits))

    #func that decrypts the high score
    def decrypt(self, text):
        digits = [str(ord(c) - self.KEY) for c in reversed(text)]
        return int(''.join(digits))

    #load high score
    def load_high_score(self):
        high_score_path = f"{self.folder}high_score.txt"
        open(high_score_path, "a").close()
        if not self.is_empty(high_score_path):
            with open(high_score_path, "r") as high_score_file:
                self.high_score = int(self.decrypt(high_score_file.read()))

    #function to save the high score
    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open(f"{self.folder}high_score.txt", "w") as high_score_file:
                high_score_file.write(self.encrypt(int(self.high_score)))
    
    #exit game function
    def exit_game(self):
        pygame.quit()
        sys.exit()
        
    #game over function
    def game_over(self):
        self.save_high_score()
        self.game_over_loop()

    def start_game(self):
        self.load_high_score()
        self.start_screen_loop()

    def start_screen_loop(self):
        
        #load text
        dino_runner_text = self.large_font.render("Dino runner", False, self.TEXT_COLOR)
        start_text = self.small_font.render(f"Press the Jump key", False, self.TEXT_COLOR)
        high_score_text = self.small_font.render(f"High score: {int(self.high_score)}", False, self.TEXT_COLOR)
        
        while True:
            
            #set fps
            self.clock.tick(60)
            
            #fill window with white color
            self.window.fill((255, 255, 255))
            
            #text
            self.window.blit(dino_runner_text , (140, 50))
            self.window.blit(start_text, (225, 125))
            self.window.blit(high_score_text, (240, 170))
            
            #check for events
            for event in pygame.event.get():
                    
                #close the game if the window is closed
                if event.type == pygame.QUIT:
                    self.exit_game()
                    return
            
                #binds keys to start game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.game_loop()
                        return
                        
                    elif event.key == pygame.K_ESCAPE:
                        self.exit_game()
                        return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.game_loop()
                        return
            
            #update display
            pygame.display.update()
    
    def game_loop(self):
        
        #initialize variables 
        self.score = 0
        JUMP_STRENGTH = 9
        GRAVITY = 0.5
        CACTUS_SPEED = 10
        fall_speed = 0
        grounded = True
        animation_counter = 0
        animation_counter1 = 0
        animation_counter2 = 0
        animation_counter3 = 0
        sliding = False
        cactus1_bird = False
        cactus2_bird = False
        cactus3_bird = False
        
        while True:
            
            #set fps
            self.clock.tick(60)
            
            #fill window with white color
            self.window.fill((255, 255, 255))
            
            #create the ground line
            pygame.draw.line(self.window, (0, 0, 0), (0, 275), (700, 275), width = 2)
            
            #load images into the window
            self.window.blit(self.dino_sprite_img, (self.dinox, self.dinoy))
            self.window.blit(self.cactus1_sprite_img, (self.cactus1x, self.cactus1y))
            self.window.blit(self.cactus2_sprite_img, (self.cactus2x, self.cactus2y))
            self.window.blit(self.cactus3_sprite_img, (self.cactus3x, self.cactus3y))
            
            #load texts
            score_text = self.small_font.render(f"Score: {int(self.score)}", False, self.TEXT_COLOR)
            self.window.blit(score_text, (500, 30))
            
            #apply jump/fall physics to dino
            self.dinoy += fall_speed
            
            #make the cacti move 
            self.cactus1x -= CACTUS_SPEED
            self.cactus2x -= CACTUS_SPEED
            self.cactus3x -= CACTUS_SPEED
            
            #some lists and tuples
            cactus_x = (self.cactus1x, self.cactus2x, self.cactus3x)
            cactus_y = (self.cactus1y, self.cactus2y, self.cactus3y)
            cactus_img_hitboxes = (self.cactus1_sprite_img, self.cactus2_sprite_img, self.cactus3_sprite_img)
            cactus_hitboxes = [self.cactus1_hit, self.cactus2_hit, self.cactus3_hit]
            
            #return cacti if they go off screen
            if self.cactus1x < -60:
                self.cactus1x = self.cactus3x + random.randint(500, 700)
                num = random.randint(1, 3)
                if num == 1 or num == 2 or self.score < 150:
                    cactus1_bird = False
                    self.cactus1y = 215
                    num1 = random.randint(0, 2)
                    self.cactus1_sprite_img = self.cactus_imgs[num1]
                else:
                    cactus1_bird = True
                    
            if self.cactus2x < -60:
                self.cactus2x = self.cactus1x + random.randint(500, 700)
                num = random.randint(1, 3)
                if num == 1 or num == 2 or self.score < 150:
                    cactus2_bird = False
                    self.cactus2y = 215
                    num1 = random.randint(0, 2)
                    self.cactus2_sprite_img = self.cactus_imgs[num1]
                else:
                    cactus2_bird = True
                    
            if self.cactus3x < -60:
                self.cactus3x = self.cactus2x + random.randint(500, 700)
                num=random.randint(1, 3)
                if num == 1 or num == 2 or self.score < 150:
                    cactus3_bird = False
                    self.cactus3y = 215
                    num1 = random.randint(0, 2)
                    self.cactus3_sprite_img = self.cactus_imgs[num1]
                else:
                    cactus3_bird = True
                    
            #put bird img on cactus if its a bird
            if cactus1_bird:
                self.cactus1y = 190
                animation_counter1 += 1
                if animation_counter1 // 10 % 2 == 0:
                    self.cactus1_sprite_img = self.bird_up
                else:
                    self.cactus1_sprite_img = self.bird_down
                    
            if cactus2_bird:
                self.cactus2y = 190
                animation_counter2 += 1
                if animation_counter2 // 10 % 2 == 0:
                    self.cactus2_sprite_img = self.bird_up
                else:
                    self.cactus2_sprite_img = self.bird_down
                    
            if cactus3_bird:
                self.cactus3y = 190
                animation_counter3 += 1
                if animation_counter3 // 10 % 2 == 0:
                    self.cactus3_sprite_img = self.bird_up
                else:
                    self.cactus3_sprite_img = self.bird_down
                    
            #hitboxes
            dino_def_rect = pygame.Rect(self.dinox + 3, self.dinoy - 3, self.dino_width - 13, self.dino_height - 5)
            dino_down_rect = pygame.Rect(self.dinox, self.dinoy, self.dino_down_width - 3, self.dino_down_height)
            for inx, img in enumerate(cactus_img_hitboxes):
                if img == self.single_cactus_img:
                    cactus_hitboxes[inx] = pygame.Rect(cactus_x[inx] + 13, cactus_y[inx] + 3, self.single_cactus_width, self.cactus_height)
                elif img == self.double_cactus_img:
                    cactus_hitboxes[inx] = pygame.Rect(cactus_x[inx] + 13, cactus_y[inx] + 3, self.double_cactus_width, self.cactus_height)
                elif img == self.triple_cactus_img:
                    cactus_hitboxes[inx] = pygame.Rect(cactus_x[inx] + 15, cactus_y[inx] + 5, self.triple_cactus_width, self.cactus_height)
                elif img == self.bird_down:
                    cactus_hitboxes[inx] = pygame.Rect(cactus_x[inx] + 10, cactus_y[inx], self.bird_width, self.bird_down_height)
                elif img == self.bird_up:
                    cactus_hitboxes[inx] = pygame.Rect(cactus_x[inx] + 10, cactus_y[inx], self.bird_width, self.bird_up_height)
            self.cactus1_hit = cactus_hitboxes[0]
            self.cactus2_hit = cactus_hitboxes[1]
            self.cactus3_hit = cactus_hitboxes[2]
            
            #check for collision
            if self.dino_hit.colliderect(self.cactus1_hit) or self.dino_hit.colliderect(self.cactus2_hit) or self.dino_hit.colliderect(self.cactus3_hit):
                self.game_over()
                return

            #increase score
            self.score += 0.2

            #check if dino is touching the ground (if hes under the ground, put him on the ground) and changing his img
            if self.dinoy >= 223:
                grounded = True
                self.dinoy = 223
                fall_speed = 0
                animation_counter += 1
                if not sliding:
                    self.dino_hit = dino_def_rect
                    self.dinoy = 223
                    if animation_counter // 5 % 2 == 0:
                        self.dino_sprite_img = self.dino_img_left
                    else:
                        self.dino_sprite_img = self.dino_img_right
                else:
                    self.dino_hit = dino_down_rect
                    self.dinoy = 241
                    if animation_counter // 5 % 2 == 0:
                        self.dino_sprite_img = self.dino_img_down_left
                    else:
                        self.dino_sprite_img = self.dino_img_down_right
            else:
                self.dino_hit = dino_def_rect
                grounded = False
                fall_speed += GRAVITY
                self.dino_sprite_img = self.dino_img_def
                
            #check for events
            for event in pygame.event.get():
                    
                #close the game if the window is closed
                if event.type == pygame.QUIT:
                    self.exit_game()
                    return

                #binds keys to jump
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        if grounded:
                            fall_speed = -JUMP_STRENGTH
                    
                    elif event.key == pygame.K_ESCAPE:
                        self.exit_game()
                        return
                        
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        sliding = True  
                            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if grounded:
                            fall_speed = -JUMP_STRENGTH
                            
                    if event.button == 3:
                        sliding = True
                            
                #binds key to slide
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        sliding = False
                if event.type == pygame.MOUSEBUTTONUP:
                    sliding = False
        
            #update display
            pygame.display.update()
            
    #game over loop 
    def game_over_loop(self):

        #update score text
        score_text = self.small_font.render(f"Score: {int(self.score)}", False, self.TEXT_COLOR)
        
        while True:
            
            #set fps
            self.clock.tick(60)
            
            #fill window with white color
            self.window.fill((255, 255, 255))
            
            #text
            self.window.blit(self.game_over_text, (185, 50))
            self.window.blit(self.restart_text, (225, 125))
            self.window.blit(score_text, (285, 180))
            self.window.blit(self.high_score_text, (245, 230))
            
            #check for events
            for event in pygame.event.get():
                    
                #close the game if the window is closed
                if event.type == pygame.QUIT:
                    self.exit_game()
                    return

                #binds keys to start game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_loop()
                        return
                        
                    elif event.key == pygame.K_ESCAPE:
                        self.exit_game()
                        return
            
            #update display
            pygame.display.update() 

game = DinoRunner()
game.start_game()