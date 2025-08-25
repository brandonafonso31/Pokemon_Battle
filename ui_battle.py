from button import *
from PIL import ImageColor
from config import img_dir_path,BLACK,battle_json_path,WHITE,res_scene,resolution
import os,pokemon_battle,json,sprite,button_test

def draw_move(window,move,x,y):
    """return a bool which is did the button got draw ?"""
    move_img_path = os.path.join(img_dir_path,f"battle_ui/{move.type.name}_attack_button.png")
    move_img = pygame.image.load(move_img_path).convert_alpha()
    move_button = button_test.Button_test(x, y, move_img, 1,move.name,ImageColor.getrgb(move.type.color()))
    move_button.draw(window)
    return move_button
                                
def get_color(ratio):
    if ratio > 0.5:
        return (0, 255, 0)       # Vert
    elif ratio > 0.2:
        return (255, 165, 0)     # Orange
    else:
        return (255, 0, 0)       # Rouge
        
def draw_hp_bar(window, pokemon, from_trainer, old_hp=None):
    hp_bar_length = 250
    hp_bar_height = 20
    padding = 10  # Espacement autour des éléments

    if from_trainer:
        x = res_scene[0] - (hp_bar_length + 2*padding + 50)
        y = res_scene[1] - hp_bar_height - 70
    else:
        x, y = 50, 70

    hp_max = pokemon.hp_max if pokemon.hp_max > 0 else 1
    current_hp = pokemon.hp
    previous_hp = old_hp if old_hp is not None else current_hp

    current_length = int(hp_bar_length * (previous_hp / hp_max))
    target_length = int(hp_bar_length * (current_hp / hp_max))
    font = pygame.font.SysFont("arialblack", 20)
    
    # Rectangle de fond qui englobe tout (texte + barre)
    background_rect = pygame.Rect(
        x - padding, 
        y - 40 - padding,  # Le texte est 40px au-dessus de la barre
        hp_bar_length + 2*padding,
        40 + hp_bar_height + 2*padding  # Texte + barre + padding
    )

    if current_length > target_length :
        hp_step = max(1, (previous_hp - current_hp) // 20)
        anim_hp = previous_hp
        clock = pygame.time.Clock()
        while anim_hp > current_hp or current_length > target_length:
            dt = clock.tick(30) / 1000 # accumulate le temps passé (en secondes)
            elapsed += dt
            
            if elapsed >= 0.05:
                if anim_hp > current_hp:
                    anim_hp = max(current_hp, anim_hp - hp_step)
            
                current_length = int(hp_bar_length * (anim_hp / hp_max))
                if current_length < target_length:
                    current_length = target_length
                
                color = get_color(current_length / hp_bar_length)

                # Dessiner le fond blanc (ou autre couleur)
                pygame.draw.rect(window, WHITE, background_rect)
                pygame.draw.rect(window, BLACK, background_rect, 2)  # Bordure noire

                # Barre de vie
                pygame.draw.rect(window, (50, 50, 50), (x, y, hp_bar_length, hp_bar_height))
                bar_rect = (x, y, current_length, hp_bar_height)
                pygame.draw.rect(window, color, bar_rect)
            
                # Texte
                text = font.render(f"{pokemon.name} HP: {anim_hp}/{hp_max}", True, BLACK)
                window.blit(text, (x, y - 40))
                
                pygame.display.update(background_rect)
                elapsed = 0
    else:
        # Affichage direct sans animation
        bar_length = int(hp_bar_length * (current_hp / hp_max))
        
        # Fond
        pygame.draw.rect(window, WHITE, background_rect)
        pygame.draw.rect(window, BLACK, background_rect, 2)  # Bordure noire
        
        # Barre de vie
        pygame.draw.rect(window, (50, 50, 50), (x, y, hp_bar_length, hp_bar_height))
        bar_rect = (x, y, bar_length, hp_bar_height)
        color = get_color(current_hp / hp_max)
        pygame.draw.rect(window, color, bar_rect)

        # Texte
        text = font.render(f"{pokemon.name} HP: {current_hp}/{hp_max}", True, BLACK)
        window.blit(text, (x, y - 40))


def refresh_pokemon_sprite(window,pokemon,data,trainer_or_opponent):
    if not pokemon.is_ko:
        current_pokemon_id = data["current"]
        path = data[trainer_or_opponent][str(current_pokemon_id[trainer_or_opponent == "opponent"])]
        pokemon_sprite = pygame.image.load(path["path_sprite"]).convert()
        pokemon_sprite.set_colorkey(sprite.get_first_pixel(path["path_sprite"]))
        window.blit(pokemon_sprite, (path["x"], path["y"]))

def refresh_screen(window, pokemon_trainer, pokemon_opponent, old_hp_trainer=None, old_hp_opponent=None):
    """Refresh the screen with the background and all sprites."""
    with open(battle_json_path, "r") as f:
        data = json.load(f)

    # Background
    background = pygame.image.load(data["background"]).convert()
    window.blit(background, (0, 0))

    refresh_pokemon_sprite(window, pokemon_trainer, data, "trainer")
    refresh_pokemon_sprite(window, pokemon_opponent, data, "opponent")

    # HP Bars
    draw_hp_bar(window, pokemon_trainer, True, old_hp_trainer)
    draw_hp_bar(window, pokemon_opponent, False, old_hp_opponent)

    pygame.display.flip()
