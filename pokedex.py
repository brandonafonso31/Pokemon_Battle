from pokemon import Pokemon
from pokemon_type import Type
from pokemon_move import *
from pokemon_nature import Nature
from pokemon_talent import talents
from config import pokemon_data_json_path,data_dir_path,cries_dir_path
import json,os


def get_pokedex(num_gen: int = -1):
    if num_gen != -1: path = os.path.join(data_dir_path,f"pokedex_gen{num_gen}.json")
    else: path = pokemon_data_json_path
    with open(path,"r",encoding="utf-8") as f:
        return json.load(f)

def get_pokemon(id,num_gen: int = -1):
    pokedex = get_pokedex(num_gen)
    for index, infos in pokedex.items():
        if num_gen != -1 and int(index) == id :  return infos
        elif num_gen == -1 and infos["num"] == id: return infos
    return None

def get_gen(id: int):
    if id <= 0 : return None
    elif id <= 151: return 1
    elif id <= 251: return 2
    elif id <= 386: return 3
    elif id <= 493: return 4
    elif id <= 649: return 5
    elif id <= 721: return 6
    elif id <= 809: return 7
    elif id <= 905: return 8
    elif id <= 1010: return 9
    return None

def choice_talent(talents):
    input_choice = ""
    for keys,talent in talents.items():
        input_choice += f"{keys}: {talent}\n"
    
    choice = str.upper(input(input_choice))
    while choice not in talents.keys():
        choice = str.upper(input(input_choice))
    return choice
    
def create_pokemon(id,nature=Nature.BIZARRE,EV={"hp":0,"atk":0,"def_":0,"atk_spe":0,"def_spe":0,"vit":0},nickname="",num_on_sprite_sheet=1):
    num_gen = get_gen(id)
    infos = get_pokemon(id,num_gen)
    if infos is None:
        return None
    
    stats = infos["baseStats"]
    types = infos["types"]
    talents = infos["abilities"]
    english_name = infos["alias"]
    
    pokemon = Pokemon(name=infos["name"],
                   hp=stats["hp"],
                   atk=stats["atk"],
                   def_=stats["def"],
                   atk_spe=stats["spa"],
                   def_spe=stats["spd"],
                   vit=stats["spe"],
                   gen=num_gen,
                   type1=Type[types[0]],
                   type2=Type[types[1]] if len(types) > 1 else None,
                   num_on_sprite_sheet=num_on_sprite_sheet,
                   EV=EV,
                   nature=nature,                   
                   nickname=nickname,
                   talent=talents["0"], #     pour l'instant par défault toujours le 1er talent mais plus tard choice_talent(talents)
                   howl_path=os.path.join(cries_dir_path,f"{english_name}.mp3")
    )
    return pokemon

"""charizard_EV = {"hp":0,"atk":0,"def_":0,"atk_spe":252,"def_spe":6,"vit":252}
charizard = create_pokemon(6,nature=Nature.MODESTE,EV=charizard_EV,num_on_sprite_sheet=7)
print(charizard)
leviator_EV = {"hp":6,"atk":252,"def_":0,"atk_spe":0,"def_spe":0,"vit":252}
leviator = create_pokemon(130, EV=leviator_EV, nature=Nature.RIGIDE, num_on_sprite_sheet=151)
print(leviator)"""