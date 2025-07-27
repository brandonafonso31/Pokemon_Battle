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
