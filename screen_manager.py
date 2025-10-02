import pygame

class ScreenManager:
    def __init__(self, logical_size=(753, 1020), keep_ratio=True):
        self.logical_size = logical_size
        self.keep_ratio = keep_ratio
        
        # Pour le pixel art, on désactive la plupart des effets
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
        pygame.display.set_caption("Pokemon Clone - Pixel Perfect")
        
        # Surface logique
        self.surface = pygame.Surface(logical_size)
        
        # VARIABLES CRITIQUES POUR LES CONVERSIONS
        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.current_scaled_size = logical_size  # Taille actuelle scaled

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

        if self.keep_ratio:
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

        else:
            # Mode étirement
            self.scale_factor = window_w / logical_w
            self.offset_x = 0
            self.offset_y = 0
            self.current_scaled_size = (window_w, window_h)
            
            scaled_surface = self.high_quality_scale(self.surface, (window_w, window_h))
            final_surface = self.apply_post_processing(scaled_surface)
            self.window.blit(final_surface, (0, 0))

        pygame.display.flip()

    def apply_post_processing(self, surface):
        """Post-processing MINIMAL pour pixel art"""
        return surface  # Pour l'instant, pas d'effets

    # MÉTHODE POUR LA DÉTECTION DE COLLISION
    def get_scaled_rect(self, logical_rect):
        """Convertit un rectangle logique en rectangle écran"""
        screen_x = logical_rect.x * self.scale_factor + self.offset_x
        screen_y = logical_rect.y * self.scale_factor + self.offset_y
        screen_width = logical_rect.width * self.scale_factor
        screen_height = logical_rect.height * self.scale_factor
        
        return pygame.Rect(screen_x, screen_y, screen_width, screen_height)