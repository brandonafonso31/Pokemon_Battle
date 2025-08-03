from pokemon_move import *
from pokemon_init import dracaufeu,leviator
from pokemon import Pokemon
from config import img_dir_path,song_dir_path,battle_dir_path,battle_json_path
import ui_battle

import os
import sprite
import pygame

def get_sprite(pokemon: Pokemon,front_or_back: str):
    pokemon_sprite = pokemon.sprites(front_or_back)
    pokemon_path = os.path.join(img_dir_path,f"sprites/pokemon_{front_or_back}.png")
    pokemon_sprite = pygame.image.load(pokemon_path).convert()
    pokemon_sprite.set_colorkey(sprite.get_first_pixel(pokemon_path))
    scale = 2 + (front_or_back == "back")
    pokemon_sprite = pygame.transform.scale(pokemon_sprite, (scale * 100,scale * 100))
    return pokemon_sprite


def get_opponent_sprite(res, pokemon = dracaufeu):
    
    opponent_pokemon_sprite = get_sprite(pokemon,"front")
    path_sprite = os.path.join(img_dir_path,"sprites/pokemon_front.png")
    y_opponent = sprite.get_base_pixel(path_sprite)
    y_opponent = res[1]//2 + 2*(96 - y_opponent) - 300
    x_opponent = res[0]//2 + 75
    pokemon_json = {
        "pokemon": pokemon,
        "path_sprite": path_sprite,
        "x": x_opponent,
        "y": y_opponent
    }
    update_battle_json({"pokemon_opponent": pokemon_json})
    
    return pokemon,opponent_pokemon_sprite, (x_opponent, y_opponent)

def get_trainer_sprite(res, pokemon = leviator):
    trainer_pokemon_sprite = get_sprite(pokemon,"back")
    path_sprite = os.path.join(img_dir_path,"sprites/pokemon_back.png")
    y_trainer = sprite.get_top_pixel(path_sprite)
    y_trainer = res[1] - 3*(96 - y_trainer) - 350
    x_trainer = res[0]//2 - 75*2 - 96*2
    pokemon_json = {
        "pokemon": pokemon,
        "path_sprite": path_sprite,
        "x": x_trainer,
        "y": y_trainer
    }
    update_battle_json({"pokemon_trainer": pokemon_json})
    return pokemon,trainer_pokemon_sprite, (x_trainer, y_trainer)

def update_battle_json(updates: dict):
    path = battle_json_path

    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data.update(updates)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def get_image(image_path):
    image = pygame.image.load(image_path).convert()
    image.set_colorkey(sprite.get_first_pixel(image_path))
    return image,image.get_size()

def start_battle(window,res):
    """Instancie les premiers éléments de la scène."""
    #-----------------------------| MUSIC |------------------------------#
    music_path = os.path.join(song_dir_path,"elite_four/Battle_Elite_Four_BW.mp3")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.3)
    #---------------------------| BACKGROUND |---------------------------#
    background_path = os.path.join(img_dir_path,"background/forest.jpg")
    background = pygame.image.load(background_path).convert()
    window.blit(background,(0,0))
    pygame.display.flip()
    #-------------------------| SPRITE ENNEMI |--------------------------#
    pygame.time.delay(500)
    pokemon_opponent,opponent_pokemon_sprite,coord_opp = get_opponent_sprite(res)
    window.blit(opponent_pokemon_sprite,coord_opp)
    pokemon_opponent.add_rect(coord_opp)
    #--------------------------| SPRITE ALLIE |--------------------------#    
    pygame.display.flip()
    pygame.time.delay(500)
    pokemon_trainer,trainer_pokemon_sprite,coord_trainer = get_trainer_sprite(res)
    window.blit(trainer_pokemon_sprite,coord_trainer)
    pokemon_trainer.add_rect(coord_trainer)
    
    ui_battle.draw_hp_bar(window, pokemon_trainer, from_trainer=True)
    ui_battle.draw_hp_bar(window, pokemon_opponent, from_trainer=False)
    
    update_battle_json({
        "music": music_path,
        "background": background_path
    })
    
    ui_battle.refresh_screen(window)
    return pokemon_trainer,pokemon_opponent,window

"""def refresh_screen(window,resolution):
    background = pygame.image.load(os.path.join(img_dir_path,"background/forest.jpg")).convert()
    window.blit(background,(0,0))
    pygame.display.flip()
    pygame.time.delay(500)
    window.blit(opponent_pokemon_sprite,coord_opp)
    window.blit(trainer_pokemon_sprite,coord_trainer)
    pygame.display.flip()
    return window"""