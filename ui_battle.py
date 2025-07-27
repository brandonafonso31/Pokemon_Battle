from button import *

def draw_move(window,move,x,y):
    """return a bool which is did the button got draw ?"""
    move_img_path = f"battle_ui/{move.type.name}_attack_button.png"
    move_img = pygame.image.load(move_img_path).convert_alpha()
    move_button = Button(x, y, move_img, 1)
    return move_button.draw(window)