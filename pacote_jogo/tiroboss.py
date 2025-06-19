# Arquivo: tiroboss.py
# Contém a classe para os tiros do chefe.

import pygame
import os
from .settings import *

class TiroBoss(pygame.sprite.Sprite):
    def __init__(self, pos_inicial, direcao, velocidade):
        super().__init__()
        try:
            self.image = pygame.image.load(os.path.join("assets", "tiroboss.png")).convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((20, 10))
            self.image.fill((255, 100, 0)) # Laranja
        
        self.rect = self.image.get_rect(center=pos_inicial)
        
        # Usa o vetor de direção e a velocidade recebida
        if direcao.length() > 0:
            self.vel = direcao.normalize() * velocidade
        else:
            self.vel = pygame.math.Vector2(-velocidade, 0)

    def update(self):
        self.rect.move_ip(self.vel)
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()
