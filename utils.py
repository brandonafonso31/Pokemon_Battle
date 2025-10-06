from config import WHITE, BLACK, res_screen_top, res_screen_bottom, img_dir_path, font_path, battle_json_path, pokeball_dir_path, sprites_dir_path, song_dir_path, low_hp_theme_path
import os, pygame, button, pokemon_battle, json, sys, sprite
from random import choice, randint


def draw_text(manager, text, font, text_col, x, y):
    surface = manager.get_surface()
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))


def reset_log(manager):
    delay_flat(1,manager)
    if not os.path.exists(battle_json_path):
        return
    with open(battle_json_path, "r") as f:
        battle_data = json.load(f)
    background = pygame.image.load(battle_data["background"]).convert()

    rect_height = 50
    rect = pygame.Rect(0, res_screen_top[1] - rect_height, res_screen_top[0], rect_height - 5)

    surface = manager.get_surface()
    surface.blit(background, rect, rect)
    manager.update()


def print_log_ingame(manager, txt, reset=False):
    if not os.path.exists(battle_json_path):
        return
    with open(battle_json_path, "r") as f:
        battle_data = json.load(f)
    background = pygame.image.load(battle_data["background"]).convert()

    rect_height = 50
    rect = pygame.Rect(0, res_screen_top[1] - rect_height, res_screen_top[0], rect_height - 5)

    surface = manager.get_surface()
    surface.blit(background, rect, rect)

    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    overlay.fill((60, 60, 60, 200))
    surface.blit(overlay, rect.topleft)

    font = pygame.font.Font(font_path, 30)
    padding = 10
    draw_text(manager, txt, font, WHITE, padding, res_screen_bottom[1] - rect_height // 2 - padding)

    manager.update()

    if reset:
        reset_log(manager)


def create_button(text, x, y, scale=1, path=""):
    if path == "":
        path = os.path.join(img_dir_path, "battle_ui/move_button.png")
    button_img = pygame.image.load(path).convert()
    return button.Button(x, y, button_img, scale, text)


def start_turn(manager, pokemon_player, pokemon_opponent, moves, move_id):
    """Joue un tour de combat avec le move choisi et retourne l'état."""
    if moves[move_id].pp <= 0:
        text = f"{pokemon_player.name} n'a plus de PP pour {moves[move_id].name}"
        print_log_ingame(manager, text, reset=True)
        text = f"Que dois faire {pokemon_player.name} ?"
        print_log_ingame(manager, text)
        return pokemon_player, pokemon_opponent, "choose_attack"
    else:
        pokemon_player, pokemon_opponent, still_in_battle = \
            pokemon_battle.turn(pokemon_player, pokemon_opponent, f"move{move_id + 1}", manager)
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


def delay_flat(delay,manager):
    elapsed = 0
    clock = pygame.time.Clock()
    while elapsed < delay:
        dt = clock.tick(30) / 1000
        elapsed += dt

        for event in pygame.event.get():
            pygame_event_handle(manager,event)


def get_width_pokemon_sprite(front_or_back):
    path = os.path.join(sprites_dir_path, "actual_battle_sprite", f"pokemon_{front_or_back}_1.png")
    if os.path.exists(path):
        sprite_img = pygame.image.load(path).convert()
        return sprite_img.get_width()
    return 0


def get_width_pokeball_sprite():
    path = os.path.join(sprites_dir_path, "pokeball", "ball_POKEBALL_open.png")
    if os.path.exists(path):
        sprite_img = pygame.image.load(path).convert()
        return sprite_img.get_width()
    return 0


def get_prio(pokemon_1, pokemon_2, move_player, move_ia, move_id_player, move_id_ia):
    if move_player.prio > move_ia.prio:
        return pokemon_1, move_id_player, pokemon_2, move_id_ia
    elif move_player.prio < move_ia.prio:
        return pokemon_2, move_id_ia, pokemon_1, move_id_player
    else:
        if pokemon_1.vit > pokemon_2.vit:
            return pokemon_1, move_id_player, pokemon_2, move_id_ia
        elif pokemon_1.vit < pokemon_2.vit:
            return pokemon_2, move_id_ia, pokemon_1, move_id_player
        else:
            if choice([True, False]):
                return pokemon_1, move_id_player, pokemon_2, move_id_ia
            else:
                return pokemon_2, move_id_ia, pokemon_1, move_id_player


def get_success_rate(pokemon_1, pokemon_2, first_move_id):
    move = getattr(pokemon_1, first_move_id)
    return pokemon_1.accuracy / pokemon_2.escape * move.accuracy


def check_hp_to_change_music(pokemon):
    hp, hp_max = pokemon.hp, pokemon.hp_max

    if not os.path.exists(battle_json_path):
        return

    with open(battle_json_path, "r") as f:
        data = json.load(f)
    music_path = data.get("music")
    opponent_theme_path = data.get("opponent_theme")

    boolean_hp = hp > 0 and hp < 20 / 100 * hp_max
    if boolean_hp and music_path != low_hp_theme_path:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(low_hp_theme_path)
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.3)
        update_battle_json({"music": low_hp_theme_path})
    elif not boolean_hp and opponent_theme_path and music_path != opponent_theme_path:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(opponent_theme_path)
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.3)
        update_battle_json({"music": opponent_theme_path})            
        
        
def pygame_event_handle(manager,event):
    if event.type == pygame.QUIT:
        pygame.quit(); sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_F11 or (event.key == pygame.K_ESCAPE and manager.is_fullscreen):
            manager.toggle_fullscreen()
            
def print_msg_eff(manager,eff):
    msg =""
    if eff == 4:
        msg+="C'est hyper efficace !"
    elif eff == 2:
        msg+="C'est super efficace !"
    elif eff ==1:
        msg+="C'est efficace"
    elif eff == 0.5:
        msg+="Ce n'est pas très efficace"
    elif eff == 0.25:
        msg+="Ce n'est vraiment pas efficace"
    elif eff == 0:
        msg+="Cela ne fait aucun dégat"
    print(msg)
    print_log_ingame(manager,msg,reset=True)