from PIL import Image
from config import img_dir_path,battle_json_path
import os, sprite, pygame, json

LEN_NAME_POKEMON = 7
NB_POKEMON_PER_ROW = 8
WHITE = (255, 255, 255, 0)
RES_SPRITE_POKEMON = (96, 96)


def recup_sprite_pokemon(sprite_gen_path, num_pokemon, front_or_back):
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
            
    sprite_pokemon.save(os.path.join(img_dir_path,f"sprites/pokemon_{front_or_back}.png"))
    return sprite_pokemon
    
def get_first_pixel(image_path):
    image = Image.open(image_path)
    return image.getpixel((0,0))

def get_base_pixel(image_path):
    """itère sur tous les pixel en les parcourant en ligne, jusqu'à 
    trouver un pixel (le pixel le plus bas), puis retourne le j"""
    image = Image.open(image_path)
    border = get_first_pixel(image_path)
    
    i,j=0,96
    pixel_cur = image.getpixel((i,j-1))
    while j!=0 and pixel_cur == border:
        pixel_cur = image.getpixel((i,j-1))
        i+=1
        if i==96:
            i=0
            j-=1
    return j

def get_top_pixel(image_path):
    """itère sur tous les pixel en les parcourant en ligne, jusqu'à 
    trouver un pixel (le pixel le plus haut), puis retourne le j"""
    image = Image.open(image_path)
    border = get_first_pixel(image_path)
    
    i,j=0,0
    pixel_cur = image.getpixel((i,j))
    while j!=96 and pixel_cur == border:
        pixel_cur = image.getpixel((i,j))
        i+=1
        if i==96:
            i=0
            j+=1
    return j

def get_sprite(pokemon,front_or_back):
    pokemon_sprite = pokemon.sprites(front_or_back)
    pokemon_path = os.path.join(img_dir_path,f"sprites/pokemon_{front_or_back}.png")
    pokemon_sprite = pygame.image.load(pokemon_path).convert()
    pokemon_sprite.set_colorkey(sprite.get_first_pixel(pokemon_path))
    scale = 2 + (front_or_back == "back")
    pokemon_sprite = pygame.transform.scale(pokemon_sprite, (scale * 100,scale * 100))
    return pokemon_sprite

def get_opponent_sprite(res, pokemon):
    
    opponent_pokemon_sprite = get_sprite(pokemon,"front")
    path_sprite = os.path.join(img_dir_path,"sprites/pokemon_front.png")
    y_opponent = sprite.get_base_pixel(path_sprite)
    y_opponent = res[1]//2 + 2*(96 - y_opponent) - 300
    x_opponent = res[0]//2 + 75
    pokemon_json = {
        "path_sprite": path_sprite,
        "x": x_opponent,
        "y": y_opponent
    }
    update_battle_json({"pokemon_opponent": pokemon_json})
    
    return pokemon,opponent_pokemon_sprite, (x_opponent, y_opponent)

def get_trainer_sprite(res, pokemon):
    trainer_pokemon_sprite = get_sprite(pokemon,"back")
    path_sprite = os.path.join(img_dir_path,"sprites/pokemon_back.png")
    y_trainer = sprite.get_top_pixel(path_sprite)
    y_trainer = res[1] - 3*(96 - y_trainer) - 350
    x_trainer = res[0]//2 - 75*2 - 96*2
    pokemon_json = {
        "path_sprite": path_sprite,
        "x": x_trainer,
        "y": y_trainer
    }
    update_battle_json({"pokemon_trainer": pokemon_json})
    return pokemon,trainer_pokemon_sprite, (x_trainer, y_trainer)

def update_battle_json(updates: dict):

    if os.path.exists(battle_json_path):
        with open(battle_json_path, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data.update(updates)

    with open(battle_json_path, "w") as f:
        json.dump(data, f, indent=4)

def get_image(image_path):
    image = pygame.image.load(image_path).convert()
    image.set_colorkey(sprite.get_first_pixel(image_path))
    return image,image.get_size()