from pokemon import Pokemon
import pygame
from config import BLACK
from random import randint

def check_move(move_id: str):
    return move_id in ["move1","move2","move3","move4"]
    
def attack(pokemon_attacker: Pokemon,pokemon_defender: Pokemon,move_id: str = "move1", ia: bool = False):
    if ia:
        move_id = f"move{randint(1,5)}"     # a modifier plus tard si vrai reflextion
    pokemon_attacker,pokemon_defender = pokemon_attacker.use_move(move_id,pokemon_defender)
    return pokemon_attacker,pokemon_defender,move_id

def perform_choice_attack(pokemon_1: Pokemon, pokemon_2: Pokemon, move_id: str,window,res_scene,resolution):
    pygame.draw.rect(window, BLACK, (0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
    pygame.display.flip()
    
    if not check_move(move_id):
        return Exception(f"Error: {move_id} n'est pass un attribut de Pokemon")
    ia = pokemon_2
    
    # check pour mettre le pokemon le plus rapide dans pokemon 1
    if pokemon_2.vit > pokemon_1.vit:
        pokemon_1,pokemon_2 = pokemon_2,pokemon_1
        ia = pokemon_1
    
    # Attaque du Pokémon le plus rapide
    pokemon_1, pokemon_2, move_id = attack(pokemon_1, pokemon_2, move_id, ia = (ia == pokemon_1))
    print(f"PP {pokemon_1.name} {move_id}: {pokemon_1.move1.pp}, Pv {pokemon_2.name}: {pokemon_2.pv}")      # barre de vie dans la fentre direct / pas d'affichage de pp
    pygame.time.delay(1500)
    
    # Si le Pokémon 2 (le moins rapide) n'est pas mort il attaque
    if not pokemon_2.is_dead():
        pokemon_2, pokemon_1,  move_id= attack(pokemon_2, pokemon_1, move_id, ia = (ia == pokemon_2))
        print(f"PP {pokemon_2.name} {move_id}: {pokemon_2.move1.pp}, Pv {pokemon_1.name}: {pokemon_1.pv}")  # barre de vie dans la fentre direct / pas d'affichage de pp
            
    pygame.time.delay(500)
    return pokemon_1,pokemon_2,not pokemon_2.is_dead() and not pokemon_1.is_dead()


"""
def battle(pokemon_trainer: Pokemon,pokemon_opponent: Pokemon):
    in_battle = True
    while in_battle and not pokemon_trainer.is_dead() and not pokemon_opponent.is_dead():
        pokemon_trainer,pokemon_opponent, in_battle = turn(pokemon_trainer,pokemon_opponent)
    return pokemon_trainer,pokemon_opponent, in_battle
"""