# Imports
import pygame
import os
import sys
import random

class DinoRunner: 
    
    def __init__(self):
        
        # Initialize pygame
        pygame.init()

        # Create window
        WINDOW_WIDTH = 700
        WINDOW_HEIGHT = 350
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Dino runner")
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_in_subdir = os.path.join(base_dir, "assets")
        if os.path.isfile(os.path.join(assets_in_subdir, "single_cactus.png")):
            self.folder = assets_in_subdir
        else:
            self.folder = base_dir
            
        self.key = 110
        self.score = 0
        self.high_score = 0
        self.clock = pygame.time.Clock()
        self.dinoX = 75
        self.dinoY = 223
        self.cactus1X = 900
        self.cactus2X = 1500
        self.cactus3X = 2100
        self.cactus1Y = 215
        self.cactus2Y = 215
        self.cactus3Y = 215
        self.DINO_WIDTH = 50
        self.DINO_HEIGHT = 52
        self.DINO_DOWN_WIDTH = 63
        self.DINO_DOWN_HEIGHT = 34
        self.SINGLE_CACTUS_WIDTH = 31
        self.DOUBLE_CACTUS_WIDTH = 61
        self.TRIPLE_CACTUS_WIDTH = 62
        self.CACTUS_HEIGHT = 60
        self.BIRD_WIDTH = 51
        self.BIRD_UP_HEIGHT = 33
        self.BIRD_DOWN_HEIGHT = 37

        # Fonts
        self.text_color = (0, 0, 0)
        self.large_font = pygame.font.SysFont("Courier", 60)
        self.small_font = pygame.font.SysFont("Arial", 30)

        # Load cactus images
        single_cactus_img_raw = pygame.image.load(os.path.join(self.folder, "single_cactus.png"))
        double_cactus_img_raw = pygame.image.load(os.path.join(self.folder, "double_cactus.png"))
        triple_cactus_img_raw = pygame.image.load(os.path.join(self.folder, "triple_cactus.png"))
        self.single_cactus_img = pygame.transform.scale(single_cactus_img_raw, (31, 60))
        self.double_cactus_img = pygame.transform.scale(double_cactus_img_raw, (61, 60))
        self.triple_cactus_img = pygame.transform.scale(triple_cactus_img_raw, (62, 60))
        self.cactus_imgs = (self.single_cactus_img, self.double_cactus_img, self.triple_cactus_img)
        self.cactus1_hitbox = pygame.Rect(self.cactus1X, self.cactus1Y, self.SINGLE_CACTUS_WIDTH, self.CACTUS_HEIGHT)
        self.cactus2_hitbox = pygame.Rect(self.cactus2X, self.cactus2Y, self.TRIPLE_CACTUS_WIDTH, self.CACTUS_HEIGHT)
        self.cactus3_hitbox = pygame.Rect(self.cactus3X, self.cactus3Y, self.DOUBLE_CACTUS_WIDTH, self.CACTUS_HEIGHT)
        self.cactus1_sprite_img = self.cactus_imgs[0]
        self.cactus2_sprite_img = self.cactus_imgs[2]
        self.cactus3_sprite_img = self.cactus_imgs[1]

        # Load dino images
        self.dino_img_default = pygame.image.load(os.path.join(self.folder, "trex.png"))
        self.dino_img_left = pygame.image.load(os.path.join(self.folder, "trex_left.png"))
        self.dino_img_right = pygame.image.load(os.path.join(self.folder, "trex_right.png"))
        self.dino_img_down_left = pygame.image.load(os.path.join(self.folder, "trex_down_left.png"))
        self.dino_img_down_right = pygame.image.load(os.path.join(self.folder, "trex_down_right.png"))
        self.dino_hitbox = pygame.Rect(self.dinoX + 3, self.dinoY - 3, self.DINO_WIDTH - 13, self.DINO_HEIGHT - 5)
        self.dino_sprite_img = self.dino_img_default

        # Load bird images
        bird_down_raw = pygame.image.load(os.path.join(self.folder, "bird_down.png"))
        bird_up_raw = pygame.image.load(os.path.join(self.folder, "bird_up.png"))
        self.bird_down = pygame.transform.scale(bird_down_raw, (51, 37))
        self.bird_up = pygame.transform.scale(bird_up_raw, (51, 33))

        # Pre-render static UI text
        self.game_over_text = self.large_font.render("Game over", False, self.text_color)
        self.restart_text = self.small_font.render(f"Press Space to restart", False, self.text_color)

    # Check if a text file is empty
    def is_empty(self, file):
        return os.stat(file).st_size == 0
    
    # Encrypt the high score (simple obfuscation)
    def encrypt(self, num):
        digits = [chr(int(d) + self.key) for d in str(num)]
        return ''.join(reversed(digits))

    # Decrypt the high score
    def decrypt(self, text):
        digits = [str(ord(c) - self.key) for c in reversed(text)]
        return int(''.join(digits))

    # Load high score
    def load_high_score(self):
        high_score_path = os.path.join(self.folder, "high_score.txt")
        open(high_score_path, "a").close()
        if not self.is_empty(high_score_path):
            with open(high_score_path, "r") as high_score_file:
                raw = high_score_file.read().strip()
                if raw:
                    try:
                        self.high_score = self.decrypt(raw)
                    except Exception:
                        self.high_score = 0

    # Save high score if beaten
    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = int(self.score)
            with open(os.path.join(self.folder, "high_score.txt"), "w") as high_score_file:
                high_score_file.write(self.encrypt(self.high_score))
    
    # Exit the game
    def exit_game(self):
        self.save_high_score()
        pygame.quit()
        sys.exit()
    
    # Start the game
    def start_game(self):
        self.load_high_score()
        self.start_screen_loop()
        
    # Game over
    def game_over(self):
        self.save_high_score()
        self.game_over_loop()

    def start_screen_loop(self):
        
        # UI text
        dino_runner_text = self.large_font.render("Dino runner", False, self.text_color)
        start_text = self.small_font.render(f"Press the Jump key", False, self.text_color)
        high_score_text = self.small_font.render(f"High score: {self.high_score}", False, self.text_color)
        
        while True:
            
            # Cap frame rate
            self.clock.tick(60)
            
            # Clear screen
            self.window.fill((255, 255, 255))
            
            # Draw UI text
            self.window.blit(dino_runner_text , (140, 50))
            self.window.blit(start_text, (225, 125))
            self.window.blit(high_score_text, (240, 170))
            
            # Event handling
            for event in pygame.event.get():
                    
                # Window close
                if event.type == pygame.QUIT:
                    self.exit_game()
                    return
            
                # Start game keybinds; Esc exits
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
            
            # Flip buffers
            pygame.display.update()
    
    def game_loop(self):
        # Initialize variables
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

        # Reset variables
        self.dinoX = 75
        self.dinoY = 223
        self.cactus1X = 900
        self.cactus2X = 1500
        self.cactus3X = 2100
        self.cactus1Y = 215
        self.cactus2Y = 215
        self.cactus3Y = 215
        self.score = 0
        self.cactus1_sprite_img = self.cactus_imgs[0]
        self.cactus2_sprite_img = self.cactus_imgs[2]
        self.cactus3_sprite_img = self.cactus_imgs[1]
        self.dino_sprite_img = self.dino_img_default

        while True:
            # Cap frame rate
            self.clock.tick(60)

            # Input
            grounded = self.dinoY >= 223
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        if grounded:
                            fall_speed = -JUMP_STRENGTH
                    elif event.key == pygame.K_ESCAPE:
                        self.exit_game()
                        return
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        sliding = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        sliding = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and grounded:
                        fall_speed = -JUMP_STRENGTH
                    elif event.button == 3:
                        sliding = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        sliding = False

            # Physics update
            self.dinoY += fall_speed

            # Ground clamp and animation state
            if self.dinoY >= 223:
                grounded = True
                self.dinoY = 223
                fall_speed = 0
                animation_counter += 1
                if not sliding:
                    if animation_counter // 5 % 2 == 0:
                        self.dino_sprite_img = self.dino_img_left
                    else:
                        self.dino_sprite_img = self.dino_img_right
                else:
                    self.dinoY = 241
                    if animation_counter // 5 % 2 == 0:
                        self.dino_sprite_img = self.dino_img_down_left
                    else:
                        self.dino_sprite_img = self.dino_img_down_right
            else:
                grounded = False
                fall_speed += GRAVITY
                self.dino_sprite_img = self.dino_img_default

            # Dino hitbox
            if grounded and sliding:
                dino_rect = pygame.Rect(self.dinoX, self.dinoY, self.DINO_DOWN_WIDTH - 3, self.DINO_DOWN_HEIGHT)
            else:
                dino_rect = pygame.Rect(self.dinoX + 3, self.dinoY - 3, self.DINO_WIDTH - 13, self.DINO_HEIGHT - 5)
            self.dino_hitbox = dino_rect

            # Move obstacles
            self.cactus1X -= CACTUS_SPEED
            self.cactus2X -= CACTUS_SPEED
            self.cactus3X -= CACTUS_SPEED

            # Respawn logic
            if self.cactus1X < -60:
                self.cactus1X = self.cactus3X + random.randint(500, 700)
                num = random.randint(1, 3)
                if num == 1 or num == 2 or self.score < 150:
                    cactus1_bird = False
                    self.cactus1Y = 215
                    num1 = random.randint(0, 2)
                    self.cactus1_sprite_img = self.cactus_imgs[num1]
                else:
                    cactus1_bird = True

            if self.cactus2X < -60:
                self.cactus2X = self.cactus1X + random.randint(500, 700)
                num = random.randint(1, 3)
                if num == 1 or num == 2 or self.score < 150:
                    cactus2_bird = False
                    self.cactus2Y = 215
                    num1 = random.randint(0, 2)
                    self.cactus2_sprite_img = self.cactus_imgs[num1]
                else:
                    cactus2_bird = True

            if self.cactus3X < -60:
                self.cactus3X = self.cactus2X + random.randint(500, 700)
                num = random.randint(1, 3)
                if num == 1 or num == 2 or self.score < 150:
                    cactus3_bird = False
                    self.cactus3Y = 215
                    num1 = random.randint(0, 2)
                    self.cactus3_sprite_img = self.cactus_imgs[num1]
                else:
                    cactus3_bird = True

            # Bird animation
            if cactus1_bird:
                self.cactus1Y = 190
                animation_counter1 += 1
                if animation_counter1 // 10 % 2 == 0:
                    self.cactus1_sprite_img = self.bird_up
                else:
                    self.cactus1_sprite_img = self.bird_down

            if cactus2_bird:
                self.cactus2Y = 190
                animation_counter2 += 1
                if animation_counter2 // 10 % 2 == 0:
                    self.cactus2_sprite_img = self.bird_up
                else:
                    self.cactus2_sprite_img = self.bird_down

            if cactus3_bird:
                self.cactus3Y = 190
                animation_counter3 += 1
                if animation_counter3 // 10 % 2 == 0:
                    self.cactus3_sprite_img = self.bird_up
                else:
                    self.cactus3_sprite_img = self.bird_down

            # Compute obstacle hitboxes for current sprites
            cactusX_list = (self.cactus1X, self.cactus2X, self.cactus3X)
            cactusY_list = (self.cactus1Y, self.cactus2Y, self.cactus3Y)
            cactus_img_hitboxes = (self.cactus1_sprite_img, self.cactus2_sprite_img, self.cactus3_sprite_img)
            cactus_hitboxes = [self.cactus1_hitbox, self.cactus2_hitbox, self.cactus3_hitbox]
            for inx, img in enumerate(cactus_img_hitboxes):
                if img == self.single_cactus_img:
                    cactus_hitboxes[inx] = pygame.Rect(cactusX_list[inx] + 13, cactusY_list[inx] + 3, self.SINGLE_CACTUS_WIDTH, self.CACTUS_HEIGHT)
                elif img == self.double_cactus_img:
                    cactus_hitboxes[inx] = pygame.Rect(cactusX_list[inx] + 13, cactusY_list[inx] + 3, self.DOUBLE_CACTUS_WIDTH, self.CACTUS_HEIGHT)
                elif img == self.triple_cactus_img:
                    cactus_hitboxes[inx] = pygame.Rect(cactusX_list[inx] + 15, cactusY_list[inx] + 5, self.TRIPLE_CACTUS_WIDTH, self.CACTUS_HEIGHT)
                elif img == self.bird_down:
                    cactus_hitboxes[inx] = pygame.Rect(cactusX_list[inx] + 10, cactusY_list[inx], self.BIRD_WIDTH, self.BIRD_DOWN_HEIGHT)
                elif img == self.bird_up:
                    cactus_hitboxes[inx] = pygame.Rect(cactusX_list[inx] + 10, cactusY_list[inx], self.BIRD_WIDTH, self.BIRD_UP_HEIGHT)
            self.cactus1_hitbox = cactus_hitboxes[0]
            self.cactus2_hitbox = cactus_hitboxes[1]
            self.cactus3_hitbox = cactus_hitboxes[2]

            # Collision check
            if (self.dino_hitbox.colliderect(self.cactus1_hitbox) or
                self.dino_hitbox.colliderect(self.cactus2_hitbox) or
                self.dino_hitbox.colliderect(self.cactus3_hitbox)):
                self.game_over()
                return

            # Score
            self.score += 0.2

            # Render
            self.window.fill((255, 255, 255))
            pygame.draw.line(self.window, (0, 0, 0), (0, 275), (700, 275), width=2)
            self.window.blit(self.dino_sprite_img, (self.dinoX, self.dinoY))
            self.window.blit(self.cactus1_sprite_img, (self.cactus1X, self.cactus1Y))
            self.window.blit(self.cactus2_sprite_img, (self.cactus2X, self.cactus2Y))
            self.window.blit(self.cactus3_sprite_img, (self.cactus3X, self.cactus3Y))
            score_text = self.small_font.render(f"Score: {int(self.score)}", False, self.text_color)
            self.window.blit(score_text, (500, 30))
            pygame.display.update()
            
    # Game over loop 
    def game_over_loop(self):

        # Refresh score UI text
        score_text = self.small_font.render(f"Score: {int(self.score)}", False, self.text_color)
        high_score_text = self.small_font.render(f"High score: {self.high_score}", False, self.text_color)
        
        while True:
            
            # Cap frame rate
            self.clock.tick(60)
            
            # Clear screen
            self.window.fill((255, 255, 255))
            
            # Draw UI text
            self.window.blit(self.game_over_text, (185, 50))
            self.window.blit(self.restart_text, (225, 125))
            self.window.blit(score_text, (285, 180))
            self.window.blit(high_score_text, (255, 230))
            
            # Event handling
            for event in pygame.event.get():
                    
                # Window close
                if event.type == pygame.QUIT:
                    self.exit_game()
                    return

                # Restart/quit bindings
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_loop()
                        return
                        
                    elif event.key == pygame.K_ESCAPE:
                        self.exit_game()
                        return
            
            # Flip buffers
            pygame.display.update() 

game = DinoRunner()
game.start_game()