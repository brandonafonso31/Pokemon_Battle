from pokemon import Pokemon
from pokemon_type import Type
from pokemon_move import *
from pokemon_nature import Nature
from pokemon_talent import talents

def pokedex():
    with open("","") as f:
        return json.load(f)