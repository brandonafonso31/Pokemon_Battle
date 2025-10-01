from button import *
from PIL import ImageColor
from config import *
import os, json, sprite, button, sys, utils, pygame


def draw_move(manager, move, x, y):
    """Crée et dessine un bouton d'attaque"""
    surface = manager.get_surface()
    move_img_path = os.path.join(img_dir_path, f"battle_ui/{move.type.name}_attack_button.png")
    move_img = pygame.image.load(move_img_path).convert_alpha()
    move_button = button.Button(x, y, move_img, 1, move.name, ImageColor.getrgb(move.type.color()))
    move_button.draw(surface)
    return move_button


def get_color(ratio):
    if ratio > 0.5:
        return (0, 255, 0)       # Vert
    elif ratio > 0.2:
        return (255, 165, 0)     # Orange
    else:
        return (255, 0, 0)       # Rouge


def get_font_size(txt, rect, x):
    max_name_width = rect.width + x - 110
    font_size = 35
    name_font = pygame.font.Font(font_path, font_size)
    name_surface = name_font.render(txt, True, BLACK)

    while font_size > 10 and name_surface.get_width() > max_name_width:
        font_size -= 1
        name_font = pygame.font.Font(font_path, font_size)
        name_surface = name_font.render(txt, True, BLACK)
    return font_size


def draw_hp_bar(manager, pokemon, from_trainer, old_hp=None):
    surface = manager.get_surface()

    hp_bar_length = 250
    hp_bar_height = 20
    padding = 10

    if from_trainer:
        x = res_screen_top[0] - (hp_bar_length + 2 * padding)
        y = res_screen_top[1] // 2 + 100
    else:
        x, y = 2 * padding, 100

    hp_max = pokemon.hp_max if pokemon.hp_max > 0 else 1
    current_hp = pokemon.hp
    previous_hp = old_hp if old_hp is not None else current_hp

    current_length = int(hp_bar_length * (previous_hp / hp_max))
    target_length = int(hp_bar_length * (current_hp / hp_max))

    background_rect = pygame.Rect(
        x - padding,
        y - 40 - padding,
        hp_bar_length + 2 * padding,
        40 + hp_bar_height + 2 * padding
    )
    pokemon.hp_bar_rect = background_rect

    hp_font = pygame.font.Font(font_path, 30)
    name_pokemon_font = pygame.font.Font(font_path, get_font_size(pokemon.name, background_rect, x))

    if current_length > target_length:
        hp_step = max(1, (previous_hp - current_hp) // 20)
        anim_hp = previous_hp
        clock = pygame.time.Clock()
        elapsed = 0
        while anim_hp > current_hp or current_length > target_length:
            dt = clock.tick(30) / 1000
            elapsed += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if elapsed >= 0.05:
                if anim_hp > current_hp:
                    anim_hp = max(current_hp, anim_hp - hp_step)

                current_length = int(hp_bar_length * (anim_hp / hp_max))
                if current_length < target_length:
                    current_length = target_length

                color = get_color(current_length / hp_bar_length)

                pygame.draw.rect(surface, WHITE, background_rect)
                pygame.draw.rect(surface, BLACK, background_rect, 2)

                pygame.draw.rect(surface, (50, 50, 50), (x, y, hp_bar_length, hp_bar_height))
                bar_rect = (x, y, current_length, hp_bar_height)
                pygame.draw.rect(surface, color, bar_rect)

                text = name_pokemon_font.render(f"{pokemon.name}", True, BLACK)
                hp_surface = hp_font.render(f"HP : {anim_hp}/{hp_max}", True, BLACK)
                surface.blit(text, (x, y - 40))
                surface.blit(hp_surface, (x + hp_bar_length - 110, y - 40))

                manager.update()
                elapsed = 0
    else:
        bar_length = int(hp_bar_length * (current_hp / hp_max))

        pygame.draw.rect(surface, WHITE, background_rect)
        pygame.draw.rect(surface, BLACK, background_rect, 2)

        pygame.draw.rect(surface, (50, 50, 50), (x, y, hp_bar_length, hp_bar_height))
        bar_rect = (x, y, bar_length, hp_bar_height)
        color = get_color(current_hp / hp_max)
        pygame.draw.rect(surface, color, bar_rect)

        text = name_pokemon_font.render(f"{pokemon.name}", True, BLACK)
        hp_surface = hp_font.render(f"HP : {current_hp}/{hp_max}", True, BLACK)
        surface.blit(text, (x, y - 40))
        surface.blit(hp_surface, (x + hp_bar_length - 110, y - 40))


def refresh_pokemon_sprite(manager, pokemon, trainer_or_opponent, data=None):
    surface = manager.get_surface()
    if not pokemon.is_dead():
        if data is None:
            with open(battle_json_path, "r") as f:
                data = json.load(f)

        current_pokemon_id = data["current"]
        path = data[trainer_or_opponent][str(current_pokemon_id[trainer_or_opponent == "opponent"])]
        pokemon_sprite = pygame.image.load(path["path_sprite"]).convert()
        pokemon_sprite.set_colorkey(sprite.get_first_pixel(path["path_sprite"]))
        surface.blit(pokemon_sprite, (path["x"], path["y"]))


def refresh_player_side(manager, pokemon):
    if pokemon is not None and not pokemon.is_dead():
        refresh_pokemon_sprite(manager, pokemon, "trainer")
        draw_hp_bar(manager, pokemon, from_trainer=True)
        draw_pokeball_team(manager, pokemon.trainer, True)


def refresh_opponent_side(manager, pokemon):
    if pokemon is not None and not pokemon.is_dead():
        refresh_pokemon_sprite(manager, pokemon, "opponent")
        draw_hp_bar(manager, pokemon, from_trainer=False)
        draw_pokeball_team(manager, pokemon.trainer, False)


def refresh_screen(manager, pokemon_player, pokemon_opponent, old_hp_trainer=None, old_hp_opponent=None):
    surface = manager.get_surface()
    with open(battle_json_path, "r") as f:
        data = json.load(f)

    background = pygame.image.load(data["background"]).convert()
    surface.blit(background, (0, 0))

    refresh_player_side(manager, pokemon_player)
    refresh_opponent_side(manager, pokemon_opponent)


def get_correct_rect(pokemon, sprite_sheet):
    height = sprite_sheet.get_height()
    frame_width = sprite_sheet.get_width() // 3

    if pokemon is None:
        return pygame.Rect(frame_width * 2, 0, frame_width, height)
    if not pokemon.is_dead():
        return pygame.Rect(0, 0, frame_width, height)
    else:
        return pygame.Rect(frame_width, 0, frame_width, height)


def draw_pokeball_team(manager, trainer, is_player=True):
    surface = manager.get_surface()
    sheet = pygame.image.load(os.path.join(sys_dir_path, "bwicons_pokeball_sheet.png")).convert()
    frame_width = sheet.get_width() // 3

    padding = frame_width // 2 + 10
    if is_player:
        x, y = res_screen_top[0] - (6 * padding) - 20, res_screen_top[1] // 2 + 20
    else:
        x, y = 20, 20

    pokemon_team = trainer.pokemon_team + [None for _ in range(6 - len(trainer.pokemon_team))]
    for pokemon in pokemon_team:
        rect = get_correct_rect(pokemon, sheet)
        surface.blit(sheet, (x, y), rect)
        x += padding
    manager.update()


def refresh_pokeball_team(manager, player, opponent):
    draw_pokeball_team(manager, player, True)
    draw_pokeball_team(manager, opponent, False)
