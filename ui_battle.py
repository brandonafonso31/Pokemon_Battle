from button import *
from PIL import ImageColor
from config import img_dir_path,BLACK
import os 
import battle_attack


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
        pokemon_trainer, pokemon_opponent, still_in_battle = battle_attack.perform_choice_attack(pokemon_trainer, pokemon_opponent, "move1",window,res_scene,resolution)                            
    if length > 1 and moves[1] is not None and draw_move(window,moves[1],x_move + 200, y_menu + 50):
        pokemon_trainer, pokemon_opponent, still_in_battle = battle_attack.perform_choice_attack(pokemon_trainer, pokemon_opponent, "move2",window,res_scene,resolution)                
    if length > 2 and moves[2] is not None and draw_move(window,moves[2],x_move - 200, y_menu + 150):
        pokemon_trainer, pokemon_opponent, still_in_battle = battle_attack.perform_choice_attack(pokemon_trainer, pokemon_opponent, "move3", window,res_scene,resolution)                
    if length > 3 and moves[3] is not None and draw_move(window,moves[3],x_move + 200, y_menu + 150):
        pokemon_trainer, pokemon_opponent, still_in_battle = battle_attack.perform_choice_attack(pokemon_trainer, pokemon_opponent, "move4", window,res_scene,resolution)
            
    return pokemon_trainer, pokemon_opponent, still_in_battle