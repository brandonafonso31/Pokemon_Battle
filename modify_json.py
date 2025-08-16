from config import pokemon_data_json_path,data_dir_path
import json, os
from pokedex import get_pokemon
from pokemon_type import Type

gen1 = {"name": "gen1", "index": list(range(1, 152))}
gen2 = {"name": "gen2", "index": list(range(152, 252))}
gen3 = {"name": "gen3", "index": list(range(252, 387))}
gen4 = {"name": "gen4", "index": list(range(387, 494))}
gen5 = {"name": "gen5", "index": list(range(494, 650))}
gen6 = {"name": "gen6", "index": list(range(650, 722))}
gen7 = {"name": "gen7", "index": list(range(722, 810))}
gen8 = {"name": "gen8", "index": list(range(810, 906))}
#gen9 = {"name": "gen9", "index": list(range(906, 1026))}

all_gen = [gen1,gen2,gen3,gen4,gen5,gen6,gen7,gen8]

def create_new_json(gen):
    with open(pokemon_data_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        #print(len(data))
    
    json_file = {}
    for i in gen["index"]:
        if len(json_file) != i:     # évite d'ajouter les doublons pour l'instant (pas de méga ni de gigamax etc ...)
            poke = get_pokemon(i)
            if poke:
                json_file[i] = poke
        gen_path = os.path.join(os.path.dirname(pokemon_data_json_path), f"pokedex_{gen['name']}.json")
    
    with open(gen_path, "w", encoding="utf-8") as f:
        json.dump(json_file, f, indent=4, ensure_ascii=False)
    
    return json_file

#json_files = [create_new_json(gen) for gen in all_gen]
#print(len(json_files))

def remove_useless_attribut(json_file_path):
    path = os.path.join(data_dir_path, json_file_path)
    
    # Lire le JSON existant
    with open(path, "r", encoding="utf-8") as f:
        data_gen = json.load(f)
    
    # Liste des clés à supprimer
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
    
    # Nettoyer chaque Pokémon
    for poke_name, infos in data_gen.items():
        for key in useless_keys:
            infos.pop(key, None)  # supprime si existe, sinon ignore
    
    # Réécrire le JSON nettoyé
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data_gen, f, indent=4, ensure_ascii=False)

    print(f" Nettoyage terminé : {path}")
"""
for i in range(1,9):
    remove_useless_attribut(f"pokedex_gen{i}.json")"""
    
def translate_type(json_file_path,tab_translate):
    path = os.path.join(data_dir_path, json_file_path)
    
    # Lire le JSON existant
    with open(path, "r", encoding="utf-8") as f:
        data_gen = json.load(f)
    
    # Nettoyer chaque Pokémon
    for poke_name, infos in data_gen.items():
        if len(infos["types"]) == 2:
            infos["types"][0] = tab_translate[infos["types"][0]]
            infos["types"][1] = tab_translate[infos["types"][1]]
        else:   
            infos["types"][0] = tab_translate[infos["types"][0]]
    print(data_gen)
    # Réécrire le JSON nettoyé
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data_gen, f, indent=4, ensure_ascii=False)

    print(f" Nettoyage terminé : {path}")
    
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

print(len(tab_translate))
for i in range(1,9):
    translate_type(f"pokedex_gen{i}.json",tab_translate)