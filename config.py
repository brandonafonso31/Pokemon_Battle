import os

res_scene = (1050,540)
resolution = (res_scene[0],260+res_scene[1])
principal_dir_path = os.getcwd()
img_dir_path = os.path.join(principal_dir_path,"images")
song_dir_path = os.path.join(principal_dir_path,"song")
battle_dir_path = os.path.join(principal_dir_path,"actual_battle")
battle_json_path = os.path.join(battle_dir_path, "battle.json")
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)