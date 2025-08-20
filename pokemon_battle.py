from config import img_dir_path,song_dir_path,battle_json_path
from trainer import trainer,trainer_ai
import ui_battle, os, sprite, pygame, json

from config import BLACK
from random import randint
from battle_timing  import Timing,timing_lock,current_timing,check_timing_talent

def get_sprite(pokemon,front_or_back):
    pokemon_sprite = pokemon.sprites(front_or_back)
    pokemon_path = os.path.join(img_dir_path,f"sprites/pokemon_{front_or_back}.png")
    pokemon_sprite = pygame.image.load(pokemon_path).convert()
    pokemon_sprite.set_colorkey(sprite.get_first_pixel(pokemon_path))
    scale = 2 + (front_or_back == "back")
    pokemon_sprite = pygame.transform.scale(pokemon_sprite, (scale * 100,scale * 100))
    return pokemon_sprite

def get_opponent_sprite(res, pokemon):
    
    opponent_pokemon_sprite = get_sprite(pokemon,"front")
    path_sprite = os.path.join(img_dir_path,"sprites/pokemon_front.png")
    y_opponent = sprite.get_base_pixel(path_sprite)
    y_opponent = res[1]//2 + 2*(96 - y_opponent) - 300
    x_opponent = res[0]//2 + 75
    pokemon_json = {
        "path_sprite": path_sprite,
        "x": x_opponent,
        "y": y_opponent
    }
    update_battle_json({"pokemon_opponent": pokemon_json})
    
    return pokemon,opponent_pokemon_sprite, (x_opponent, y_opponent)

def get_trainer_sprite(res, pokemon):
    trainer_pokemon_sprite = get_sprite(pokemon,"back")
    path_sprite = os.path.join(img_dir_path,"sprites/pokemon_back.png")
    y_trainer = sprite.get_top_pixel(path_sprite)
    y_trainer = res[1] - 3*(96 - y_trainer) - 350
    x_trainer = res[0]//2 - 75*2 - 96*2
    pokemon_json = {
        "path_sprite": path_sprite,
        "x": x_trainer,
        "y": y_trainer
    }
    update_battle_json({"pokemon_trainer": pokemon_json})
    return pokemon,trainer_pokemon_sprite, (x_trainer, y_trainer)

def update_battle_json(updates: dict):
    path = battle_json_path

    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data.update(updates)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def get_image(image_path):
    image = pygame.image.load(image_path).convert()
    image.set_colorkey(sprite.get_first_pixel(image_path))
    return image,image.get_size()

def start_battle(window, res, trainer = trainer, trainer_ia  = trainer_ai, \
    music_path = "elite_four/Battle_Elite_Four_BW.mp3", background_path = "background/forest.jpg"):
    """Instancie les premiers éléments de la scène."""
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
    pokemon_opponent,opponent_pokemon_sprite,coord_opp = get_opponent_sprite(res, trainer_ia.pokemon_team[0])
    window.blit(opponent_pokemon_sprite,coord_opp)
    
    pokemon_opponent.play_howl()
    
    pokemon_opponent.add_rect(coord_opp)
    #--------------------------| SPRITE ALLIE |--------------------------#    
    pygame.display.flip()
    pygame.time.delay(500)
    pokemon_trainer,trainer_pokemon_sprite,coord_trainer = get_trainer_sprite(res, trainer.pokemon_team[0])
    window.blit(trainer_pokemon_sprite,coord_trainer)
    
    pokemon_trainer.play_howl()
    
    pokemon_trainer.add_rect(coord_trainer)
    
    ui_battle.draw_hp_bar(window, pokemon_trainer, from_trainer=True)
    ui_battle.draw_hp_bar(window, pokemon_opponent, from_trainer=False)
    
    update_battle_json({
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
    first_from_trainer = True
    if move_player.prio > move_ia.prio:
        first, first_move_id = pokemon_1, move_id_player
        second, second_move_id = pokemon_2, move_id_ia
    elif move_ia.prio > move_player.prio:
        first, first_move_id = pokemon_2, move_id_ia
        second, second_move_id = pokemon_1, move_id_player
        first_from_trainer = False
    else:
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
    pygame.time.delay(1000)
    first, second, old_hp = first.use_move(first_move_id, second, window)
    if second is pokemon_1:
        ui_battle.refresh_screen(window, pokemon_1, pokemon_2, old_hp_trainer=old_hp)
    else:
        ui_battle.refresh_screen(window, pokemon_1, pokemon_2, old_hp_opponent=old_hp)

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

        second, first, old_hp = second.use_move(second_move_id, first, window)
        if first is pokemon_1:
            ui_battle.refresh_screen(window, pokemon_1, pokemon_2, old_hp_trainer=old_hp)
        else:
            ui_battle.refresh_screen(window, pokemon_1, pokemon_2, old_hp_opponent=old_hp)
        with timing_lock:
            Timing.current_timing = Timing.GOT_HIT
        check_timing_talent(second, first)

        move = getattr(second, second_move_id)
        print(f"PP {second.name} {second_move_id}: {move.pp}, hp {first.name}: {first.hp}\n")

        pygame.time.delay(1000)

    with timing_lock:
        Timing.current_timing = Timing.END

    return pokemon_1, pokemon_2, "ko" if (pokemon_1.is_dead() or pokemon_2.is_dead()) else "continue"