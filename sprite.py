from PIL import Image
from config import img_dir_path,battle_json_path,sprites_dir_path,WHITE
import os, sprite, pygame, json

LEN_NAME_POKEMON = 7
NB_POKEMON_PER_ROW = 8
RES_SPRITE_POKEMON = (96, 96)


def recup_sprite_pokemon(sprite_gen_path, num_pokemon, front_or_back,id):
    global LEN_NAME_POKEMON,WHITE,NB_POKEMON_PER_ROW,RES_SPRITE_POKEMON
    image = Image.open(f"{sprite_gen_path}_{front_or_back}.png")
    res_image = image.size
    
    nb_row = res_image[0]//RES_SPRITE_POKEMON[0]
    nb_col = res_image[1]//RES_SPRITE_POKEMON[1]
    
    indice_row  = RES_SPRITE_POKEMON[0] * ((num_pokemon-1) % NB_POKEMON_PER_ROW)
    indice_col = (RES_SPRITE_POKEMON[1] + LEN_NAME_POKEMON) * (num_pokemon//NB_POKEMON_PER_ROW)
    #print(f"Premier pixel : {indice_row,indice_col}")
    
    sprite_pokemon = Image.new('RGBA', RES_SPRITE_POKEMON, WHITE)
    for i in range(indice_row,indice_row + RES_SPRITE_POKEMON[0]):
        for j in range(indice_col,indice_col + RES_SPRITE_POKEMON[1]):
            pixel = image.getpixel((i,j))
            sprite_pokemon.putpixel((i-indice_row,j-indice_col), pixel)
            
    sprite_pokemon.save(os.path.join(sprites_dir_path,f"pokemon_{front_or_back}_{id}.png"))
    return sprite_pokemon
    
def get_first_pixel(image_path):
    image = Image.open(image_path)
    return image.getpixel((0,0))

def get_base_pixel(image_path):
    """itère sur tous les pixel en les parcourant en ligne, jusqu'à 
    trouver un pixel (le pixel le plus bas), puis retourne le j"""
    image = Image.open(image_path)
    image_height = image.size[1]
    border = get_first_pixel(image_path)
    
    i,j=0,image_height
    pixel_cur = image.getpixel((i,j-1))
    while j!=0 and pixel_cur == border:
        pixel_cur = image.getpixel((i,j-1))
        i+=1
        if i==image_height:
            i=0
            j-=1
    return j

def get_top_pixel(image_path):
    """itère sur tous les pixel en les parcourant en ligne, jusqu'à 
    trouver un pixel (le pixel le plus haut), puis retourne le j"""
    image = Image.open(image_path)
    image_height = image.size[1]
    border = get_first_pixel(image_path)
    
    i,j=0,0
    pixel_cur = image.getpixel((i,j))
    while j!=image_height and pixel_cur == border:
        pixel_cur = image.getpixel((i,j))
        i+=1
        if i==image_height:
            i=0
            j+=1
    return j

def get_sprite(pokemon,id,front_or_back):
    path = f"pokemon_{front_or_back}_{id}.png"
    pokemon_sprite = pokemon.sprites(front_or_back,path)
    pokemon_path = os.path.join(sprites_dir_path,path)
    pokemon_sprite = pygame.image.load(pokemon_path).convert()
    pokemon_sprite.set_colorkey(sprite.get_first_pixel(pokemon_path))
    scale = 2 + (front_or_back == "back")
    
    base_w, base_h = pokemon_sprite.get_size()
    pokemon_sprite = pygame.transform.scale(pokemon_sprite, (base_w * scale, base_h * scale))
    pygame.image.save(pokemon_sprite, pokemon_path)
    return pokemon_sprite


def create_pokemon_opponent(res, pokemon, id, save_to_filename: str):
    opponent_pokemon_sprite = get_sprite(pokemon, id, "front")
    path_sprite = os.path.join(sprites_dir_path, save_to_filename)
    
    base_offset = sprite.get_base_pixel(path_sprite) - opponent_pokemon_sprite.get_height() 
    x_opponent = (res[0] + opponent_pokemon_sprite.get_width())//2 - 40
    y_opponent = res[1]//2 - base_offset  - 200

    pokemon_json = {
        "path_sprite": path_sprite,
        "x": x_opponent,
        "y": y_opponent
    }
    pokemon.add_rect((x_opponent, y_opponent), opponent_pokemon_sprite)
    return pokemon_json


def create_pokemon_trainer(res, pokemon, id, save_to_filename: str):
    trainer_pokemon_sprite = get_sprite(pokemon, id, "back")
    path_sprite = os.path.join(sprites_dir_path, save_to_filename)

    base_offset = sprite.get_base_pixel(path_sprite) - trainer_pokemon_sprite.get_height()
    x_trainer = (res[0]//2 - trainer_pokemon_sprite.get_width())//2 + 40
    y_trainer = res[1] - base_offset - 375

    pokemon_json = {
        "path_sprite": path_sprite,
        "x": x_trainer,
        "y": y_trainer
    }
    pokemon.add_rect((x_trainer, y_trainer), trainer_pokemon_sprite)
    return pokemon_json

def get_image(image_path,scale=1):
    image = pygame.image.load(image_path).convert()
    w,h = image.get_size()
    image.set_colorkey(sprite.get_first_pixel(image_path))
    image = pygame.transform.scale(image, (scale * w, scale * h))
    return image