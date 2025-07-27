from button import *
from PIL import ImageColor
from config import img_dir_path
import os 

def draw_move(window,move,x,y):
    """return a bool which is did the button got draw ?"""
    move_img_path = os.path.join(img_dir_path,f"battle_ui/{move.type.name}_attack_button.png")
    move_img = pygame.image.load(move_img_path).convert_alpha()
    move_button = Button(x, y, move_img, 1,move.name,ImageColor.getrgb(move.type.color()))
    return move_button.draw(window)