from config import WHITE, res_screen_top,res_screen_bottom,img_dir_path,font_path,battle_json_path
import os,pygame,button,pokemon_battle,json
def draw_text(surface,text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))

def print_log_ingame(surface,txt):
    font = pygame.font.Font(font_path)
    draw_text(surface, txt, font, WHITE, res_screen_top[0], res_screen_bottom[1] - 50)
    
def create_button(text,x,y, scale = 1, path=""):
    if path == "":
        path = os.path.join(img_dir_path,"battle_ui/move_button.png")
    button_img = pygame.image.load(path).convert_alpha()
    return button.Button(x, y, button_img, scale, text)

def start_turn(window, pokemon_player, pokemon_opponent, moves, move_id):
    """Joue un tour de combat avec le move choisi et retourne l'état."""
    if moves[move_id].pp <= 0:
        text = f"{pokemon_player.name} n'a plus de PP pour {moves[move_id].name}"
        print_log_ingame(text)
        return pokemon_player, pokemon_opponent, True  # toujours en combat, mais pas d'action
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