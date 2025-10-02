import pygame,os

class ScreenManager:
    def __init__(self, logical_size=(753, 1020)):
        self.logical_size = logical_size
        self.post_effects = {
            'fxaa': False,
            'sharpness': 0.0,
            'vignette': 0.0,  
            'color_boost': 1.0,
            'crt_curvature': 0.0,
            'scanlines': 0.0,
        }
        
        self.scaling_method = "nearest"
        
        self.window = pygame.display.set_mode(logical_size, pygame.RESIZABLE)
        
        # Surface logique
        self.surface = pygame.Surface(logical_size)
        
        # VARIABLES CRITIQUES POUR LES CONVERSIONS
        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.current_scaled_size = logical_size
        self.is_fullscreen = False

    def get_surface(self):
        return self.surface

    def high_quality_scale(self, surface, target_size):
        if self.scaling_method == "nearest":
            return pygame.transform.scale(surface, target_size)
        else:
            return pygame.transform.smoothscale(surface, target_size)

    def update(self):
        """Render final OPTIMISÉ pixel art - CORRIGÉ POUR LES CONVERSIONS"""
        window_w, window_h = self.window.get_size()
        logical_w, logical_h = self.logical_size

        scale = min(window_w / logical_w, window_h / logical_h)
        new_w, new_h = int(logical_w * scale), int(logical_h * scale)
            
        # METTRE À JOUR LES VARIABLES DE CONVERSION
        self.scale_factor = scale
        self.offset_x = (window_w - new_w) // 2
        self.offset_y = (window_h - new_h) // 2
        self.current_scaled_size = (new_w, new_h)
            
        scaled_surface = self.high_quality_scale(self.surface, (new_w, new_h))
        final_surface = self.apply_post_processing(scaled_surface)

        self.window.fill((0, 0, 0))
        self.window.blit(final_surface, (self.offset_x, self.offset_y))

        pygame.display.flip()

    def apply_post_processing(self, surface):
        return surface

    def get_scaled_rect(self, logical_rect):
        """Convertit un rectangle logique en rectangle écran"""
        screen_x = logical_rect.x * self.scale_factor + self.offset_x
        screen_y = logical_rect.y * self.scale_factor + self.offset_y
        screen_width = logical_rect.width * self.scale_factor
        screen_height = logical_rect.height * self.scale_factor
        
        return pygame.Rect(screen_x, screen_y, screen_width, screen_height)
    
    def toggle_fullscreen(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        if not self.is_fullscreen:
            # FULLSCREEN BORDERLESS
            self.window = pygame.display.set_mode(self.logical_size, pygame.RESIZABLE)
            self.window = pygame.display.set_mode(
                (0,0),
                pygame.NOFRAME
            )
            self.is_fullscreen = True
            print("Borderless fullscreen activé")
        else:
            # Revenir en mode fenêtré centré
            self.window = pygame.display.set_mode(self.logical_size, pygame.RESIZABLE)
            self.is_fullscreen = False
            print("Retour en mode fenêtré centré")

        # recalcul scale / offsets
        window_w, window_h = self.window.get_size()
        logical_w, logical_h = self.logical_size
        scale = min(window_w / logical_w, window_h / logical_h)
        new_w, new_h = int(logical_w * scale), int(logical_h * scale)
        self.scale_factor = scale
        self.offset_x = (window_w - new_w) // 2
        self.offset_y = (window_h - new_h) // 2
        self.current_scaled_size = (new_w, new_h)

        pygame.display.flip()


        
    def screen_to_logical(self, screen_pos):
        """Convertit une position écran (event.pos) -> position logique (surface)."""
        window_w, window_h = self.window.get_size()
        logical_w, logical_h = self.logical_size

        # scale et offsets recalculés à la volée (identique à update())
        scale = min(window_w / logical_w, window_h / logical_h)
        new_w, new_h = int(logical_w * scale), int(logical_h * scale)
        offset_x = (window_w - new_w) // 2
        offset_y = (window_h - new_h) // 2

        sx, sy = screen_pos
        # convertir en coords logiques (float -> int)
        lx = (sx - offset_x) / scale
        ly = (sy - offset_y) / scale
        return int(lx), int(ly)