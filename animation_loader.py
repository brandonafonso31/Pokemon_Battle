import json
import os
from PIL import Image
from config import img_dir_path

def load_animation_config(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_animation_frames(name, config):
    data = config[name]
    path = os.path.join(img_dir_path, data["spritesheet"])
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