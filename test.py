import os
from PIL import Image,ImageColor
from pokemon_type import Type

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)
BLUE = (0, 0, 255, 255)
GREEN = (0, 255, 0, 255)


#-----Paramètres------------------------------------------------------------------------------------#
image = Image.open("battle_ui/move1_button.png")
#print(image.size)
length,height= image.size
"""#---------------------------------------------------------------------------------------------------#
button_attack = Image.new('RGBA', (length, height), (255, 255, 255, 0))
print(button_attack.size)
for i in range(length):
    for j in range(height):
        pixel = image.getpixel((i,j))
        if pixel != BLACK:
            pixel = RED
        button_attack.putpixel((i,j), pixel)
button_attack.save(filename)
#---------------------------------------------------------------------------------------------------#"""

types = list(Type)

for type in types:
    # Recharger une nouvelle copie de l’image d’origine à chaque tour
    image = Image.open("battle_ui/move_button.png").convert("RGBA")
    pixels = image.load()
    
    print(type, ImageColor.getrgb(type.color()))

    for i in range(image.width):
        for j in range(image.height):
            r, g, b, a = pixels[i, j]
            brightness = (r + g + b) / 3
            if brightness > 90 and a > 0:
                r, g, b = ImageColor.getrgb(type.color())
                pixels[i, j] = (r, g, b, a)

    image.save(f"battle_ui/{type.name}_attack_button.png")