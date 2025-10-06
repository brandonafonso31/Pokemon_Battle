from config import song_dir_path, battle_json_path, background_dir_path, BLACK, res_screen_top, resolution, res_screen_bottom, black_band_res, BACKGROUND_IMAGE_BOTTOM
import ui_battle as ui_battle, os, sprite, pygame, json, sys, utils
from random import randint, choice, random
import battle_timing as bt


def start_battle(manager, player, opponent, background="forest.jpg"):
    """Instancie les premiers éléments de la scène."""
    print(bt.current_timing)
    surface = manager.get_surface()

    # --- fond inférieur
    surface.blit(BACKGROUND_IMAGE_BOTTOM, (
        res_screen_bottom[0] - BACKGROUND_IMAGE_BOTTOM.get_width(),
        res_screen_bottom[1] + black_band_res[1]
    ))

    # --- musique
    music_path = os.path.join(song_dir_path, "battle", opponent.theme)
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.3)
    utils.update_battle_json({"opponent_theme": music_path, "music": music_path})

    # --- background
    background_path = os.path.join(background_dir_path, background)
    background_img = pygame.image.load(background_path).convert()
    surface.blit(background_img, (0, 0))
    manager.update()
    utils.update_battle_json({"background": background_path})

    # --- pokeballs team
    ui_battle.refresh_pokeball_team(manager, player, opponent)

    # --- sprite trainer
    utils.delay_flat(1,manager)
    surface.blit(opponent.get_opponent_sprite(), opponent.sprite_coord)
    manager.update()
    utils.delay_flat(1,manager)
    utils.print_log_ingame(manager, f"{opponent.name} vous défie dans un duel au sommet !", reset=True)
    utils.delay_flat(1,manager)
    opponent.move_to_right(manager)
    utils.delay_flat(0.5,manager)

    # --- sprites pokémon
    clock = pygame.time.Clock()
    elapsed = 0
    step = 0
    pokemon_player, pokemon_opponent = None, None
    running = True

    while running:
        dt = clock.tick(30) / 1000
        elapsed += dt

        if step == 0:
            pokemon_opponent = opponent.send_next(manager, "front")
            ui_battle.refresh_opponent_side(manager, pokemon_opponent)
            step = 1
            elapsed = 0

        elif step == 1 and elapsed >= 4:
            pokemon_player = player.send_next(manager, "back")
            ui_battle.refresh_player_side(manager, pokemon_player)
            step = 2
            elapsed = 0

        elif step == 2 and elapsed >= 2:
            running = False

        for event in pygame.event.get():
            utils.pygame_event_handle(manager,event)


        manager.update()

    bt.check_timing_talent(pokemon_player, pokemon_opponent)
    return pokemon_player, pokemon_opponent


def check_move(move_id: str):
    return move_id in ["move1", "move2", "move3", "move4"]


def turn(pokemon_1, pokemon_2, move_id_player, manager):
    """Exécute un tour complet de combat entre deux Pokémon."""
    surface = manager.get_surface()

    # --- nettoyer interface
    surface.blit(BACKGROUND_IMAGE_BOTTOM, (
        res_screen_bottom[0] - BACKGROUND_IMAGE_BOTTOM.get_width(),
        res_screen_bottom[1] + black_band_res[1]
    ))
    manager.update()

    # --- vérif move joueur
    if not check_move(move_id_player):
        raise Exception(f"Erreur : {move_id_player} n'est pas un move valide.")

    # --- move IA
    move_id_ia = f"move{randint(1, len(pokemon_2.get_moveset()))}"
    if not check_move(move_id_ia):
        raise Exception(f"Erreur : {move_id_ia} n'est pas un move valide pour l'IA.")

    # --- récup moves
    move_player = getattr(pokemon_1, move_id_player)
    move_ia = getattr(pokemon_2, move_id_ia)

    # --- prio / vitesse
    first, first_move_id, second, second_move_id = utils.get_prio(
        pokemon_1, pokemon_2, move_player, move_ia, move_id_player, move_id_ia
    )

    # --- timing talents
    current_timing = bt.change_timing()
    bt.check_timing_talent(first, second)

    # --- attaque du premier
    utils.delay_flat(1,manager)

    success_rate = utils.get_success_rate(first, second, first_move_id)
    if random() <= success_rate:
        first, second, old_hp = first.use_move(first_move_id, second, manager)
        ui_battle.draw_hp_bar(manager, second, from_trainer=(second is pokemon_1), old_hp=old_hp)
    else:
        utils.print_log_ingame(manager, f"{first.name} rate son attaque !", reset=True)

    current_timing = bt.change_timing()
    bt.check_timing_talent(first, second)

    utils.check_hp_to_change_music(pokemon_1)

    move = getattr(first, first_move_id)
    print(f"PP {first.name} {first_move_id}: {move.pp}, hp {second.name}: {second.hp}\n")

    # --- tour du second
    turn_running = not second.is_dead()
    clock = pygame.time.Clock()
    elapsed = 0
    state = 0

    while turn_running:
        dt = clock.tick(30) / 1000
        elapsed += dt

        if state == 0 and elapsed >= 1.5:
            current_timing = bt.change_timing(bt.Timing.ABOUT_TO_GET_HIT)
            bt.check_timing_talent(second, first)

            success_rate = utils.get_success_rate(second, first, second_move_id)
            if random() <= success_rate:
                second, first, old_hp = second.use_move(second_move_id, first, manager)
                ui_battle.draw_hp_bar(manager, first, from_trainer=(second is pokemon_2), old_hp=old_hp)
            else:
                utils.print_log_ingame(manager, f"{second.name} rate son attaque !", reset=True)

            current_timing = bt.change_timing()
            bt.check_timing_talent(second, first)

            utils.check_hp_to_change_music(pokemon_1)

            move = getattr(second, second_move_id)
            print(f"PP {second.name} {second_move_id}: {move.pp}, hp {first.name}: {first.hp}\n")

            state = 1
            elapsed = 0

        elif state == 1 and elapsed >= 3:
            turn_running = False

        for event in pygame.event.get():
            utils.pygame_event_handle(manager,event)

        manager.update()

    current_timing = bt.change_timing()

    return pokemon_1, pokemon_2, "ko" if (pokemon_1.is_dead() or pokemon_2.is_dead()) else "continue"
