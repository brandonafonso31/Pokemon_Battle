import os
#print(os.getcwd())
import pygame
from pygame.locals import *
from sprite import *
from pokemon_init import *
from pokemon_battle import *
from battle_attack import *
from button import *
from ui_battle import *

#------|Init pygame
pygame.init()
pygame.mixer.init()
 
#------|Resolution
res_scene = (1050,540)
resolution = (res_scene[0],260+res_scene[1])
window = pygame.display.set_mode(resolution)
pygame.display.set_caption("Pokemon Battle")

#------|Fonts
font = pygame.font.SysFont("arialblack",40)
WHITE = (255,255,255)
BLACK=(0,0,0)

#------|Button
attack_img = pygame.image.load("battle_ui/button_attack.png").convert_alpha()
pokemon_img = pygame.image.load("battle_ui/button_pokemon.png").convert_alpha()
bag_img = pygame.image.load("battle_ui/button_bag.png").convert_alpha()

move1_img = pygame.image.load('battle_ui/move1_button.png').convert_alpha()
move2_img = pygame.image.load('battle_ui/move2_button.png').convert_alpha()
move3_img = pygame.image.load('battle_ui/move3_button.png').convert_alpha()
move4_img = pygame.image.load('battle_ui/move4_button.png').convert_alpha()

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

def perform_choice_attack(pokemon_trainer, pokemon_opponent, move_id):
    pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
    pygame.display.flip()
    pokemon_trainer, pokemon_opponent, in_battle = turn(pokemon_trainer, pokemon_opponent, move_id)
    choose_action = in_battle
    attack_selected = False
    run = in_battle     # run = *False on stoppe car le combat est finis
    battle_start = run
    pygame.time.delay(500)
    return pokemon_trainer, pokemon_opponent, in_battle, choose_action, attack_selected, run, battle_start
    
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
        #------|Musique
        pygame.mixer.music.load('song/elite_four/2-29. Battle! Elite Four.mp3')
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.3)
        pokemon_trainer,pokemon_opponent,window = start_battle(window,resolution)
        in_battle = True
        choose_action = True
    
    # battle    
    if in_battle:
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
            pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
            
            moves = pokemon_trainer.get_moveset()
            if moves[0] is not None and draw_move(window,moves[0],x_move - 200, y_menu + 50):
                pokemon_trainer, pokemon_opponent, in_battle, choose_action, attack_selected, run, battle_start = perform_choice_attack(pokemon_trainer, pokemon_opponent, "move1")                            
            if moves[1] is not None and draw_move(window,moves[1],x_move + 200, y_menu + 50):
                pokemon_trainer, pokemon_opponent, in_battle, choose_action, attack_selected, run, battle_start = perform_choice_attack(pokemon_trainer, pokemon_opponent, "move2")                
            if moves[2] is not None and draw_move(window,moves[2],x_move - 200, y_menu + 150):
                pokemon_trainer, pokemon_opponent, in_battle, choose_action, attack_selected, run, battle_start = perform_choice_attack(pokemon_trainer, pokemon_opponent, "move3")                
            if moves[3] is not None and draw_move(window,moves[3],x_move + 200, y_menu + 150):
                pokemon_trainer, pokemon_opponent, in_battle, choose_action, attack_selected, run, battle_start = perform_choice_attack(pokemon_trainer, pokemon_opponent, "move4")
        
        # façon très sale de parer au pb des deux boutons qui s'affichent avant que l'app ne se ferme
        if not run:
            break
             
        if pokemon_selected:
            pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
            # open_pokemon_team()
            pokemon_selected = False
            choose_action = True
        
        if bag_selected:
            pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
            # open_bag()
            bag_selected = False
            choose_action = True
        
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
pygame.time.delay(2000)
pygame.quit()
exit()