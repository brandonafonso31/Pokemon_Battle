from pokemon import Pokemon
import pygame
from config import BLACK
from random import randint
from battle_timing  import Timing,timing_lock,current_timing 

def check_move(move_id: str):
    return move_id in ["move1","move2","move3","move4"]

def check_prio(pokemon:Pokemon, move_id:str, pokemon_ia:Pokemon,move_id_ia:str):
    move = getattr(pokemon, move_id)
    print(move,move.prio)
    move_ia = getattr(pokemon_ia,move_id_ia)
    print(move_ia,move_ia.prio)
    if move_ia.prio > move.prio or pokemon_ia.vit > pokemon.vit:
        return pokemon_ia,move_id_ia,pokemon,move_id, True
    return pokemon,move_id,pokemon_ia,move_id_ia,False

def check_timing_talent(pokemon: Pokemon):
    """Check if the timing is correct for the move"""
    timing_talent = pokemon.talent.timing
    with timing_lock:
        if current_timing == timing_talent :
            pokemon.talent.effect()  


def turn(pokemon_1: Pokemon, pokemon_ia: Pokemon, move_id: str,window,res_scene,resolution):
    with timing_lock:
        current_timing = Timing.Start
    check_timing_talent(pokemon_1)
    check_timing_talent(pokemon_2)
    pygame.draw.rect(window, BLACK, (0, res_scene[1], resolution[0], resolution[1]-res_scene[1]))
    pygame.display.flip()
    
    if not check_move(move_id):
        return Exception(f"Error: {move_id} n'est pas un attribut du Pokemon Allié")
   
    # Changer ou non l'order selon la prio des attaques ou la vitesse des pokemon
    move_id_ia = f"move{randint(1,len(pokemon_ia.get_moveset()))}"   # a modifier plus tard si vrai reflextion
    if not check_move(move_id_ia):
        return Exception(f"Error: {move_id_ia} n'est pas un attribut du Pokemon Ennemi")
    
    pokemon_1,move_id_1,pokemon_2,move_id_2,bool_change = check_prio(pokemon_1,move_id,pokemon_ia,move_id_ia)

    # Attaque du Pokémon le plus rapide
    with timing_lock:
        current_timing = Timing.ABOUT_TO_GET_HIT
    check_timing_talent(pokemon_1)
    check_timing_talent(pokemon_2)
    
    pokemon_1, pokemon_2 = pokemon_1.use_move(move_id_1,pokemon_2,window)
    with timing_lock:
        current_timing = Timing.GOT_HIT 
    check_timing_talent(pokemon_1)
    check_timing_talent(pokemon_2)
     
    print(f"PP {pokemon_1.name} {move_id_1}: {getattr(pokemon_1,move_id_1).pp}, Pv {pokemon_2.name}: {pokemon_2.pv}\n")  # barre de vie dans la fentre direct / pas d'affichage de pp
    pygame.time.delay(1500)
    
    # Si le Pokémon 2 (le moins rapide) n'est pas mort il attaque
    if not pokemon_2.is_dead():
        with timing_lock:
            current_timing = Timing.ABOUT_TO_GET_HIT
            check_timing_talent(pokemon_1)
            check_timing_talent(pokemon_2)
        pokemon_2, pokemon_1 = pokemon_2.use_move(move_id_2,pokemon_1,window)
        with timing_lock:
            current_timing = Timing.GOT_HIT
            check_timing_talent(pokemon_1)
            check_timing_talent(pokemon_2)
        print(f"PP {pokemon_2.name} {move_id_2}: {getattr(pokemon_2,move_id_2).pp}, Pv {pokemon_1.name}: {pokemon_1.pv}\n")  # barre de vie dans la fentre direct / pas d'affichage de pp
            
    pygame.time.delay(500)
    
    if bool_change:
        pokemon_1,pokemon_2 = pokemon_2, pokemon_1
    with timing_lock:
        current_timing = Timing.END
        check_timing_talent(pokemon_1)
        check_timing_talent(pokemon_2)
    
    return pokemon_1, pokemon_2, (not pokemon_2.is_dead() and not pokemon_1.is_dead())


"""
def battle(pokemon_trainer: Pokemon,pokemon_opponent: Pokemon):
    in_battle = True
    while in_battle and not pokemon_trainer.is_dead() and not pokemon_opponent.is_dead():
        pokemon_trainer,pokemon_opponent, in_battle = turn(pokemon_trainer,pokemon_opponent)
    return pokemon_trainer,pokemon_opponent, in_battle
"""