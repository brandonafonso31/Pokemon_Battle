import json
import os
import pygame
from PIL import Image

def load_animation_config(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_animation_frames(name, config):
    data = config[name]
    path = os.path.join("animations", data["spritesheet"])
    img = Image.open(path).convert("RGBA")

    frames = []
    fw, fh = data["frame_width"], data["frame_height"]
    cols = img.width // fw
    zoom = data.get("zoom", 1)

    for i in range(data["total_frames"]):
        x = (i % cols) * fw
        y = (i // cols) * fh
        frame = img.crop((x, y, x + fw, y + fh))
        if zoom != 1:
            frame = frame.resize((fw * zoom, fh * zoom), Image.NEAREST)
        frames.append(frame)

    return frames, data["frame_duration"]

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