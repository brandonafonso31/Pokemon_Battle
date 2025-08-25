import os,sys,pygame,pokemon_battle,ui_battle,json,sprite,pokemon_trainer
from config import project_name,img_dir_path,sys_dir_path,BLACK,WHITE,song_dir_path,background_dir_path,battle_json_path
from pygame.locals import *
from button_test import Button_test

#------|Init pygame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
dt = 0

#------|Resolution
res_scene = (753,500)
resolution = (res_scene[0],res_scene[1]+253)
window = pygame.display.set_mode(resolution,vsync=1)
pygame.display.set_caption(project_name)
pygame.display.set_icon(pygame.image.load(os.path.join(img_dir_path,"sys/logo.png")))

#------|Fonts
font = pygame.font.SysFont("arialblack",40)

#------|Utils
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

def create_button(text,x,y,path=""):
    if path == "":
        path = os.path.join(img_dir_path,"battle_ui/move_button.png")
    button_img = pygame.image.load(path).convert_alpha()
    return Button_test(x, y, button_img, 1, text)

def fps_counter():
    fps = str(int(clock.get_fps()))
    fps_t = font.render(f"{fps} fps" , 1, pygame.Color("RED"))
    window.blit(fps_t,(0,0))

def start_turn(window, pokemon_player, pokemon_opponent, moves, move_id):
    """Joue un tour de combat avec le move choisi et retourne l'état."""
    if moves[move_id].pp <= 0:
        print(f"{pokemon_player.name} n'a plus de PP pour {moves[move_id].name}")
        return pokemon_player, pokemon_opponent, True  # toujours en combat, mais pas d'action
    else:
        # Lance le tour de combat (animations, dégâts…)
        pokemon_player, pokemon_opponent, still_in_battle = \
            pokemon_battle.turn(pokemon_player, pokemon_opponent, f"move{move_id + 1}", window, res_scene, resolution)

        return pokemon_player, pokemon_opponent, still_in_battle      
            
#------|Var
y_menu = res_scene[1] + 50
x_menu = 50
BACKGROUND_INTRO = pygame.image.load(os.path.join(sys_dir_path,"intro.jpg"))
BACKGROUND_LENGHT,BACKGROUND_HEIGHT = BACKGROUND_INTRO.get_size()
ratio = resolution[0] / BACKGROUND_LENGHT
scale = (BACKGROUND_LENGHT*ratio,BACKGROUND_HEIGHT*ratio)
BACKGROUND_INTRO = pygame.transform.scale(BACKGROUND_INTRO,scale)
trainer,opponent = pokemon_trainer.init_trainer()
 
#------|Button
PLAY_BUTTON = create_button("Jouer", 200 ,200)
OPTIONS_BUTTON = create_button("Options", 200,300)
QUIT_BUTTON = create_button("Quitter", 200,400)

ATTACK_BUTTON = create_button("Attaquer", (resolution[0] - 191)//2, res_scene[1] + 18)
POKEMON_BUTTON = create_button("Pokémon", resolution[0] - 191 - 18, resolution[1] - 82 - 18)
BAG_BUTTON = create_button("Sac", 18, resolution[1] - 82 - 18)
BACK_BUTTON = create_button("Retour", (resolution[0] - 191)//2, resolution[1] - 82 - 18)
# taille du boutton sans texte : 191 x 82

#------|function
def ko(window, pokemon_player, pokemon_opponent):
    trainer = pokemon_player.trainer
    opponent = pokemon_opponent.trainer
    clock = pygame.time.Clock()
    elapsed = 0
    pokemon_ko, front_or_back = (pokemon_player, "back") if pokemon_player.hp <= 0 else (pokemon_opponent, "front")
    ko_running = True
    state = 0
    pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
    while ko_running:
        dt = clock.tick(30) / 1000
        elapsed += dt
        
        # État 0 : afficher le message KO
        if state == 0 and elapsed >= 0.5:
            text = f"{pokemon_ko.name} {'ennemi' if pokemon_ko is pokemon_opponent else 'allié'} est KO"
            draw_text(text, font, WHITE, 100, 600)
            state = 1
            elapsed = 0
            
        # État 1 : jouer l'animation après 2s
        elif state == 1 and elapsed >= 2:
            pokemon_ko.animate_death(window, front_or_back)
            state = 2
            elapsed = 0 
            
        # État 2 : envoie du pokemon suivant après 4s apres le state 1
        elif state == 2 and elapsed >= 4:    
            if pokemon_ko is pokemon_player:
                pokemon_player = trainer.send_next("back")
                ui_battle.refresh_pokemon_sprite(window,pokemon_player,"trainer")
                ui_battle.draw_hp_bar(window, pokemon_player, True)
            else:
                pokemon_opponent = opponent.send_next("front")
                ui_battle.refresh_pokemon_sprite(window,pokemon_opponent,"opponent") 
                ui_battle.draw_hp_bar(window, pokemon_opponent, False)
            
            ko_running = False
            
        pygame.display.flip()
        
    pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
    return pokemon_player,pokemon_opponent,not(pokemon_player is None or pokemon_opponent is None)

def turn(window, pokemon_player, pokemon_opponent):
    pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
    turn_running = True
    battle_running = True
    while turn_running:
        dt = clock.tick(30)
                    
        # --- créer boutons des attaques
        moves_available = pokemon_player.get_moveset()
        list_coord = [(18,res_scene[1] + 18),
                      (resolution[0] - 191 - 18, res_scene[1] + 18),
                      (18,resolution[1] - 18  - 82),
                      (resolution[0] - 191 - 18,resolution[1] - 18 - 82)]
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
                        start_turn(window, pokemon_player, pokemon_opponent, moves_available, i)
                    if battle_state == "ko":
                        return ko(window, pokemon_player, pokemon_opponent)

            if BACK_BUTTON.handle_event(event):
                turn_running = False

        pygame.display.flip()
    pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
    return pokemon_player, pokemon_opponent, battle_running

def battle(window):    
    #------|Variable
    battle_running = True
    trainer,opponent = pokemon_trainer.init_trainer()
    # random background()
    bg_path = os.path.join(background_dir_path,"bg-forest.png")
    pokemon_player,pokemon_opponent,window = pokemon_battle.start_battle(window,trainer,opponent,background=bg_path)
    while battle_running :
        dt = clock.tick(30)
                    
        for button in [ATTACK_BUTTON, BAG_BUTTON, POKEMON_BUTTON]:
            button.draw(window)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ATTACK_BUTTON.handle_event(event):
                pokemon_player,pokemon_opponent,battle_running = \
                    turn(window,pokemon_player,pokemon_opponent)
            if BAG_BUTTON.handle_event(event):
                pass
            if POKEMON_BUTTON.handle_event(event):
                pass

        pygame.display.flip()

def options():
    options_running = True
    while options_running :
        dt = clock.tick(30)
        window.fill(BLACK)
        fps_counter()
        
        draw_text("OPTIONS", font, "#b68f40", res_scene[0]//2 + 200, res_scene[1]//2)

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
    run = True
    while run :
        window.fill(BLACK)        
        window.blit(BACKGROUND_INTRO,(0,0))       
        draw_text(project_name, font, "#b68f40", res_scene[0]//2 - 200, res_scene[1]//3 - 100)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.draw(window)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if PLAY_BUTTON.handle_event(event):
                battle(window)
            if OPTIONS_BUTTON.handle_event(event):
                options()
            if QUIT_BUTTON.handle_event(event):
                pygame.quit()
                sys.exit()

        pygame.display.flip()

main_menu(window)