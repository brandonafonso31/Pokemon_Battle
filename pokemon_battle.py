from config import song_dir_path,battle_json_path,background_dir_path,BLACK,res_screen_top,resolution
import ui_battle, os, sprite, pygame, json, sys, utils
from random import randint,choice
import battle_timing as bt

def start_battle(window, trainer, trainer_ia, \
    music_path="battle/trainer_BW.mp3", background="forest.jpg"):
    """Instancie les premiers éléments de la scène."""
    with open(battle_json_path, "r") as f:
        battle_data = json.load(f)

    #-----------------------------| MUSIC |------------------------------#
    music_path = os.path.join(song_dir_path, music_path)
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.3)
    utils.update_battle_json({"music": music_path})

    #---------------------------| BACKGROUND |---------------------------#
    background_path = os.path.join(background_dir_path, background)
    background = pygame.image.load(background_path).convert()
    window.blit(background, (0, 0))
    pygame.display.flip()
    utils.update_battle_json({"background": background_path})

    #---------------------| Gestion des étapes avec timer |---------------#
    clock = pygame.time.Clock()
    elapsed = 0
    step = 0
    pokemon_player, pokemon_opponent = None, None
    running = True

    while running:
        dt = clock.tick(30) / 1000 # accumulate le temps passé (en secondes)
        elapsed += dt
        
        if step == 0 and elapsed >= 1:  # après 2.5s : afficher ennemi
            pokemon_opponent = trainer_ia.send_next("front")
            ui_battle.refresh_opponent_side(window, pokemon_opponent)
            pygame.display.flip()
            step = 1
            elapsed = 0
            
        elif step == 1 and elapsed >= 1:  # après 5s : afficher joueur
            pokemon_player = trainer.send_next("back")
            ui_battle.refresh_player_side(window, pokemon_player)
            pygame.display.flip()
            step = 2
            running = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    return pokemon_player, pokemon_opponent, window


def check_move(move_id: str):
    return move_id in ["move1", "move2", "move3", "move4"]

def turn(pokemon_1, pokemon_2, move_id_player, window):
    """Exécute un tour complet de combat entre deux Pokémon."""
    global res_screen_top, resolution
    
    # Nettoyage interface
    menu_rect = pygame.Rect(0, res_screen_top[1], resolution[0], resolution[1] - res_screen_top[1])
    pygame.draw.rect(window, BLACK, menu_rect)
    pygame.display.update(menu_rect)

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
    elif move_player.prio < move_ia.prio:
        first, first_move_id = pokemon_2, move_id_ia
        second, second_move_id = pokemon_1, move_id_player
    else:
        if pokemon_1.vit > pokemon_2.vit:
            first, first_move_id = pokemon_1, move_id_player
            second, second_move_id = pokemon_2, move_id_ia
        elif pokemon_1.vit < pokemon_2.vit:
            first, first_move_id = pokemon_2, move_id_ia
            second, second_move_id = pokemon_1, move_id_player
        else:
            # Si les vitesses sont égales, déterminer l'ordre aléatoirement
            if choice([True, False]):
                first, first_move_id = pokemon_1, move_id_player
                second, second_move_id = pokemon_2, move_id_ia
            else:
                first, first_move_id = pokemon_2, move_id_ia
                second, second_move_id = pokemon_1, move_id_player

    # TIMING : ABOUT_TO_GET_HIT
    current_timing = bt.change_timing()
    bt.check_timing_talent(first, second)

    # ATTAQUE DU PREMIER
    elapsed = 0
    while True:
        dt = pygame.time.Clock().tick(30) / 1000
        elapsed += dt
        
        if elapsed >= 1:
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    first, second, old_hp = first.use_move(first_move_id, second, window)
    ui_battle.draw_hp_bar(window, second, from_trainer=(second is pokemon_1),old_hp=old_hp)
    
    # TIMING : GOT_HIT
    current_timing = bt.change_timing()
    bt.check_timing_talent(first, second)

    # Log
    move = getattr(first, first_move_id)
    print(f"PP {first.name} {first_move_id}: {move.pp}, hp {second.name}: {second.hp}\n")

    turn_running = not second.is_dead()
    clock = pygame.time.Clock()
    elapsed = 0    
    state = 0
    while turn_running:
        dt = clock.tick(30) / 1000
        elapsed += dt
        
        # ATTAQUE DU SECOND SI VIVANT
        if state == 0 and elapsed >= 1.5:
        
            current_timing = bt.change_timing()
            bt.check_timing_talent(second,first)

            second, first, old_hp = second.use_move(second_move_id, first, window)
            ui_battle.draw_hp_bar(window, first, from_trainer=(second is pokemon_2),old_hp=old_hp)    
                
            current_timing = bt.change_timing()
            bt.check_timing_talent(second,first)

            move = getattr(second, second_move_id)
            print(f"PP {second.name} {second_move_id}: {move.pp}, hp {first.name}: {first.hp}\n")
        
            state = 1
            elapsed = 0
            
        elif state == 1 and elapsed >= 3:
            turn_running = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
    current_timing = bt.change_timing()

    return pokemon_1, pokemon_2, "ko" if (pokemon_1.is_dead() or pokemon_2.is_dead()) else "continue"