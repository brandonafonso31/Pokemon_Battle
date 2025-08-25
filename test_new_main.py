import os,sys,pygame,pokemon_battle,ui_battle,json,sprite
from config import project_name,img_dir_path,sys_dir_path,BLACK,song_dir_path,background_dir_path,battle_json_path
from pygame.locals import *
from button_test import Button_test
import pokemon_trainer

#------|Init pygame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
dt = 0

#------|Resolution
res_scene = (700,500)
resolution = (res_scene[0],res_scene[1]+200)
window = pygame.display.set_mode(resolution,vsync=1)
pygame.display.set_caption(project_name)
pygame.display.set_icon(pygame.image.load(os.path.join(img_dir_path,"sys/logo.png")))

#------|Fonts
font = pygame.font.SysFont("arialblack",40)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

def create_button(text,x,y,path):
    button_img = pygame.image.load(path).convert_alpha()
    return Button_test(x, y, button_img, 1, text)

def fps_counter():
    fps = str(int(clock.get_fps()))
    fps_t = font.render(f"{fps} fps" , 1, pygame.Color("RED"))
    window.blit(fps_t,(0,0))

def start_turn(pokemon_player,pokemon_opponent,moves,move_id):
    if moves[move_id].pp <= 0:
        print(f"{pokemon_player.name} n'a plus de PP pour {moves[0].name}")
        return pokemon_player,pokemon_opponent,True
    else:
        pokemon_player,pokemon_opponent,still_in_battle = \
            pokemon_battle.turn(pokemon_trainer, pokemon_opponent, f"move{move_id + 1}", window,res_scene,resolution) 
        if still_in_battle == "ko":
            still_in_battle = False
        return pokemon_player,pokemon_opponent,still_in_battle
            
            
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
BACK_BUTTON = create_button("Retour", 200,400)
QUIT_BUTTON = create_button("Quitter", 200,400)

ATTACK_BUTTON = create_button("Attaquer", (resolution[0] - 191)//2, res_scene[1] + 18)
POKEMON_BUTTON = create_button("Pokémon", resolution[0] - 191 - 18, resolution[1] - 82 - 18)
BAG_BUTTON = create_button("Sac", 18, resolution[1] - 82 - 18)
# taille du boutton sans texte : 191 x 82

#------|function
def battle(window,pokemon_player,pokemon_opponent):
    battle_running = True
    still_in_battle = True
    while battle_running :
        dt = clock.tick(30)
        window.fill(BLACK)
        fps_counter()
        
        draw_text("OPTIONS", font, "#b68f40", res_scene[0]//2 + 200, res_scene[1]//2)
        
        moves_available = pokemon_player.get_moveset()
        list_coord = [(18,res_scene[1] + 18),(resolution[0] - 191 - 18, res_scene[1] + 18), \
            (18,resolution[1] - 18),(resolution[0] - 191 - 18,resolution[1] - 18)]
        
        moves_button = [ui_battle.draw_move(window,move,coord[0], coord[1],create_button) for move,coord in zip(moves_available,list_coord) ]
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if len(moves_button) > 0 and moves_button[0].handle_event(event):
                pokemon_player,pokemon_opponent,still_in_battle = \
                    start_turn(pokemon_player,pokemon_opponent,moves_available,0)
            if len(moves_button) > 1 and moves_button[1].handle_event(event):
                pokemon_player,pokemon_opponent,still_in_battle = \
                    start_turn(pokemon_player,pokemon_opponent,moves_available,1)
            if len(moves_button) > 2 and moves_button[2].handle_event(event):
                pokemon_player,pokemon_opponent,still_in_battle = \
                    start_turn(pokemon_player,pokemon_opponent,moves_available,2)
            if len(moves_button) > 3 and moves_button[3].handle_event(event):
                pokemon_player,pokemon_opponent,still_in_battle = \
                    start_turn(pokemon_player,pokemon_opponent,moves_available,3)          
                
            
            if BACK_BUTTON.handle_event(event):
                options_running = False

        pygame.display.flip()

def play(window):    
    #------|Variable
    battle_start = False
    play_running = True
    while play_running :
        dt = clock.tick(30)
        fps_counter()
        bg_path = os.path.join(background_dir_path,"bg-forest.png")
        if not battle_start:
            pokemon_player,pokemon_opponent,window = pokemon_battle.start_battle(window,trainer,opponent,background=bg_path)
            battle_start = True
        ui_battle.refresh_screen(window,pokemon_player,pokemon_opponent)
        
        for button in [ATTACK_BUTTON, BAG_BUTTON, POKEMON_BUTTON]:
            button.draw(window)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ATTACK_BUTTON.handle_event(event):
                pokemon_player,pokemon_opponent,still_in_battle = \
                    battle(window,pokemon_player,pokemon_opponent)
            if BAG_BUTTON.handle_event(event):
                play_running = False
            if POKEMON_BUTTON.handle_event(event):
                play_running = False

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
        dt = clock.tick(30)
        window.fill(BLACK)        
        window.blit(BACKGROUND_INTRO,(0,0))
        fps_counter()
        
        draw_text(project_name, font, "#b68f40", res_scene[0]//2 - 200, res_scene[1]//3 - 100)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.draw(window)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if PLAY_BUTTON.handle_event(event):
                play(window)
            if OPTIONS_BUTTON.handle_event(event):
                options()
            if QUIT_BUTTON.handle_event(event):
                pygame.quit()
                sys.exit()

        pygame.display.flip()

main_menu(window)