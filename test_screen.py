import pygame
from screen_manager import ScreenManager

pygame.init()
clock = pygame.time.Clock()

# Manager avec logique 750x750 mais fenêtre redimensionnable
screen = ScreenManager((750, 750), (1080, 1080), keep_ratio=True)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen.window_size = (event.w, event.h)

    # Dessin normal sur la surface logique
    surface = screen.get_surface()
    surface.fill((200, 200, 200))  # fond gris
    pygame.draw.circle(surface, (255, 0, 0), (375, 375), 100)  # cercle rouge centré

    # Mise à jour fenêtre avec scaling
    screen.update()
    clock.tick(60)

pygame.quit()
