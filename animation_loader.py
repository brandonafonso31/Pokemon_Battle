import pygame
import json


def load_animation_config(json_path):
    with open(json_path, "r") as f:
        return json.load(f)

def load_animation_frames(config):
    sheet = pygame.image.load(config["sheet"]).convert_alpha()
    frame_width, frame_height = config["frame_size"]
    rows = config["rows"]
    cols = config["cols"]

    frames = []
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
            frames.append(sheet.subsurface(rect))
    return frames

def play_attack_animation(move_name, window, target_pos):
    if move_name not in animation_data:
        return  # Pas d'anim disponible pour ce move
    
    config = animation_data[move_name]
    frames = load_animation_frames(config)
    offset = config.get("offset", [0, 0])
    duration = config.get("frame_duration", 60)

    x, y = target_pos[0] + offset[0], target_pos[1] + offset[1]
    for frame in frames:
        window.blit(frame, (x, y))
        pygame.display.flip()
        pygame.time.delay(duration)
        

animation_data = load_animation_config("animations/animations.json")