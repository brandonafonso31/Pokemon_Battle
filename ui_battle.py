from button import *
from PIL import ImageColor
from config import img_dir_path,BLACK
import os 
import battle_attack
from config import BLACK,res_scene

def draw_move(window,move,x,y):
    """return a bool which is did the button got draw ?"""
    move_img_path = os.path.join(img_dir_path,f"battle_ui/{move.type.name}_attack_button.png")
    move_img = pygame.image.load(move_img_path).convert_alpha()
    move_button = Button(x, y, move_img, 1,move.name,ImageColor.getrgb(move.type.color()))
    return move_button.draw(window)

def choice_move(window,res_scene,resolution,x_move,y_menu,pokemon_trainer,pokemon_opponent):
    pygame.draw.rect(window, BLACK,(0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
    still_in_battle = True
    
    moves = pokemon_trainer.get_moveset()
    length = len(moves)
    if length > 0 and moves[0] is not None and draw_move(window,moves[0],x_move - 200, y_menu + 50):
        pokemon_trainer, pokemon_opponent, still_in_battle = battle_attack.turn(pokemon_trainer, pokemon_opponent, "move1", window,res_scene,resolution)                            
    if length > 1 and moves[1] is not None and draw_move(window,moves[1],x_move + 200, y_menu + 50):
        pokemon_trainer, pokemon_opponent, still_in_battle = battle_attack.turn(pokemon_trainer, pokemon_opponent, "move2", window,res_scene,resolution)                
    if length > 2 and moves[2] is not None and draw_move(window,moves[2],x_move - 200, y_menu + 150):
        pokemon_trainer, pokemon_opponent, still_in_battle = battle_attack.turn(pokemon_trainer, pokemon_opponent, "move3", window,res_scene,resolution)                
    if length > 3 and moves[3] is not None and draw_move(window,moves[3],x_move + 200, y_menu + 150):
        pokemon_trainer, pokemon_opponent, still_in_battle = battle_attack.turn(pokemon_trainer, pokemon_opponent, "move4", window,res_scene,resolution)
            
    return pokemon_trainer, pokemon_opponent, still_in_battle

def draw_hp_bar(window, pokemon, from_trainer):
    """Draw the HP bar of a pokemon"""  
    hp_bar_length = 200
    hp_bar_height = 20
    if from_trainer:
        x = res_scene[0] - hp_bar_length - 50
        y = res_scene[1] - hp_bar_height - 50
    else:
        x,y = 50,50
            
    hp_ratio = pokemon.hp / (pokemon.hp_max if pokemon.hp_max > 0 else 1.0)
    
    # Draw the background of the HP bar
    pygame.draw.rect(window, (50, 50, 50), (x, y, hp_bar_length, hp_bar_height))
    
    # Draw the current HP
    current_hp_length = int(hp_bar_length * hp_ratio)
    pygame.draw.rect(window, (0, 255, 0), (x, y, current_hp_length, hp_bar_height))
    
    # Draw the text
    font = pygame.font.SysFont("arial", 20)
    text = font.render(f"{pokemon.name} HP: {pokemon.hp}/{pokemon.hp_max}", True, BLACK)
    window.blit(text, (x, y))