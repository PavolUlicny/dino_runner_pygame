#imports
import pygame
import os
import sys

#variables
window_width=700
window_height=350
running=True
folder="dino_runner"
jump_strength=9.5
gravity=0.5
fall_speed=0
dinox=75
dinoy=223
grounded=True
score=0
cactus_height=50
dino_width=50
dino_height=52
animation_counter=0
clock=pygame.time.Clock()

#load dino images
dino_img_def=pygame.image.load((f"{folder}/trex.png"))
dino_img_left=pygame.image.load((f"{folder}/trex_left.png"))
dino_img_right=pygame.image.load((f"{folder}/trex_right.png"))
dino_img=dino_img_def

#initialize pygame
pygame.init()

#create window
window1=pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Dino runner")

#fonts and texts
#fonts and texts
text_color=(0,0,0)
font1=pygame.font.SysFont("Courier",60)
font2=pygame.font.SysFont("Arial",30)
score_text=font2.render(f"Score: {int(score)}",False,text_color)


#main loop
while running:
    
    #set fps
    clock.tick(60)
    
    #fill window with white color
    window1.fill((255,255,255))
    
    #create the ground line
    pygame.draw.line(window1,(0,0,0),(0,275),(700,275),width=2)
    
    #load images into the window
    window1.blit(dino_img,(dinox,dinoy))
    
    #load texts
    score_text=font2.render(f"Score: {int(score)}",False,text_color)
    window1.blit(score_text,(500,30))
    
    #apply jump/fall physics to dino
    dinoy+=fall_speed

    #increase score
    score+=0.2

    #check if dino is touching the ground (if hes under, put him on the ground)
    if dinoy>=223:
        grounded=True
        dinoy=223
        fall_speed=0
        animation_counter+=1
        if animation_counter//5%2==0:
            dino_img=dino_img_left
        else:
            dino_img=dino_img_right
    else:
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
            if event.key==pygame.K_SPACE or event.key==pygame.K_ESCAPE:
                if grounded:
                    fall_speed=-jump_strength
                    
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                if grounded:
                    fall_speed=-jump_strength
    
    pygame.display.update()

pygame.quit()
sys.exit()

#3 prekazky - rovnako ako flappy bird
#randomne menia img z tych troch ked prejdu spet 
#mozno neskor pridat aj sliding mechaniku + tie vtaky (keby som sa velmi nudil)
#vela stastia 
