import pygame

class Button():
	def __init__(self, x, y, image, scale, text='', text_color=(0, 0, 0)):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
  
  		# Texte du bouton
		self.text = text
		self.font = pygame.font.SysFont(None, 50)  # Taille par défaut
		self.text_color = text_color
		self.text_surface = self.font.render(text, True, text_color)
		self.text_rect = self.text_surface.get_rect(center=self.rect.center)
  
	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))
  
		# Redessine le texte (car centré sur le rect original)
		self.text_rect = self.text_surface.get_rect(center=self.rect.center)
		surface.blit(self.text_surface, self.text_rect)
		return action