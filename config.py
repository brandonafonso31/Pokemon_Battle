import os

project_name = "Pokemon: Battle Project"

res_screen_top = (753,500)
res_screen_bottom = res_screen_top
black_band_res = (max(res_screen_top[0],res_screen_bottom[0]),20)
resolution = (max(res_screen_top[0],res_screen_bottom[0],black_band_res[0]),res_screen_top[1]+black_band_res[1]+res_screen_bottom[1])

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

font_path = os.path.join("font", "pokemon_BW2.otf")