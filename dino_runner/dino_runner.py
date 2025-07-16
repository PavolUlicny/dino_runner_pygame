#imports
import pygame
import os
import sys
import random

#variables
global running, start_screen
window_width=700
window_height=350
running=False
folder="python/dino_runner"
jump_strength=9
gravity=0.5
fall_speed=0
dinox=75
dinoy=223
cactus1y=215
cactus2y=215
cactus3y=215
cactus1x=900
cactus2x=1500
cactus3x=2100
cactus_speed=10
grounded=True
score=0
cactus_height=50
dino_width=50
dino_height=52
animation_counter=0
animation_counter1=0
animation_counter2=0
animation_counter3=0
sliding=False
cactus1_bird=False
cactus2_bird=False
cactus3_bird=False
dino_width=50
dino_height=52
dino_down_width=63
dino_down_height=34
single_cactus_width=31
cactus_height=60
double_cactus_width=61
triple_cactus_width=55
bird_width=51
bird_up_height=33
bird_down_height=37
start_screen=True
high_score=0
clock=pygame.time.Clock()

#func that checks if a txt file is empty
def is_empty(file):
    if os.stat(file).st_size>0:
        return False
    else:
        return True
    
#func for encrypting a num
def encrypt(num):
    list1=list(str(num))
    list1=[int(s) for s in list1]
    list2=[]
    str1=""
    for i in list1:
        list2.append(chr(i+110))
    list2.reverse()
    for i in list2:
        str1+=i
    return str1

#func for deencrypting a num
def deencrypt(text):
    list1=list(text)
    list2=[]
    str1=""
    num=0
    for i in list1:
        list2.append(ord(i)-110)
    list2.reverse()
    for i in list2:
        str1+=str(i)
    return int(str1)

#load high score 
high_score_file=open(f"{folder}/high_score.txt", "a")
high_score_file.close()
if not is_empty(f"{folder}/high_score.txt"):
    high_score_file=open(f"{folder}/high_score.txt", "r")
    high_score=int(deencrypt(high_score_file.read()))
    high_score_file.close()

#load dino images
dino_img_def=pygame.image.load((f"{folder}/trex.png"))
dino_img_left=pygame.image.load((f"{folder}/trex_left.png"))
dino_img_right=pygame.image.load((f"{folder}/trex_right.png"))
dino_img_down_left=pygame.image.load((f"{folder}/trex_down_left.png"))
dino_img_down_right=pygame.image.load((f"{folder}/trex_down_right.png"))
dino_img=dino_img_def
dino_hit=pygame.Rect(dinox+3,dinoy-3,dino_width-13,dino_height-5)

#load cactus images 
single_cactus_img1=pygame.image.load((f"{folder}/single_cactus.png"))
double_cactus_img1=pygame.image.load((f"{folder}/double_cactus.png"))
triple_cactus_img1=pygame.image.load((f"{folder}/triple_cactus.png"))
single_cactus_img=pygame.transform.scale(single_cactus_img1,(31,60))
double_cactus_img=pygame.transform.scale(double_cactus_img1,(61,60))
triple_cactus_img=pygame.transform.scale(triple_cactus_img1,(62,60))
cactus_imgs=(single_cactus_img,double_cactus_img,triple_cactus_img)
cactus1_img=cactus_imgs[0]
cactus2_img=cactus_imgs[2]
cactus3_img=cactus_imgs[1]
cactus1_hit=pygame.Rect(cactus1x,cactus1y,single_cactus_width,cactus_height)
cactus2_hit=pygame.Rect(cactus2x,cactus2y,triple_cactus_width,cactus_height)
cactus3_hit=pygame.Rect(cactus3x,cactus3y,double_cactus_width,cactus_height)
cactus_img_hitboxes=(cactus1_img,cactus2_img,cactus3_img)
cactus_hitboxes=[cactus1_hit,cactus2_hit,cactus3_hit]
cactus_x=(cactus1x,cactus2x,cactus3x)
cactus_y=(cactus1y,cactus2y,cactus3y)

#load bird images
bird_down1=pygame.image.load((f"{folder}/bird_down.png"))
bird_up1=pygame.image.load((f"{folder}/bird_up.png"))
bird_down=pygame.transform.scale(bird_down1,(51,37))
bird_up=pygame.transform.scale(bird_up1,(51,33))

#game over function
def game_over():
    global running,score,high_score
    running=False
    if score>high_score:
        high_score=score
        high_score_file=open(f"{folder}/high_score.txt", "w")
        high_score_file.write(encrypt(int(high_score)))
        high_score_file.close()

