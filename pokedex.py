from pokemon import Pokemon
from pokemon_type import Type
from pokemon_move import *
from pokemon_nature import Nature
from pokemon_talent import talents
from config import pokemon_data_json_path,data_dir_path
import json,os


def get_pokedex(num_gen: int = -1):
    if num_gen != -1: path = f"data/pokedex_gen{num_gen}.json"
    else: pokemon_data_json_path
    with open(pokemon_data_json_path,"r",encoding="utf-8") as f:
        return json.load(f)

def get_pokemon(id,num_gen: int = -1):
    pokedex = get_pokedex(num_gen)
    for name, infos in pokedex.items():
        if infos["num"] == id :  return infos
    return None

def get_gen(id: str):
    id = int(id)
    if id <= 151: return 1
    elif id <= 251: return 2
    elif id <= 386: return 3
    elif id <= 493: return 4
    elif id <= 649: return 5
    elif id <= 721: return 6
    elif id <= 809: return 7
    elif id <= 905: return 8
    elif id <= 1010: return 9
    return None

def create_pokemon(id,nature=Nature.BIZARRE,EV={"hp":0,"atk":0,"def_":0,"atk_spe":0,"def_spe":0,"vit":0},nickname="",num_on_sprite_sheet=1):
    infos = get_pokemon(id)
    if infos is None:
        return None
    
    pokemon = Pokemon(name=infos["name"],
                   hp=infos["baseStats"]["hp"],
                   atk=infos["baseStats"]["atk"],
                   def_=infos["baseStats"]["def"],
                   atk_spe=infos["baseStats"]["spa"],
                   def_spe=infos["baseStats"]["spd"],
                   vit=infos["baseStats"]["spe"],
                   gen=infos["gen"],
                   type1=Type(infos["types"][0]),
                   type2=Type(infos["types"][1]) if len(infos["types"]) > 1 else None,
                   num_on_sprite_sheet=num_on_sprite_sheet,
                   EV=EV,
                   nature=nature,                   
                   nickname=nickname
    )
    
    return pokemon

"""charizard = create_pokemon(6)
print(charizard)"""