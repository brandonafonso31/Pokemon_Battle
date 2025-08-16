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

print(get_pokemon(6))