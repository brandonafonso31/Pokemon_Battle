from pokemon import *
import pygame
from pygame.locals import *

def attack(pokemon_attacker: Pokemon,pokemon_defender: Pokemon,move_id: str = "move1", ia: bool = False):
    if ia:
        move_id = "move1" # "move"+randint(1,5)
    pokemon_attacker,pokemon_defender = pokemon_attacker.use_move(move_id,pokemon_defender)
    return pokemon_attacker,pokemon_defender

def check_if_dead(pokemon):
    return pokemon.pv <= 0

def turn(pokemon_1: Pokemon,pokemon_2: Pokemon, move_id: int):
    if move_id not in ["move1","move2","move3","move4"]:
        return
    ia = pokemon_2
    # check pour s'assurer que le pokemon1 est plus rapide sinon on les inverse
    if pokemon_2.vit > pokemon_1.vit:
        pokemon_1,pokemon_2 = pokemon_2,pokemon_1
        ia = pokemon_1
        
    pokemon_1, pokemon_2 = attack(pokemon_1, pokemon_2, move_id, ia = (ia == pokemon_1))
    print(f"PP {pokemon_1.name} move1: {pokemon_1.move1.pp}, Pv {pokemon_2.name}: {pokemon_2.pv}")      # barre de vie dans la fentre direct / pas d'affichage de pp
    pygame.time.delay(2000)
    if not check_if_dead(pokemon_2):
        pokemon_2,pokemon_1= attack(pokemon_2, pokemon_1, move_id, ia = (ia == pokemon_2))
        print(f"PP {pokemon_2.name} move1: {pokemon_2.move1.pp}, Pv {pokemon_1.name}: {pokemon_1.pv}")  # barre de vie dans la fentre direct / pas d'affichage de pp
    else:
        pokemon_1,pokemon_2,not check_if_dead(pokemon_2)   
    return pokemon_1,pokemon_2,not check_if_dead(pokemon_2) and not check_if_dead(pokemon_1)

"""
def battle(pokemon_trainer: Pokemon,pokemon_opponent: Pokemon):
    in_battle = True
    while in_battle and not check_if_dead(pokemon_trainer) and not check_if_dead(pokemon_opponent):
        pokemon_trainer,pokemon_opponent, in_battle = turn(pokemon_trainer,pokemon_opponent)
    return pokemon_trainer,pokemon_opponent, in_battle
"""