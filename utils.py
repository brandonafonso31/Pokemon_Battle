from config import WHITE, BLACK, res_screen_top,res_screen_bottom,img_dir_path,font_path,battle_json_path,pokeball_dir_path,sprites_dir_path
import os,pygame,button,pokemon_battle,json,sys,sprite

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
                
# A changer par une fonction générique display_animation(window,animation_file_path)
def send_pokeball(window, pos, pokeball_name = "pokeball"):
    x,y = pos
    path = os.path.join(pokeball_dir_path,f"ball_{pokeball_name.upper()}.png")
    pokeball_sprite = pygame.image.load(path).convert()
    pokeball_sprite.set_colorkey(sprite.get_first_pixel(path))
    
    path_open = os.path.join(pokeball_dir_path,f"ball_{pokeball_name.upper()}_open.png")
    pokeball_sprite_open = pygame.image.load(path_open).convert()
    pokeball_sprite_open.set_colorkey(sprite.get_first_pixel(path_open))
    
    with open(battle_json_path, "r") as f:
        data = json.load(f)        
    bg = pygame.image.load(data["background"]).convert()
    
    width = pokeball_sprite.get_width()
    height = pokeball_sprite.get_height()
    
    clock = pygame.time.Clock()
    nb_frames = 8
    width_per_frame = width // nb_frames
    elapsed = 0
    x_frame = 0
    rect_bg = pygame.Rect(x, y, width_per_frame, height)
    loop = 0
    
    while loop <= 3:
        dt = clock.tick(30) / 1000
        elapsed += dt
        
        if elapsed >= 0.05:
            rect = pygame.Rect(x_frame, 0, width_per_frame, height)
            window.blit(bg,pos,rect_bg)
            window.blit(pokeball_sprite, pos, rect) 
            x_frame += width_per_frame
            elapsed = 0
            
            if x_frame >= width :
                loop += 1
                x_frame = 0             
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.display.flip() 
    
    window.blit(bg,pos,rect_bg)
    window.blit(pokeball_sprite_open, pos)
    pygame.display.flip()
    delay_flat(0.5)
    # flash écran ou qqch
    window.blit(bg,pos,rect_bg)
    delay_flat(0.2)
       
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