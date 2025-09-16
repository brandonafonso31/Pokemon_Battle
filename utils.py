from config import WHITE, BLACK, res_screen_top,res_screen_bottom,img_dir_path,font_path,battle_json_path,pokeball_dir_path,sprites_dir_path,song_dir_path,low_hp_theme_path
import os,pygame,button,pokemon_battle,json,sys,sprite
from random import choice,randint

def draw_text(surface,text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))

def reset_log(surface):
    delay_flat(1)
    with open(battle_json_path, "r") as f:
        battle_data = json.load(f)
    background = pygame.image.load(battle_data["background"]).convert()
    
    rect_height = 50
    rect = pygame.Rect(0,res_screen_top[1]- rect_height,res_screen_top[0],rect_height-5)

    surface.blit(background, rect, rect)
    pygame.display.flip()
    
def print_log_ingame(surface,txt,reset = False):
    with open(battle_json_path, "r") as f:
        battle_data = json.load(f)
    background = pygame.image.load(battle_data["background"]).convert()
    
    rect_height = 50
    rect = pygame.Rect(0,res_screen_top[1]- rect_height,res_screen_top[0],rect_height-5)

    surface.blit(background, rect, rect)
    
    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    overlay.fill((60, 60, 60, 200))  # 180 = opacité (0=transparent, 255=opaque)

    # On blitte l'overlay sur la fenêtre
    surface.blit(overlay, rect.topleft)
    
    font = pygame.font.Font(font_path,30)
    padding = 10
    draw_text(surface, txt, font, WHITE, padding, res_screen_bottom[1] - rect_height//2 - padding)
    pygame.display.flip()
    if reset:
        reset_log(surface)
    
def create_button(text,x,y, scale = 1, path=""):
    if path == "":
        path = os.path.join(img_dir_path,"battle_ui/move_button.png")
    button_img = pygame.image.load(path).convert()
    return button.Button(x, y, button_img, scale, text)

def start_turn(window, pokemon_player, pokemon_opponent, moves, move_id):
    """Joue un tour de combat avec le move choisi et retourne l'état."""
    if moves[move_id].pp <= 0:
        text = f"{pokemon_player.name} n'a plus de PP pour {moves[move_id].name}"
        print_log_ingame(window,text, reset = True)
        text = f"Que dois faire {pokemon_player.name} ?"
        print_log_ingame(window,text)
        return pokemon_player, pokemon_opponent, "choose_attack"  # toujours en combat, mais pas d'action
    else:
        # Lance le tour de combat (animations, dégâts…)
        pokemon_player, pokemon_opponent, still_in_battle = \
            pokemon_battle.turn(pokemon_player, pokemon_opponent, f"move{move_id + 1}", window)

        return pokemon_player, pokemon_opponent, still_in_battle

def update_battle_json(updates: dict):
    if os.path.exists(battle_json_path):
        with open(battle_json_path, "r") as f:
            data = json.load(f)
    else:
        data = {}
    data.update(updates)
    with open(battle_json_path, "w") as f:
        json.dump(data, f, indent=4)
        
def delay_flat(delay):
    elapsed = 0
    clock = pygame.time.Clock()
    while elapsed < delay:
        dt = clock.tick(30) / 1000
        elapsed += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                       
def get_width_pokemon_sprite(front_or_back):
    path = os.path.join(sprites_dir_path,"actual_battle_sprite",f"pokemon_{front_or_back}_1.png")
    if os.path.exists(path):
        sprite = pygame.image.load(path).convert()
        return sprite.get_width()
    return 0

def get_width_pokeball_sprite():
    path = os.path.join(sprites_dir_path,"pokeball","ball_POKEBALL_open.png")
    if os.path.exists(path):
        sprite = pygame.image.load(path).convert()
        return sprite.get_width()
    return 0

def get_prio(pokemon_1,pokemon_2,move_player,move_ia,move_id_player,move_id_ia):
    first, first_move_id, second, second_move_id = None,None,None,None
    if move_player.prio > move_ia.prio:
        first, first_move_id = pokemon_1, move_id_player
        second, second_move_id = pokemon_2, move_id_ia
    elif move_player.prio < move_ia.prio:
        first, first_move_id = pokemon_2, move_id_ia
        second, second_move_id = pokemon_1, move_id_player
    else:
        if pokemon_1.vit > pokemon_2.vit:
            first, first_move_id = pokemon_1, move_id_player
            second, second_move_id = pokemon_2, move_id_ia
        elif pokemon_1.vit < pokemon_2.vit:
            first, first_move_id = pokemon_2, move_id_ia
            second, second_move_id = pokemon_1, move_id_player
        else:
            # Si les vitesses sont égales, déterminer l'ordre aléatoirement
            if choice([True, False]):
                first, first_move_id = pokemon_1, move_id_player
                second, second_move_id = pokemon_2, move_id_ia
            else:
                first, first_move_id = pokemon_2, move_id_ia
                second, second_move_id = pokemon_1, move_id_player
    return first, first_move_id, second, second_move_id

def get_success_rate(pokemon_1, pokemon_2, first_move_id):
    move = getattr(pokemon_1, first_move_id)
    return pokemon_1.accuracy / pokemon_2.escape * move.accuracy
    
def check_hp_to_change_music(pokemon_1,pokemon_2):
    hp_1,hp_max_1 = pokemon_1.hp,pokemon_1.hp_max
    hp_2,hp_max_2 = pokemon_2.hp,pokemon_2.hp_max
    
    if os.path.exists(battle_json_path):
        with open(battle_json_path, "r") as f:
            data = json.load(f)
        music_path = data["music"]
        opponent_theme_path = data["opponent_theme"]
    else:
        return
    boolean_hp = (hp_1 > 0 and hp_1 < 20/100 * hp_max_1) or (hp_2 > 0 and hp_2 < 20/100 * hp_max_2)    
    if boolean_hp and music_path != low_hp_theme_path:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(low_hp_theme_path)
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.3)
        update_battle_json({"music": low_hp_theme_path})
    elif not boolean_hp and music_path != opponent_theme_path:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(opponent_theme_path)
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.3)
        update_battle_json({"music": opponent_theme_path})