import os

project_name = "Pokemon: Battle Project"
res_scene = (753,500)
resolution = (res_scene[0],253+res_scene[1])

principal_dir_path = os.getcwd()
img_dir_path = os.path.join(principal_dir_path,"images")
sprites_dir_path = os.path.join(img_dir_path,"sprites")
song_dir_path = os.path.join(principal_dir_path,"song")
data_dir_path = os.path.join(principal_dir_path,"data")
battle_json_path = os.path.join(data_dir_path, "actual_battle.json")
pokemon_data_json_path = os.path.join(data_dir_path, "pokedex.json")
sound_effect_dir_path = os.path.join(song_dir_path,"sound_effect")
cries_dir_path = os.path.join(song_dir_path,"cries")
background_dir_path = os.path.join(img_dir_path,"background")
sys_dir_path = os.path.join(img_dir_path,"sys")

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)

font_path = os.path.join("font", "pokemon_BW.otf")