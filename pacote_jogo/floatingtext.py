# Arquivo: floatingtext.py
# Contém a classe para os números de dano flutuantes.

import pygame
from .settings import *

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font, color):
        super().__init__()
        self.font = font
        self.image = self.font.render(str(text), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.spawn_time = pygame.time.get_ticks()
        self.speed_y = -1
        self.duration = 600 # O texto dura 600ms

    def update(self):
        # Move o texto para cima
        self.rect.y += self.speed_y
        # Remove o texto após a sua duração
        if pygame.time.get_ticks() - self.spawn_time > self.duration:
            self.kill()