#restart function
def restart_func():
    global running,dino_img,dino_img_def,dino_hit,dinox,dinoy,cactus1y,cactus2y,cactus3y,cactus1x,cactus2x,cactus3x,cactus_speed,grounded,fall_speed,score,animation_counter,animation_counter1,animation_counter2,animation_counter3,sliding,cactus1_bird,cactus2_bird,cactus3_bird,dino_width,dino_height,cactus1_img,cactus2_img,cactus3_img,cactus_imgs,cactus1_hit,cactus2_hit,cactus3_hit,cactus_height,single_cactus_width,double_cactus_width,triple_cactus_width,cactus_img_hitboxes,cactus_x,cactus_y,cactus_hitboxes
    running=True
    fall_speed=0
    dinox=75
    dinoy=223
    cactus1y=215
    cactus2y=215
    cactus3y=215
    cactus1x=900
    cactus2x=1500
    cactus3x=2100
    cactus_speed=10
    grounded=True
    score=0
    animation_counter=0
    animation_counter1=0
    animation_counter2=0
    animation_counter3=0
    sliding=False
    cactus1_bird=False
    cactus2_bird=False
    cactus3_bird=False
    dino_img=dino_img_def
    dino_hit=pygame.Rect(dinox+3,dinoy-3,dino_width-13,dino_height-5)
    cactus_img_hitboxes=(cactus1_img,cactus2_img,cactus3_img)
    cactus_hitboxes=[cactus1_hit,cactus2_hit,cactus3_hit]
    cactus_x=(cactus1x,cactus2x,cactus3x)
    cactus_y=(cactus1y,cactus2y,cactus3y)
    cactus1_img=cactus_imgs[0]
    cactus2_img=cactus_imgs[2]
    cactus3_img=cactus_imgs[1]
    cactus1_hit=pygame.Rect(cactus1x,cactus1y,single_cactus_width,cactus_height)
    cactus2_hit=pygame.Rect(cactus2x,cactus2y,triple_cactus_width,cactus_height)
    cactus3_hit=pygame.Rect(cactus3x,cactus3y,double_cactus_width,cactus_height)

#initialize pygame
pygame.init()

#create window
window1=pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Dino runner")

#fonts and texts
text_color=(0,0,0)
font1=pygame.font.SysFont("Courier",60)
font2=pygame.font.SysFont("Arial",30)
score_text=font2.render(f"Score: {int(score)}",False,text_color)
dino_runner_text=font1.render("Dino runner",False,text_color)
start_text=font2.render(f"Press the Jump key",False,text_color)
game_over_text=font1.render("Game over",False,text_color)
restart_text=font2.render(f"Press Space to restart",False,text_color)
high_score_text=font2.render(f"High score: {int(high_score)}",False,text_color)

#starting screen 
while start_screen and not running:
    
    #set fps
    clock.tick(60)
    
    #fill window with white color
    window1.fill((255,255,255))
    
    #text
    window1.blit(dino_runner_text,(140,50))
    window1.blit(start_text,(225,125))
    high_score_text=font2.render(f"High score: {int(high_score)}",False,text_color)
    window1.blit(high_score_text,(240,170))
    
    #check for events
    for event in pygame.event.get():
            
        #close the game if the window is closed
        if event.type==pygame.QUIT:
            start_screen=False
            pygame.quit()
            sys.exit()
    
        #binds keys to start game
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w or event.key==pygame.K_UP:
                start_screen=False
                running=True

        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                start_screen=False
                running=True
    
    
    #update display
    pygame.display.update()
    
