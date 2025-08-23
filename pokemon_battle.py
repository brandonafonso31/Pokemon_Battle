from config import img_dir_path,song_dir_path,battle_json_path,sprites_dir_path
import ui_battle, os, sprite, pygame, json

from config import BLACK
from random import randint
import battle_timing as bt

def start_battle(window, res, trainer, trainer_ia , \
    music_path = "elite_four/Battle_Elite_Four_BW.mp3", background_path = "background/forest.jpg"):
    """Instancie les premiers éléments de la scène."""
    with open(battle_json_path,"r") as f:
        battle_data = json.load(f)
    #-----------------------------| MUSIC |------------------------------#
    music_path = os.path.join(song_dir_path,music_path)
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.3)
    #---------------------------| BACKGROUND |---------------------------#
    background_path = os.path.join(img_dir_path,background_path)
    background = pygame.image.load(background_path).convert()
    window.blit(background,(0,0))
    pygame.display.flip()
    #-------------------------| SPRITE ENNEMI |--------------------------#
    pygame.time.delay(500)
    pokemon_opponent,boolean = trainer_ia.send_next("front")
    pokemon_opponent_sprite_path = os.path.join(sprites_dir_path,f"pokemon_front_1.png")
    pokemon_opponent_sprite = sprite.get_image(pokemon_opponent_sprite_path,scale=2)
    coord_opp = battle_data["opponent"]["1"]["x"],battle_data["opponent"]["1"]["y"]
    window.blit(pokemon_opponent_sprite,coord_opp)
    pokemon_opponent.add_rect(coord_opp,scale=2)
    pygame.display.flip()
    #--------------------------| SPRITE ALLIE |--------------------------#    
    pygame.time.delay(500)
    pokemon_trainer,boolean = trainer.send_next("back")    
    pokemon_trainer_sprite_path = os.path.join(sprites_dir_path,f"pokemon_back_1.png")
    pokemon_trainer_sprite = sprite.get_image(pokemon_trainer_sprite_path,scale=3)
    coord_opp = battle_data["trainer"]["1"]["x"],battle_data["trainer"]["1"]["y"] 
    window.blit(pokemon_trainer_sprite,coord_opp)
    pokemon_opponent.add_rect(coord_opp,scale=3)
    pygame.display.flip()
    #----------------------------| HP BAR |-----------------------------#
    pygame.time.delay(500)
    ui_battle.draw_hp_bar(window, pokemon_trainer, from_trainer=True)
    ui_battle.draw_hp_bar(window, pokemon_opponent, from_trainer=False)
    
    sprite.update_battle_json({
        "music": music_path,
        "background": background_path
    })  
    
    ui_battle.refresh_screen(window,pokemon_trainer, pokemon_opponent)
    return pokemon_trainer,pokemon_opponent,window

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
        if pokemon_1.vit >= pokemon_2.vit:
            first, first_move_id = pokemon_1, move_id_player
            second, second_move_id = pokemon_2, move_id_ia
        else:
            first, first_move_id = pokemon_2, move_id_ia
            second, second_move_id = pokemon_1, move_id_player

    # TIMING : ABOUT_TO_GET_HIT
    current_timing = bt.change_timing()
    bt.check_timing_talent(first, second)

    # ATTAQUE DU PREMIER
    pygame.time.delay(1000)
    first, second, old_hp = first.use_move(first_move_id, second, window)
    if second is pokemon_1:
        ui_battle.refresh_screen(window, pokemon_1, pokemon_2, old_hp_trainer=old_hp)
    else:
        ui_battle.refresh_screen(window, pokemon_1, pokemon_2, old_hp_opponent=old_hp)

    # TIMING : GOT_HIT
    current_timing = bt.change_timing()
    bt.check_timing_talent(first, second)

    # Log
    move = getattr(first, first_move_id)
    print(f"PP {first.name} {first_move_id}: {move.pp}, hp {second.name}: {second.hp}\n")

    pygame.time.delay(1500)

    # ATTAQUE DU SECOND SI VIVANT
    if not second.is_dead():
        
        current_timing = bt.change_timing()
        bt.check_timing_talent(second,first)

        second, first, old_hp = second.use_move(second_move_id, first, window)
        if first is pokemon_1:
            ui_battle.refresh_screen(window, pokemon_1, pokemon_2, old_hp_trainer=old_hp)
        else:
            ui_battle.refresh_screen(window, pokemon_1, pokemon_2, old_hp_opponent=old_hp)
            
        current_timing = bt.change_timing()
        bt.check_timing_talent(second,first)

        move = getattr(second, second_move_id)
        print(f"PP {second.name} {second_move_id}: {move.pp}, hp {first.name}: {first.hp}\n")

        pygame.time.delay(1000)

    current_timing = bt.change_timing()

    return pokemon_1, pokemon_2, "ko" if (pokemon_1.is_dead() or pokemon_2.is_dead()) else "continue"