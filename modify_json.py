from config import pokemon_data_json_path,data_dir_path
import json, os
from pokedex import get_pokemon
from pokemon_type import Type

def create_new_json(gen):
    with open(pokemon_data_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    json_file = {}
    for i in gen["index"]:
        poke = get_pokemon(i)
        if poke:
            json_file[i] = poke
    
    gen_path = os.path.join(os.path.dirname(pokemon_data_json_path), f"pokedex_{gen['name']}.json")    
    with open(gen_path, "w", encoding="utf-8") as f:
        json.dump(json_file, f, indent=4, ensure_ascii=False)
    
    return json_file


def remove_useless_attribut(json_file_path):
    path = os.path.join(data_dir_path, json_file_path)
    with open(path, "r", encoding="utf-8") as f:
        data_gen = json.load(f)
    
    useless_keys = [
        "genderRatio","heightm","weightkg","color","evos","eggGroups","hasLearnset",
        "baseForme","baseFormeAlias","baseFormeSprite",
        "cosmeticFormes","cosmeticFormesAliases","cosmeticFormesSprites",
        "otherFormes","otherFormesAliases","otherFormesSprites",
        "formeOrder","prevo","evoLevel","canGigantamax","baseSpecies",
        "forme","requiredItem","changesFrom","evoType","gender","gen",
        "evoItem","evoCondition","canHatch","evoMove","maxHP",
        "requiredAbility","battleOnly","requiredMove","requiredItems",
        "unreleasedHidden","cannotDynamax","alias","sprite"
    ]
    
    for poke_name, infos in data_gen.items():
        for key in useless_keys:
            infos.pop(key, None)  # supprime si existe, sinon ignore
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data_gen, f, indent=4, ensure_ascii=False)
    
    
def translate_type(json_file_path,tab_translate):
    path = os.path.join(data_dir_path, json_file_path)
    
    with open(path, "r", encoding="utf-8") as f:
        data_gen = json.load(f)
    
    for poke_name, infos in data_gen.items():
        if len(infos["types"]) == 2:
            infos["types"][0] = tab_translate[infos["types"][0]]
            infos["types"][1] = tab_translate[infos["types"][1]]
        else:   
            infos["types"][0] = tab_translate[infos["types"][0]]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data_gen, f, indent=4, ensure_ascii=False)
    
    
def translate_name(json_file_path,start = 1):
    with open("data/fr_indexed.json","r",encoding="utf-8") as f:
        fr_data = json.load(f)
        
    path = os.path.join(data_dir_path, json_file_path)
    with open(path, "r", encoding="utf-8") as f:
        data_gen = json.load(f)
    
    #print(fr_data)
    
    i = start
    for poke_name, infos in data_gen.items():
        infos["name"] = fr_data[str(i)]
        i+=1
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data_gen, f, indent=4, ensure_ascii=False)

        
start_gen = [1,152,252,387,494,650,722,810]        
end_gen = [151,251,386,493,649,721,809,906]
gen1 = {"name": "gen1", "index": list(range(start_gen[0], end_gen[0] + 1))}
gen2 = {"name": "gen2", "index": list(range(start_gen[1], end_gen[1] + 1))}
gen3 = {"name": "gen3", "index": list(range(start_gen[2], end_gen[2] + 1))}
gen4 = {"name": "gen4", "index": list(range(start_gen[3], end_gen[3] + 1))}
gen5 = {"name": "gen5", "index": list(range(start_gen[4], end_gen[4] + 1))}
gen6 = {"name": "gen6", "index": list(range(start_gen[5], end_gen[5] + 1))}
gen7 = {"name": "gen7", "index": list(range(start_gen[6], end_gen[6] + 1))}
gen8 = {"name": "gen8", "index": list(range(start_gen[7], end_gen[7] + 1))}
#gen9 = {"name": "gen9", "index": list(range(906, 1026))}
all_gen = [gen1,gen2,gen3,gen4,gen5,gen6,gen7,gen8]

tab_translate = {"Normal":"NORMAL",
                    "Fire":"FEU",
                    "Grass":"PLANTE",
                    "Water":"EAU",
                    "Bug":"INSECTE",
                    "Steel":"ACIER",
                    "Poison":"POISON",
                    "Electric":"ELECTRIQUE",
                    "Ground":"SOL",
                    "Fairy":"FEE",  
                    "Fighting":"COMBAT",
                    "Rock":"ROCHE",  
                    "Psychic":"PSY",
                    "Ice":"GLACE",
                    "Dragon":"DRAGON",
                    "Ghost":"SPECTRE",
                    "Flying":"VOL",
                    "Dark":"TENEBRE" }


def index_json():
    with open("data/fr.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    indexed_data = {str(i+1): name for i, name in enumerate(data)}
    with open("data/fr_indexed.json", "w", encoding="utf-8") as f:
        json.dump(indexed_data, f, indent=4, ensure_ascii=False)

index_json()
for i in range(1,len(all_gen)+1):
    create_new_json(all_gen[i-1])
    remove_useless_attribut(f"pokedex_gen{i}.json")
    translate_type(f"pokedex_gen{i}.json",tab_translate)
    translate_name(f"pokedex_gen{i}.json",start_gen[i-1])