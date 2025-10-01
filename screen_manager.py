import pygame

class ScreenManager:
    def __init__(self, logical_size=(750, 750), window_size=(750,750), keep_ratio=True):
        self.logical_size = logical_size
        self.window_size = window_size
        self.keep_ratio = keep_ratio

        # Fenêtre redimensionnable
        self.window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
        pygame.display.set_caption("Pokemon Clone")

        # Surface logique (où tu dessines ton jeu)
        self.surface = pygame.Surface(logical_size)

    def get_surface(self):
        """Retourne la surface logique pour dessiner dessus"""
        return self.surface

    def update(self):
        """Scale la surface logique et affiche sur la vraie fenêtre"""
        window_w, window_h = self.window.get_size()
        logical_w, logical_h = self.logical_size

        if self.keep_ratio:
            # Calcul du scale tout en gardant le ratio
            scale = min(window_w / logical_w, window_h / logical_h)
            new_w, new_h = int(logical_w * scale), int(logical_h * scale)
            scaled_surface = pygame.transform.smoothscale(self.surface, (new_w, new_h))

            # Remplir avec noir (bandes noires)
            self.window.fill((0, 0, 0))
            pos_x = (window_w - new_w) // 2
            pos_y = (window_h - new_h) // 2
            self.window.blit(scaled_surface, (pos_x, pos_y))

        else:
            # Étirement direct (peut déformer si ratio différent)
            scaled_surface = pygame.transform.smoothscale(self.surface, (window_w, window_h))
            self.window.blit(scaled_surface, (0, 0))

        pygame.display.flip()
