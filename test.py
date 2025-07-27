import os
from PIL import Image

#-----Paramètres------------------------------------------------------------------------------------#
image = Image.open("battle_ui/french_commands.png")
i_range = 392,472
j_range = 43,91
filename = "battle_ui/button_attack.png"
#---------------------------------------------------------------------------------------------------#
new_i = 0
new_j = 0
button_attack = Image.new('RGBA', (i_range[1]-i_range[0], j_range[1]-j_range[0]), (255, 255, 255, 0))
print(button_attack.size)
for i in range(i_range[0],i_range[1]):
    for j in range(j_range[0],j_range[1]):
        pixel = image.getpixel((i,j))
        button_attack.putpixel((new_i,new_j), pixel)
        new_j+=1
    new_j = 0
    new_i+=1
button_attack.save(filename)
#---------------------------------------------------------------------------------------------------#