while True:
    #main loop
    while running and not start_screen:
        
        #set fps
        clock.tick(60)
        
        #fill window with white color
        window1.fill((255,255,255))
        
        #create the ground line
        pygame.draw.line(window1,(0,0,0),(0,275),(700,275),width=2)
        
        #load images into the window
        window1.blit(dino_img,(dinox,dinoy))
        window1.blit(cactus1_img,(cactus1x,cactus1y))
        window1.blit(cactus2_img,(cactus2x,cactus2y))
        window1.blit(cactus3_img,(cactus3x,cactus3y))
        
        #load texts
        score_text=font2.render(f"Score: {int(score)}",False,text_color)
        window1.blit(score_text,(500,30))
        
        #apply jump/fall physics to dino
        dinoy+=fall_speed
        
        #make the cacti move 
        cactus1x-=cactus_speed
        cactus2x-=cactus_speed
        cactus3x-=cactus_speed
        
        #some lists and tuples
        cactus_x=(cactus1x,cactus2x,cactus3x)
        cactus_y=(cactus1y,cactus2y,cactus3y)
        cactus_img_hitboxes=(cactus1_img,cactus2_img,cactus3_img)
        cactus_hitboxes=[cactus1_hit,cactus2_hit,cactus3_hit]
        
        #return cacti if they go off screen
        if cactus1x<-60:
            cactus1x=cactus3x+random.randint(500,700)
            num=random.randint(1,3)
            if num==1 or num==2 or score<150:
                cactus1_bird=False
                cactus1y=215
                num1=random.randint(0,2)
                cactus1_img=cactus_imgs[num1]
            else:
                cactus1_bird=True
        if cactus2x<-60:
            cactus2x=cactus1x+random.randint(500,700)
            num=random.randint(1,3)
            if num==1 or num==2 or score<150:
                cactus2_bird=False
                cactus2y=215
                num1=random.randint(0,2)
                cactus2_img=cactus_imgs[num1]
            else:
                cactus2_bird=True
        if cactus3x<-60:
            cactus3x=cactus2x+random.randint(500,700)
            num=random.randint(1,3)
            if num==1 or num==2 or score<150:
                cactus3_bird=False
                cactus3y=215
                num1=random.randint(0,2)
                cactus3_img=cactus_imgs[num1]
            else:
                cactus3_bird=True
                
        #put bird img on cactus if its a bird
        if cactus1_bird:
            cactus1y=190
            animation_counter1+=1
            if animation_counter1//10%2==0:
                cactus1_img=bird_up
            else:
                cactus1_img=bird_down
        if cactus2_bird:
            cactus2y=190
            animation_counter2+=1
            if animation_counter2//10%2==0:
                cactus2_img=bird_up
            else:
                cactus2_img=bird_down
        if cactus3_bird:
            cactus3y=190
            animation_counter3+=1
            if animation_counter3//10%2==0:
                cactus3_img=bird_up
            else:
                cactus3_img=bird_down
                
        #hitboxes
        dino_def_rect=pygame.Rect(dinox+3,dinoy-3,dino_width-13,dino_height-5)
        dino_down_rect=pygame.Rect(dinox,dinoy,dino_down_width-3,dino_down_height)
        for inx,img in enumerate(cactus_img_hitboxes):
            if img==single_cactus_img:
                cactus_hitboxes[inx]=pygame.Rect(cactus_x[inx]+13,cactus_y[inx]+3,single_cactus_width,cactus_height)
            elif img==double_cactus_img:
                cactus_hitboxes[inx]=pygame.Rect(cactus_x[inx]+13,cactus_y[inx]+3,double_cactus_width,cactus_height)
            elif img==triple_cactus_img:
                cactus_hitboxes[inx]=pygame.Rect(cactus_x[inx]+15,cactus_y[inx]+5,triple_cactus_width,cactus_height)
            elif img==bird_down:
                cactus_hitboxes[inx]=pygame.Rect(cactus_x[inx]+10,cactus_y[inx],bird_width,bird_down_height)
            elif img==bird_up:
                cactus_hitboxes[inx]=pygame.Rect(cactus_x[inx]+10,cactus_y[inx],bird_width,bird_up_height)
        cactus1_hit=cactus_hitboxes[0]
        cactus2_hit=cactus_hitboxes[1]
        cactus3_hit=cactus_hitboxes[2]
        
        #check for collision
        if dino_hit.colliderect(cactus1_hit) or dino_hit.colliderect(cactus2_hit) or dino_hit.colliderect(cactus3_hit):
            game_over()
        
        #increase score
        score+=0.2

        #check if dino is touching the ground (if hes under the ground, put him on the ground) and changing his img
        if dinoy>=223:
            grounded=True
            dinoy=223
            fall_speed=0
            animation_counter+=1
            if not sliding:
                dino_hit=dino_def_rect
                dinoy=223
                if animation_counter//5%2==0:
                    dino_img=dino_img_left
                else:
                    dino_img=dino_img_right
            else:
                dino_hit=dino_down_rect
                dinoy=241
                if animation_counter//5%2==0:
                    dino_img=dino_img_down_left
                else:
                    dino_img=dino_img_down_right
        else:
            dino_hit=dino_def_rect
            grounded=False
            fall_speed+=gravity
            dino_img=dino_img_def
            
        #check for events
        for event in pygame.event.get():
                
            #close the game if the window is closed
            if event.type==pygame.QUIT:
                start_screen=False
                pygame.quit()
                sys.exit()

            #binds keys to jump
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_w or event.key==pygame.K_UP:
                    if grounded:
                        fall_speed=-jump_strength
                
                elif event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
                elif event.key==pygame.K_DOWN or event.key==pygame.K_s:
                    sliding=True  
                        
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if grounded:
                        fall_speed=-jump_strength
                        
                if event.button==3:
                    sliding=True
                        
            #binds key to slide
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_DOWN or event.key==pygame.K_s:
                    sliding=False
            if event.type==pygame.MOUSEBUTTONUP:
                sliding=False
    
        #update display
        pygame.display.update()
        
    #game over loop 

    while not running and not start_screen:
        
        #set fps
        clock.tick(60)
        
        #fill window with white color
        window1.fill((255,255,255))
        
        #text
        window1.blit(game_over_text,(185,50))
        window1.blit(restart_text,(225,125))
        score_text=font2.render(f"Score: {int(score)}",False,text_color)
        window1.blit(score_text,(285,180))
        high_score_text=font2.render(f"High score: {int(high_score)}",False,text_color)
        window1.blit(high_score_text,(245,230))
        
        #check for events
        for event in pygame.event.get():
                
            #close the game if the window is closed
            if event.type==pygame.QUIT:
                start_screen=False
                pygame.quit()
                sys.exit()

            #binds keys to start game
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    restart_func()
                elif event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        #update display
        pygame.display.update() 