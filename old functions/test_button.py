import pygame, sys, os 
from screen_manager import ScreenManager
from button import Button
from pygame.locals import *

pygame.init()

# reprend ta classe ScreenManager (ou colle la version ci-dessus)
# et ta classe Button (avec handle_event modifié)...

mgr = ScreenManager(logical_size=(400,300))
img = pygame.Surface((160,60))
img.fill((200,200,200))
pygame.draw.rect(img, (100,100,250), (0,0,160,60), 4)
btn = Button(120, 120, img, 1, "Test")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit()
        if btn.handle_event(event, mgr):
            print("BUTTON CLICKED!")

    mgr.get_surface().fill((10,10,10))
    btn.draw(mgr)
    mgr.update()
