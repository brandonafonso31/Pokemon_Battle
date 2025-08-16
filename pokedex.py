from pokemon import Pokemon
from pokemon_type import Type
from pokemon_move import *
from pokemon_nature import Nature
from pokemon_talent import talents
from config import pokemon_data_json_path
import json

def pokedex():
    with open("pokemon_data_json_path","r") as f:
        return json.load(f)