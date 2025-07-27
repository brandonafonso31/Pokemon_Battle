import os
#print(os.getcwd())
import pygame
from pygame.locals import *
from pokemon_init import *
import pokemon_battle
from button import Button
import ui_battle
from config import *

#------|Init pygame
pygame.init()
pygame.mixer.init()
 
#------|Resolution
res_scene = (1050,540)
resolution = (res_scene[0],260+res_scene[1])
window = pygame.display.set_mode(resolution)
pygame.display.set_caption("Pokemon Battle")
pygame.display.set_icon(pygame.image.load(os.path.join(img_dir_path,"sys/pokeball.png")))

#------|Fonts
font = pygame.font.SysFont("arialblack",40)

#------|Button
attack_img = pygame.image.load(os.path.join(img_dir_path,"battle_ui/button_attack.png")).convert_alpha()
pokemon_img = pygame.image.load(os.path.join(img_dir_path,"battle_ui/button_pokemon.png")).convert_alpha()
bag_img = pygame.image.load(os.path.join(img_dir_path,"battle_ui/button_bag.png")).convert_alpha()

#------|create button instances
y_menu = resolution[1]-260
x_menu = resolution[0]-500
attack_button = Button(x_menu, y_menu + 5, attack_img, 1)
pokemon_button = Button(x_menu, y_menu + 95, pokemon_img, 1)
bag_button = Button(x_menu, y_menu + 185, bag_img, 1)
x_move = resolution[0]//2

#------|Functions
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))
    
#------|Variable
battle_start = False
in_battle = False
choose_action = False
attack_selected = False
pokemon_selected = False
bag_selected = False

#------|Boucle qui fait tourner le jeu  
run = True
while run :
    #check les variables afin de faire divers actions
    if battle_start and not in_battle:
        pokemon_trainer,pokemon_opponent,window = pokemon_battle.start_battle(window,resolution)
        in_battle = True
        choose_action = True
        
    if in_battle:
        #refresh_screen(window,resolution)
        
        if choose_action: 
            pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))   
            if attack_button.draw(window):
                choose_action = False
                attack_selected = True
                
            if pokemon_button.draw(window):
                pokemon_selected = True
                choose_action = False
            if bag_button.draw(window):
                bag_selected = True
                choose_action = False
            
        if attack_selected:
            pokemon_trainer, pokemon_opponent, in_battle, choose_action,\
                attack_selected, run, battle_start, window = ui_battle.choice_move(window,res_scene,resolution,x_move,y_menu,pokemon_trainer,pokemon_opponent)
        
        # façon très sale de parer au pb des deux boutons qui s'affichent avant que l'app ne se ferme
        if not run:
            break
             
        if pokemon_selected:
            pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
            # open_pokemon_team()
            pokemon_selected = False
            choose_action = True
            draw_text("LA TEAM POKEMON EST SELECTIONNEE", font,WHITE,250,resolution[1]//2)
        
        if bag_selected:
            pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
            # open_bag()
            bag_selected = False
            choose_action = True
            draw_text("LE SAC EST SELECTIONNE", font,WHITE,100,resolution[1]//2)
            
    if not battle_start and run:
        pygame.time.delay(500)
        window.fill((0,0,0))
        pygame.mixer.music.stop()        
        
        draw_text("Press left click to start battle",font,WHITE,250,resolution[1]//2)
     
    #event handler
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            battle_start = True
                    
    pygame.display.update()
    
pygame.mixer.music.stop()
pygame.time.delay(1000)
pygame.quit()
exit()