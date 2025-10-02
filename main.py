import os, sys, pygame, pokemon_battle as pokemon_battle, ui_battle as ui_battle, json, sprite, pokemon_trainer, utils as utils
from config import *
from pygame.locals import *
from screen_manager import ScreenManager  # <-- ton gestionnaire de scaling

#------|Init pygame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
dt = 0

#------|Resolution avec ScreenManager
manager = ScreenManager(resolution)
pygame.display.set_caption(project_name)
pygame.display.set_icon(pygame.image.load(os.path.join(img_dir_path, "sys/logo.png")))

#------|Fonts
font = pygame.font.Font(font_path, 40)

#------|Var
BACKGROUND_INTRO = pygame.image.load(os.path.join(sys_dir_path, "intro.jpg"))
BACKGROUND_LENGHT, BACKGROUND_HEIGHT = BACKGROUND_INTRO.get_size()
ratio = res_screen_top[0] / BACKGROUND_LENGHT
ratio2 = res_screen_top[1] / BACKGROUND_HEIGHT
scale = (BACKGROUND_LENGHT * ratio, BACKGROUND_HEIGHT * ratio2)
BACKGROUND_INTRO = pygame.transform.scale(BACKGROUND_INTRO, scale)

BACKGROUND_TITLE_IMAGE = pygame.image.load(os.path.join(sys_dir_path, "pokemon_logo.png"))
BACKGROUND_TITLE_IMAGE = pygame.transform.scale(
    BACKGROUND_TITLE_IMAGE,
    (BACKGROUND_TITLE_IMAGE.get_width() // 5, BACKGROUND_TITLE_IMAGE.get_height() // 5)
)

#------|Button
BUTTON_LENGTH, BUTTON_HEIGHT = pygame.image.load(
    os.path.join(img_dir_path, "battle_ui", "move_button.png")
).get_size()

PLAY_BUTTON = utils.create_button("Jouer", (resolution[0] - BUTTON_LENGTH) // 2, res_screen_bottom[1] + black_band_res[1] + 25)
OPTIONS_BUTTON = utils.create_button("Options", (resolution[0] - BUTTON_LENGTH) // 2, res_screen_bottom[1] + black_band_res[1] + 175)
QUIT_BUTTON = utils.create_button("Quitter", (resolution[0] - BUTTON_LENGTH) // 2, res_screen_bottom[1] + black_band_res[1] + 325)

ATTACK_BUTTON = utils.create_button("Attaquer", (resolution[0] - 191) // 2, res_screen_bottom[1] + black_band_res[1] + 50)
POKEMON_BUTTON = utils.create_button("Pokémon", resolution[0] - 191 - 18, resolution[1] - 82 - 18)
BAG_BUTTON = utils.create_button("Sac", 18, resolution[1] - 82 - 18)
BACK_BUTTON = utils.create_button("Retour", (resolution[0] - 191) // 2, resolution[1] - 82 - 18)

#------|Menus adaptés
def pokemon_team_menu(manager, pokemon_player, pokemon_opponent):
    options_running = True
    while options_running:
        dt = clock.tick(30)
        surface = manager.get_surface()
        surface.fill(BLACK)

        utils.draw_text(manager, "Pokemon Team", font, "#b68f40", res_screen_bottom[0] // 2 - 200, res_screen_bottom[1] // 2)

        for button in [BACK_BUTTON]:
            button.draw(manager)
        
        for event in pygame.event.get():
            if BACK_BUTTON.handle_event(event, manager):
                options_running = False
            else: utils.pygame_event_handle(manager,event)

        manager.update()

    ui_battle.refresh_screen(manager, pokemon_player, pokemon_opponent)
    manager.update()


def bag_menu(manager, pokemon_player, pokemon_opponent):
    options_running = True
    while options_running:
        dt = clock.tick(30)
        surface = manager.get_surface()
        surface.fill(BLACK)

        utils.draw_text(manager, "Sac", font, "#b68f40", res_screen_bottom[0] // 2 - 200, res_screen_bottom[1] // 2)

        for button in [BACK_BUTTON]:
            button.draw(manager)
            
        for event in pygame.event.get():
            if BACK_BUTTON.handle_event(event, manager):
                options_running = False
            else: utils.pygame_event_handle(manager,event)

        manager.update()

    ui_battle.refresh_screen(manager, pokemon_player, pokemon_opponent)
    manager.update()


def ko(manager, pokemon_player, pokemon_opponent):
    trainer = pokemon_player.trainer
    opponent = pokemon_opponent.trainer

    clock = pygame.time.Clock()
    elapsed = 0
    pokemon_ko, front_or_back = (pokemon_player, "back") if pokemon_player.hp <= 0 else (pokemon_opponent, "front")
    ko_running = True
    state = 0
    while ko_running:
        dt = clock.tick(30) / 1000
        elapsed += dt
        surface = manager.get_surface()

        for event in pygame.event.get():
            utils.pygame_event_handle(manager,event)

        if state == 0 and elapsed >= 0.5:
            utils.print_log_ingame(manager, f"{pokemon_ko.name} {'ennemi' if pokemon_ko is pokemon_opponent else 'allié'} est KO")
            state = 1; elapsed = 0

        elif state == 1 and elapsed >= 2:
            pokemon_ko.animate_death(manager, front_or_back)
            state = 2; elapsed = 0

        elif state == 2 and elapsed >= 2:
            if pokemon_ko is pokemon_player:
                new_pokemon = trainer.send_next(manager, "back")
                if new_pokemon is None:
                    return new_pokemon, pokemon_opponent, False
                pokemon_player = new_pokemon
                utils.print_log_ingame(manager, f"{pokemon_player.name} est envoyé par {trainer.name} !")
                ui_battle.refresh_player_side(surface, pokemon_player)
            else:
                new_pokemon = opponent.send_next(manager, "front")
                if new_pokemon is None:
                    return pokemon_player, pokemon_opponent, False
                pokemon_opponent = new_pokemon
                utils.print_log_ingame(manager, f"{pokemon_opponent.name} est envoyé par {opponent.name} !")
                ui_battle.refresh_opponent_side(surface, pokemon_opponent)

            utils.check_hp_to_change_music(pokemon_player)
            state = 3; elapsed = 0

        elif state == 3 and elapsed >= 2:
            ko_running = False

        manager.update()

    surface.blit(BACKGROUND_IMAGE_BOTTOM, (res_screen_bottom[0] - BACKGROUND_IMAGE_BOTTOM.get_width(),
                                           res_screen_bottom[1] + black_band_res[1]))
    return pokemon_player, pokemon_opponent, not (pokemon_player is None or pokemon_opponent is None)


def attack_menu(manager, pokemon_player, pokemon_opponent):
    surface = manager.get_surface()
    surface.blit(BACKGROUND_IMAGE_BOTTOM, (res_screen_bottom[0] - BACKGROUND_IMAGE_BOTTOM.get_width(),
                                           res_screen_bottom[1] + black_band_res[1]))
    moves_available = pokemon_player.get_moveset()

    button_padding = 20
    center = (resolution[0] // 2, resolution[1] - res_screen_bottom[1] // 2)
    list_coord = [
        (center[0] - BUTTON_LENGTH - button_padding, center[1] - BUTTON_HEIGHT - button_padding),
        (center[0] + button_padding, center[1] - BUTTON_HEIGHT - button_padding),
        (center[0] - BUTTON_LENGTH - button_padding, center[1]),
        (center[0] + button_padding, center[1])
    ]

    turn_running = True
    battle_running = True
    while turn_running:
        dt = clock.tick(30)
        surface = manager.get_surface()

        moves_button = [ui_battle.draw_move(manager, move, coord[0], coord[1]) for move, coord in zip(moves_available, list_coord)]
        BACK_BUTTON.draw(manager)

        for event in pygame.event.get():
            for i, button in enumerate(moves_button):
                if button.handle_event(event, manager):
                    pokemon_player, pokemon_opponent, battle_state = \
                        utils.start_turn(manager, pokemon_player, pokemon_opponent, moves_available, i)
                    if battle_state != "choose_attack":
                        if battle_state == "ko":
                            return ko(manager, pokemon_player, pokemon_opponent)
                        elif battle_state == "continue":
                            return pokemon_player, pokemon_opponent, battle_running
            if BACK_BUTTON.handle_event(event, manager):
                turn_running = False
            else: utils.pygame_event_handle(manager,event)

        manager.update()

    return pokemon_player, pokemon_opponent, battle_running


def battle_menu(manager):
    battle_running = True
    trainer, opponent = pokemon_trainer.init_trainer()
    bg_path = os.path.join(background_dir_path, "bg-forest.png")
    pokemon_player, pokemon_opponent = pokemon_battle.start_battle(manager, trainer, opponent, background=bg_path)
    elapsed = 0
    state = ""
    showing_menu = True
    while battle_running:
        dt = clock.tick(30) / 1000
        elapsed += dt
        surface = manager.get_surface()

        if showing_menu and state not in ["ko", "end"]:
            surface.blit(BACKGROUND_IMAGE_BOTTOM, (res_screen_bottom[0] - BACKGROUND_IMAGE_BOTTOM.get_width(),
                                                   res_screen_bottom[1] + black_band_res[1]))
            utils.print_log_ingame(manager, f"Que dois faire {pokemon_player.name} ?")
            for button in [ATTACK_BUTTON, BAG_BUTTON, POKEMON_BUTTON]:
                button.draw(manager)
            showing_menu = False

        elif state == "ko" and elapsed >= 3:
            winner, loser = pokemon_trainer.get_winner(trainer, opponent)
            utils.print_log_ingame(manager, f"{winner.name} a vaincu {loser.name} !", reset=True)
            elapsed = 0; state = "end"

        elif state == "end" and elapsed >= 2:
            battle_running = False

        
        for event in pygame.event.get():
            if ATTACK_BUTTON.handle_event(event, manager):
                pokemon_player, pokemon_opponent, battle_running = attack_menu(manager, pokemon_player, pokemon_opponent)
                if not battle_running:
                    state = "ko"; battle_running = True
                showing_menu = True
            if BAG_BUTTON.handle_event(event, manager):
                bag_menu(manager, pokemon_player, pokemon_opponent)
                showing_menu = True
            if POKEMON_BUTTON.handle_event(event, manager):
                pokemon_team_menu(manager, pokemon_player, pokemon_opponent)
                showing_menu = True
            else: utils.pygame_event_handle(manager,event)

        manager.update()


def options_menu(manager):
    options_running = True
    while options_running:
        dt = clock.tick(30)
        surface = manager.get_surface()
        surface.fill(BLACK)

        utils.draw_text(manager, "OPTIONS", font, "#b68f40", res_screen_bottom[0] // 2 + 200, res_screen_bottom[1] // 2)
        for button in [BACK_BUTTON]:
            button.draw(manager)

        
        for event in pygame.event.get():
            if BACK_BUTTON.handle_event(event, manager):
                options_running = False
            else: utils.pygame_event_handle(manager,event)

        manager.update()


def main_menu(manager):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join(song_dir_path, "sys/title.mp3"))
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.3)

    run = True
    while run:
        dt = clock.tick(30)
        surface = manager.get_surface()
        surface.fill(BLACK)

        surface.blit(BACKGROUND_INTRO, (0, 0))
        surface.blit(BACKGROUND_TITLE_IMAGE, ((res_screen_bottom[0] - BACKGROUND_TITLE_IMAGE.get_width()) // 2, 0))
        surface.blit(BACKGROUND_IMAGE_BOTTOM, (res_screen_bottom[0] - BACKGROUND_IMAGE_BOTTOM.get_width(),
                                               res_screen_bottom[1] + black_band_res[1]))

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.draw(manager)

        
        for event in pygame.event.get():
            if PLAY_BUTTON.handle_event(event, manager):
                battle_menu(manager); pygame.quit(); sys.exit()
            if OPTIONS_BUTTON.handle_event(event, manager):
                print("BUTTON CLICKED!")
                options_menu(manager)
            if QUIT_BUTTON.handle_event(event, manager):
                pygame.quit(); sys.exit()
            else: utils.pygame_event_handle(manager,event)

        manager.update()


main_menu(manager)
