from pokemon import Pokemon
import pygame
from config import BLACK
from random import randint
from battle_timing  import Timing,timing_lock,current_timing,check_timing_talent
import ui_battle

def check_move(move_id: str):
    return move_id in ["move1", "move2", "move3", "move4"]

def turn(pokemon_1, pokemon_2, move_id_player, window, res_scene, resolution):
    """Exécute un tour complet de combat entre deux Pokémon."""

    # Nettoyage interface
    pygame.draw.rect(window, (0, 0, 0), (0, res_scene[1], resolution[0], resolution[1] - res_scene[1]))
    pygame.display.flip()

    # Vérification validité du move joueur
    if not check_move(move_id_player):
        raise Exception(f"Erreur : {move_id_player} n'est pas un move valide.")

    # Choix du move de l'IA
    move_id_ia = f"move{randint(1, len(pokemon_2.get_moveset()))}"
    if not check_move(move_id_ia):
        raise Exception(f"Erreur : {move_id_ia} n'est pas un move valide pour l'IA.")

    # Récupération des moves
    move_player = getattr(pokemon_1, move_id_player)
    move_ia = getattr(pokemon_2, move_id_ia)

    # Détermination de l'ordre : priorité > vitesse
    if move_player.prio > move_ia.prio:
        first, first_move_id = pokemon_1, move_id_player
        second, second_move_id = pokemon_2, move_id_ia
    elif move_ia.prio > move_player.prio:
        first, first_move_id = pokemon_2, move_id_ia
        second, second_move_id = pokemon_1, move_id_player
    else:
        first_from_trainer = True
        if pokemon_1.vit >= pokemon_2.vit:
            first, first_move_id = pokemon_1, move_id_player
            second, second_move_id = pokemon_2, move_id_ia
        else:
            first, first_move_id = pokemon_2, move_id_ia
            second, second_move_id = pokemon_1, move_id_player
            first_from_trainer = False

    # TIMING : ABOUT_TO_GET_HIT
    with timing_lock:
        Timing.current_timing = Timing.ABOUT_TO_GET_HIT
    check_timing_talent(first, second)

    # ATTAQUE DU PREMIER
    first, second = first.use_move(first_move_id, second, window)
    ui_battle.draw_hp_bar(window, first, from_trainer=first_from_trainer)

    # TIMING : GOT_HIT
    with timing_lock:
        Timing.current_timing = Timing.GOT_HIT
    check_timing_talent(first, second)

    # Log
    move = getattr(first, first_move_id)
    print(f"PP {first.name} {first_move_id}: {move.pp}, hp {second.name}: {second.hp}\n")

    pygame.time.delay(1500)

    # ATTAQUE DU SECOND SI VIVANT
    if not second.is_dead():
        with timing_lock:
            Timing.current_timing = Timing.ABOUT_TO_GET_HIT
        check_timing_talent(second, first)

        second, first = second.use_move(second_move_id, first, window)
        ui_battle.draw_hp_bar(window, second, from_trainer=not first_from_trainer)
        with timing_lock:
            Timing.current_timing = Timing.GOT_HIT
        check_timing_talent(second, first)

        move = getattr(second, second_move_id)
        print(f"PP {second.name} {second_move_id}: {move.pp}, hp {first.name}: {first.hp}\n")

        pygame.time.delay(1000)

    with timing_lock:
        Timing.current_timing = Timing.END

    return pokemon_1, pokemon_2, (not pokemon_1.is_dead() and not pokemon_2.is_dead())


"""
def battle(pokemon_trainer: Pokemon,pokemon_opponent: Pokemon):
    in_battle = True
    while in_battle and not pokemon_trainer.is_dead() and not pokemon_opponent.is_dead():
        pokemon_trainer,pokemon_opponent, in_battle = turn(pokemon_trainer,pokemon_opponent)
    return pokemon_trainer,pokemon_opponent, in_battle
"""