import os,sys,pygame,pokemon_battle,ui_battle,json,sprite,pokemon_trainer,utils
from config import *
from pygame.locals import *

#------|Init pygame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
dt = 0

#------|Resolution
window = pygame.display.set_mode(resolution,vsync=1)
pygame.display.set_caption(project_name)
pygame.display.set_icon(pygame.image.load(os.path.join(img_dir_path,"sys/logo.png")))

#------|Fonts
font = pygame.font.Font(font_path, 40)
            
#------|Var
BACKGROUND_INTRO = pygame.image.load(os.path.join(sys_dir_path,"intro.jpg"))
BACKGROUND_LENGHT,BACKGROUND_HEIGHT = BACKGROUND_INTRO.get_size()
ratio = res_screen_top[0] / BACKGROUND_LENGHT
ratio2 = res_screen_top[1] / BACKGROUND_HEIGHT
scale = (BACKGROUND_LENGHT*ratio,BACKGROUND_HEIGHT*ratio2)
BACKGROUND_INTRO = pygame.transform.scale(BACKGROUND_INTRO,scale)

BACKGROUND_TITLE_IMAGE = pygame.image.load(os.path.join(sys_dir_path,"pokemon_logo.png"))
BACKGROUND_TITLE_IMAGE = pygame.transform.scale(BACKGROUND_TITLE_IMAGE,(BACKGROUND_TITLE_IMAGE.get_width()//5,BACKGROUND_TITLE_IMAGE.get_height()//5))

#------|Button
BUTTON_LENGTH,BUTTON_HEIGHT = 191,82    # taille du boutton sans texte : 191 x 82 par default

PLAY_BUTTON = utils.create_button("Jouer", (resolution[0] - BUTTON_LENGTH)//2 , res_screen_bottom[1] + black_band_res[1]+25)
OPTIONS_BUTTON = utils.create_button("Options", (resolution[0] - BUTTON_LENGTH)//2, res_screen_bottom[1] + black_band_res[1] + 175)
QUIT_BUTTON = utils.create_button("Quitter", (resolution[0] - BUTTON_LENGTH)//2, res_screen_bottom[1] + black_band_res[1] + 325)

ATTACK_BUTTON = utils.create_button("Attaquer", (resolution[0] - 191)//2, res_screen_bottom[1] + black_band_res[1] + 50)
POKEMON_BUTTON = utils.create_button("Pokémon", resolution[0] - 191 - 18, resolution[1] - 82 - 18)
BAG_BUTTON = utils.create_button("Sac", 18, resolution[1] - 82 - 18)
BACK_BUTTON = utils.create_button("Retour", (resolution[0] - 191)//2, resolution[1] - 82 - 18)


#------|function
def pokemon_team_menu(window,pokemon_player, pokemon_opponent):
    options_running = True
    while options_running :
        dt = clock.tick(30)
        window.fill(BLACK)
        
        utils.draw_text(window,"Pokemon Team", font, "#b68f40", res_screen_bottom[0]//2 - 200, res_screen_bottom[1]//2)

        for button in [BACK_BUTTON]:
            button.draw(window)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if BACK_BUTTON.handle_event(event):
                options_running = False

        pygame.display.flip()
    
    ui_battle.refresh_screen(window, pokemon_player, pokemon_opponent)
        
def bag_menu(window, pokemon_player, pokemon_opponent):
    options_running = True
    while options_running :
        dt = clock.tick(30)
        window.fill(BLACK)
        
        utils.draw_text(window,"Sac", font, "#b68f40", res_screen_bottom[0]//2 - 200, res_screen_bottom[1]//2)

        for button in [BACK_BUTTON]:
            button.draw(window)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if BACK_BUTTON.handle_event(event):
                options_running = False

        pygame.display.flip()
    
    ui_battle.refresh_screen(window, pokemon_player, pokemon_opponent)
        
def ko(window, pokemon_player, pokemon_opponent):
    print("entree dans KO menu")
    trainer = pokemon_player.trainer
    opponent = pokemon_opponent.trainer
    print(trainer.name,opponent.name)
    
    clock = pygame.time.Clock()
    elapsed = 0
    pokemon_ko, front_or_back = (pokemon_player, "back") if pokemon_player.hp <= 0 else (pokemon_opponent, "front")
    ko_running = True
    state = 0
    while ko_running:
        dt = clock.tick(30) / 1000
        elapsed += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # État 0 : afficher le message KO
        if state == 0 and elapsed >= 0.5:
            text = f"{pokemon_ko.name} {'ennemi' if pokemon_ko is pokemon_opponent else 'allié'} est KO"
            utils.print_log_ingame(window,text, reset = True)
            state = 1
            elapsed = 0
            
        # État 1 : jouer l'animation après 2s
        elif state == 1 and elapsed >= 2:
            pokemon_ko.animate_death(window, front_or_back)
            state = 2
            elapsed = 0 
            
        # État 2 : envoie du pokemon suivant après 4s apres le state 1
        elif state == 2 and elapsed >= 3: 
            if pokemon_ko is pokemon_player:
                new_pokemon = trainer.send_next(window,"back")
                if new_pokemon is None:
                    return new_pokemon,pokemon_opponent, False
                pokemon_player = new_pokemon
                text = f"{pokemon_player.name} est envoyé par {trainer.name} !"
                utils.print_log_ingame(window,text)
                ui_battle.refresh_player_side(window,pokemon_player)
            else:
                new_pokemon = opponent.send_next(window,"front")
                if new_pokemon is None:
                    return pokemon_player,pokemon_opponent, False
                pokemon_opponent = new_pokemon
                text = f"{pokemon_opponent.name} est envoyé par {opponent.name} !"
                utils.print_log_ingame(window,text)
                ui_battle.refresh_opponent_side(window,pokemon_opponent)
            state = 3
            elapsed = 0
        
        elif state == 3 and elapsed >= 2: 
            ko_running = False
            
        pygame.display.flip()
        
    window.blit(BACKGROUND_IMAGE_BOTTOM, (res_screen_bottom[0] - BACKGROUND_IMAGE_BOTTOM.get_width(), res_screen_bottom[1] + black_band_res[1]))
    return pokemon_player,pokemon_opponent,not(pokemon_player is None or pokemon_opponent is None)

def attack_menu(window, pokemon_player, pokemon_opponent):
    window.blit(BACKGROUND_IMAGE_BOTTOM, (res_screen_bottom[0] - BACKGROUND_IMAGE_BOTTOM.get_width(), res_screen_bottom[1] + black_band_res[1]))
    moves_available = pokemon_player.get_moveset()
        
    button_padding = 20
    center = (resolution[0]//2,resolution[1] - res_screen_bottom[1]//2)
    list_coord = [(center[0] - BUTTON_LENGTH - button_padding, center[1] - BUTTON_HEIGHT - button_padding),
                    (center[0] + button_padding, center[1] - BUTTON_HEIGHT - button_padding),
                    (center[0] - BUTTON_LENGTH - button_padding, center[1]),
                    (center[0] + button_padding, center[1])]
    
    turn_running = True
    battle_running = True
    while turn_running:
        dt = clock.tick(30)
        
        # --- créer boutons des attaques
        moves_button = [ui_battle.draw_move(window, move, coord[0], coord[1])
                        for move, coord in zip(moves_available, list_coord)]
        
        BACK_BUTTON.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- gestion des attaques
            for i, button in enumerate(moves_button):
                if button.handle_event(event):
                    pokemon_player, pokemon_opponent, battle_state = \
                        utils.start_turn(window, pokemon_player, pokemon_opponent, moves_available, i)
                    if battle_state != "choose_attack": 
                        if battle_state == "ko":
                            return ko(window, pokemon_player, pokemon_opponent)
                        elif battle_state == "continue":
                            print("personne n'est ko donc on continue")
                            window.blit(BACKGROUND_IMAGE_BOTTOM, (res_screen_bottom[0] - BACKGROUND_IMAGE_BOTTOM.get_width(), res_screen_bottom[1] + black_band_res[1]))
                            return pokemon_player, pokemon_opponent, battle_running 

            if BACK_BUTTON.handle_event(event):
                turn_running = False

        pygame.display.flip()
    window.blit(BACKGROUND_IMAGE_BOTTOM, (res_screen_bottom[0] - BACKGROUND_IMAGE_BOTTOM.get_width(), res_screen_bottom[1] + black_band_res[1]))
    return pokemon_player, pokemon_opponent, battle_running

def battle_menu(window):    
    #------|Variable
    battle_running = True
    trainer,opponent = pokemon_trainer.init_trainer()
    # random background()
    bg_path = os.path.join(background_dir_path,"bg-forest.png")
    pokemon_player,pokemon_opponent,window = pokemon_battle.start_battle(window,trainer,opponent,background=bg_path)
    elapsed = 0
    state =""
    while battle_running :
        dt = clock.tick(30) / 1000
        elapsed += dt
        window.blit(BACKGROUND_IMAGE_BOTTOM, (res_screen_bottom[0] - BACKGROUND_IMAGE_BOTTOM.get_width(), res_screen_bottom[1] + black_band_res[1]))
        
        if state != "ko" and state != "end":            
            text = f"Que dois faire {pokemon_player.name} ?"
            utils.print_log_ingame(window,text)
            for button in [ATTACK_BUTTON, BAG_BUTTON, POKEMON_BUTTON]:
                button.draw(window)
        
        elif state == "ko" and elapsed >= 2:
            winner,loser = pokemon_trainer.get_winner(trainer,opponent)
            text = f"{winner.name} a vaincu {loser.name} !"
            utils.print_log_ingame(window,text)
            elapsed = 0
            state = "end"
        
        elif state == "end" and elapsed >= 2:
            battle_running = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ATTACK_BUTTON.handle_event(event):
                pokemon_player,pokemon_opponent,battle_running = \
                    attack_menu(window,pokemon_player,pokemon_opponent)
                if not battle_running: 
                    state = "ko"
                    battle_running = True
            if BAG_BUTTON.handle_event(event):
                bag_menu(window, pokemon_player, pokemon_opponent)
            if POKEMON_BUTTON.handle_event(event):
                pokemon_team_menu(window, pokemon_player, pokemon_opponent)

        pygame.display.flip()
         
def options_menu(window):
    options_running = True
    while options_running :
        dt = clock.tick(30)
        window.fill(BLACK)
        utils.fps_counter()
        
        utils.draw_text(window,"OPTIONS", font, "#b68f40", res_screen_bottom[0]//2 + 200, res_screen_bottom[1]//2)

        for button in [BACK_BUTTON]:
            button.draw(window)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if BACK_BUTTON.handle_event(event):
                options_running = False

        pygame.display.flip()

def main_menu(window):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join(song_dir_path,"sys/title.mp3"))
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.3)
    
    clock = pygame.time.Clock()
    run = True
    while run :
        dt = clock.tick(30)
        
        window.fill(BLACK)        
        window.blit(BACKGROUND_INTRO,(0,0))       
        window.blit(BACKGROUND_TITLE_IMAGE, ((res_screen_bottom[0] - BACKGROUND_TITLE_IMAGE.get_width())//2, 0))
        window.blit(BACKGROUND_IMAGE_BOTTOM, (res_screen_bottom[0] - BACKGROUND_IMAGE_BOTTOM.get_width(), res_screen_bottom[1] + black_band_res[1]))
        
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.draw(window)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if PLAY_BUTTON.handle_event(event):
                battle_menu(window)
                pygame.quit()
                sys.exit()
            if OPTIONS_BUTTON.handle_event(event):
                options_menu(window)
            if QUIT_BUTTON.handle_event(event):
                pygame.quit()
                sys.exit()

        pygame.display.flip()

main_menu(window)