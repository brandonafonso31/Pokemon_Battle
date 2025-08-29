import pygame,os
from config import WHITE,font_path

class Button:
    def __init__(self, x, y, image, scale, text='', text_color=WHITE, padding=10,font_size = 50):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
  
        self.text = text
        self.text_color = text_color

        self.font_path = font_path
        self.font_size = font_size
        self.font = pygame.font.Font(self.font_path, font_size)
        
        self.padding = padding
        self.text_surface, self.text_rect = self.render_text_to_fit()
  
    def render_text_to_fit(self):
        max_width = self.rect.width - 2 * self.padding
        max_height = self.rect.height - 2 * self.padding
        adjust_x = 2.5
        font_size = self.font_size

        while font_size > 20:
            font = pygame.font.Font(self.font_path, font_size)
            text_surface = font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect()
            if text_rect.width <= max_width and text_rect.height <= max_height:
                text_rect.center = (self.rect.center[0] - adjust_x, self.rect.center[1])
                self.font = font
                return text_surface, text_rect
            font_size -= 1

        # Fallback : texte trop long
        font = pygame.font.Font(self.font_path, 10)
        self.font = font
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.rect.center[0] - adjust_x, self.rect.center[1]))
        return text_surface, text_rect

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(self.text_surface, self.text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return event.button == 1 and self.rect.collidepoint(event.pos)
        return False
