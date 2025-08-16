from pokemon import Pokemon
from pokemon_type import Type
from pokemon_move import *
from pokemon_nature import Nature
from pokemon_talent import talents
from config import pokemon_data_json_path
import json

def get_pokedex():
    with open(pokemon_data_json_path,"r",encoding="utf-8") as f:
        return json.load(f)
    
def get_pokemon(id):
    """Retourne le Pokémon dont le champ 'num' correspond à l'id"""
    pokedex = get_pokedex()
    for name, infos in pokedex.items():
        if infos["num"] == id:
            return infos
    return None

def create_pokemon(id,EV={"hp":0,"atk":0,"def_":0,"atk_spe":0,"def_spe":0,"vit":0},nickname=""):
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
                   num_on_sprite_sheet=infos["num"],
                   EV=EV,
                   nature=infos[""],
                   
                   nickname=nickname
    )
    
    return pokemon

"""charizard = create_pokemon(6)
print(charizard)"""