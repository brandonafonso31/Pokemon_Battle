from pokemon import Pokemon
import pygame
from config import BLACK
from random import randint

def check_move(move_id: str):
    return move_id in ["move1","move2","move3","move4"]

def check_prio(pokemon:Pokemon, move_id:str, pokemon_ia:Pokemon,move_id_ia:str):
    move = getattr(pokemon, move_id)
    move_ia = getattr(pokemon_ia,move_id_ia)
    if move_ia.prio > move.prio or pokemon_ia.vit > pokemon.vit:
        return pokemon_ia,move_id_ia,pokemon,move_id
    return pokemon,move_id,pokemon_ia,move_id_ia

def perform_choice_attack(pokemon_1: Pokemon, pokemon_2: Pokemon, move_id: str,window,res_scene,resolution):
    pygame.draw.rect(window, BLACK, (0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
    pygame.display.flip()
    
    if not check_move(move_id):
        return Exception(f"Error: {move_id} n'est pas un attribut du Pokemon Allié")
   
    # Changer ou non l'order selon la prio des attaques ou la vitesse des pokemon
    move_id_ia = f"move{randint(1,len(pokemon_2.get_moveset()))}"   # a modifier plus tard si vrai reflextion
    if not check_move(move_id_ia):
        return Exception(f"Error: {move_id_ia} n'est pas un attribut du Pokemon Ennemi")
    
    pokemon_1,move_id_1,pokemon_2,move_id_2 = check_prio(pokemon_1,move_id,pokemon_2,move_id_ia)

    # Attaque du Pokémon le plus rapide
    pokemon_1, pokemon_2 = pokemon_1.use_move(move_id,pokemon_2)
    print(f"PP {pokemon_1.name} {move_id}: {getattr(pokemon_1,move_id_1).pp}, Pv {pokemon_2.name}: {pokemon_2.pv}")  # barre de vie dans la fentre direct / pas d'affichage de pp
    pygame.time.delay(1500)
    
    # Si le Pokémon 2 (le moins rapide) n'est pas mort il attaque
    if not pokemon_2.is_dead():
        pokemon_2, pokemon_1 = pokemon_2.use_move(move_id_2,pokemon_1)
        print(f"PP {pokemon_2.name} {move_id_2}: {getattr(pokemon_2,move_id_2).pp}, Pv {pokemon_1.name}: {pokemon_1.pv}")  # barre de vie dans la fentre direct / pas d'affichage de pp
            
    pygame.time.delay(500)
    
    
    return pokemon_1, pokemon_2, (not pokemon_2.is_dead() and not pokemon_1.is_dead())


"""
def battle(pokemon_trainer: Pokemon,pokemon_opponent: Pokemon):
    in_battle = True
    while in_battle and not pokemon_trainer.is_dead() and not pokemon_opponent.is_dead():
        pokemon_trainer,pokemon_opponent, in_battle = turn(pokemon_trainer,pokemon_opponent)
    return pokemon_trainer,pokemon_opponent, in_battle
"""