from PIL import Image
import os

LEN_NAME_POKEMON = 7
NB_POKEMON_PER_ROW = 8
WHITE = (255, 255, 255, 0)
RES_SPRITE_POKEMON = (96, 96)


def recup_sprite_pokemon(sprite_gen_path, num_pokemon, front_or_back):
    global LEN_NAME_POKEMON,WHITE,NB_POKEMON_PER_ROW,RES_SPRITE_POKEMON
    image = Image.open(sprite_gen_path+"_"+front_or_back+".png")
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
            
    sprite_pokemon.save("sprites/pokemon_"+front_or_back+".png")
    return sprite_pokemon
    
def get_first_pixel(image_path):
    image = Image.open(image_path)
    return image.getpixel((0,0))

def get_base_pixel(image_path):
    """itère sur tous les pixel en les parcourant en ligne, jusqu'à 
    trouver un pixel (le pixel le plus bas), puis le retourne le j"""
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
    trouver un pixel (le pixel le plus bas), puis le retourne le j"""
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