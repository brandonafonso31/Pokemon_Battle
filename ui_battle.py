from button import *
from PIL import ImageColor
from config import img_dir_path,BLACK,battle_json_path,res_scene
import os,battle_attack,json,sprite

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
        if moves[0].pp <= 0:
            print(f"{pokemon_trainer.name} n'a plus de PP pour {moves[0].name}")
        else: pokemon_trainer, pokemon_opponent, still_in_battle = battle_attack.turn(pokemon_trainer, pokemon_opponent, "move1", window,res_scene,resolution)                            
    if length > 1 and moves[1] is not None and draw_move(window,moves[1],x_move + 200, y_menu + 50):
        if moves[1].pp <= 0:
            print(f"{pokemon_trainer.name} n'a plus de PP pour {moves[1].name}")
        else: pokemon_trainer, pokemon_opponent, still_in_battle = battle_attack.turn(pokemon_trainer, pokemon_opponent, "move2", window,res_scene,resolution)                
    if length > 2 and moves[2] is not None and draw_move(window,moves[2],x_move - 200, y_menu + 150):
        if moves[2].pp <= 0:
            print(f"{pokemon_trainer.name} n'a plus de PP pour {moves[2].name}")
        else: pokemon_trainer, pokemon_opponent, still_in_battle = battle_attack.turn(pokemon_trainer, pokemon_opponent, "move3", window,res_scene,resolution)                
    if length > 3 and moves[3] is not None and draw_move(window,moves[3],x_move + 200, y_menu + 150):
        if moves[3].pp <= 0:
            print(f"{pokemon_trainer.name} n'a plus de PP pour {moves[3].name}")
        else: pokemon_trainer, pokemon_opponent, still_in_battle = battle_attack.turn(pokemon_trainer, pokemon_opponent, "move4", window,res_scene,resolution)
            
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
        
def refresh_screen(window, pokemon_trainer, pokemon_opponent):
    """Refresh the screen with the background."""
    with open(battle_json_path, "r") as f:
            data = json.load(f)
    
    # Background
    background = pygame.image.load(data["background"]).convert()
    window.blit(background, (0, 0))
    
    # Pokemon Trainer
    pokemon_trainer_path = data["pokemon_trainer"]
    pokemon_trainer_sprite = pygame.image.load(pokemon_trainer_path["path_sprite"]).convert()
    pokemon_trainer_sprite.set_colorkey(sprite.get_first_pixel(pokemon_trainer_path["path_sprite"]))
    scale = 3
    pokemon_trainer_sprite = pygame.transform.scale(pokemon_trainer_sprite, (scale * 100,scale * 100))
    window.blit(pokemon_trainer_sprite, (pokemon_trainer_path["x"], pokemon_trainer_path["y"]))
    
    # Pokemon Opponent
    pokemon_opponent_path = data["pokemon_opponent"]
    pokemon_opponent_sprite = pygame.image.load(pokemon_opponent_path["path_sprite"]).convert()
    pokemon_opponent_sprite.set_colorkey(sprite.get_first_pixel(pokemon_opponent_path["path_sprite"]))
    scale = 2
    pokemon_opponent_sprite = pygame.transform.scale(pokemon_opponent_sprite, (scale * 100,scale * 100))
    window.blit(pokemon_opponent_sprite, (pokemon_opponent_path["x"], pokemon_opponent_path["y"]))
    #pygame.display.flip()
    
    # HP Bar
    draw_hp_bar(window, pokemon_trainer, True)
    draw_hp_bar(window, pokemon_opponent, False)
    pygame.display.flip()