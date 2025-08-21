import os,ui_battle,pokemon_battle,pygame
import battle_timing as bt
from config import *
from pygame.locals import *
from pokemon_init import *
from button import Button
from trainer import trainer,trainer_ai  # a deplacer dans un autre fichier

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
current_menu = ""
fight_continue = True
#------|Boucle qui fait tourner le jeu  
run = True
while run :
    
    if not battle_start and run:
        pygame.time.delay(500)
        window.fill((0,0,0))
        pygame.mixer.music.stop()
        draw_text("Press left click to start battle", font, WHITE,250,resolution[1]//2)
        
    #check les variables afin de faire divers actions
    if battle_start and not in_battle:
        pokemon_trainer,pokemon_opponent,window = pokemon_battle.start_battle(window,resolution)
        in_battle = True
        current_menu = "main"
        
    if in_battle:
        #refresh_screen(window,resolution)
        
        if current_menu == "main":
            with bt.timing_lock:
                current_timing = bt.Timing.Start
            pokemon_trainer,pokemon_opponent = bt.check_timing_talent(pokemon_trainer,pokemon_opponent) 
            pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))   
            if attack_button.draw(window):
                current_menu = "attack"
            elif pokemon_button.draw(window):
                current_menu = "team_pokemon"
            elif bag_button.draw(window):
                current_menu = "bag"
            
        elif current_menu == "attack":
            pokemon_trainer, pokemon_opponent, in_battle = ui_battle.choice_move(window,res_scene,resolution,x_move,y_menu,pokemon_trainer,pokemon_opponent)
            if in_battle == "ko":   # l'un des 2 pokemon est KO
                pygame.time.delay(500)
                pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
                pokemon_ko = pokemon_trainer if pokemon_trainer.hp <= 0 else pokemon_opponent
                draw_text(f"{pokemon_ko.name} {"ennemi" if pokemon_ko is pokemon_opponent else "allié"} est KO", font, WHITE, 100, 600)
                pygame.display.flip()
                pygame.time.delay(500)
                
                #animation de la mort du pokemon
                pokemon_ko.is_ko = True
                pokemon_ko.animate_death(window,front_or_back="back" if pokemon_ko is pokemon_trainer else "front")
                
                if pokemon_ko is pokemon_trainer:
                    pokemon_trainer,in_battle = trainer.send_next("back")
                else:
                    pokemon_opponent,in_battle = trainer_ai.send_next("front")
                
                if in_battle:
                    pygame.time.delay(1000)
                    ui_battle.refresh_screen(window, pokemon_trainer, pokemon_opponent)
                    pygame.time.delay(1000)
                    current_menu  = "main"
                    
                if not in_battle:
                    run = False
            
            elif in_battle == "continue":
                current_menu = "main"
            
            else:
                current_menu = "attack"
            
        elif current_menu == "team_pokemon":
            pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
            # open_pokemon_team()
            draw_text("LA TEAM POKEMON EST SELECTIONNEE", font, WHITE, 250, 600)
            pygame.display.flip()
            pygame.time.delay(500)
            current_menu = "main"
        
        elif current_menu == "bag":
            pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
            # open_bag()
            draw_text("LE SAC EST SELECTIONNE", font, WHITE, 100, 600)
            pygame.display.flip()
            pygame.time.delay(500)
            current_menu = "main"
     
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