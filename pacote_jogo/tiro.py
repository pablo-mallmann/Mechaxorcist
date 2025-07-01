# Arquivo: tiro.py
# Contém a classe para os tiros do jogador.

import pygame
import os
from .settings import *

class Tiro(pygame.sprite.Sprite):
    def __init__(self, pos_inicial, alvo, velocidade, penetration):
        super().__init__()
        try:
            self.image = pygame.image.load(os.path.join("assets", "tiro1.png")).convert_alpha()
        except pygame.error:
            self.image = pygame.Surface([8, 8])
            self.image.fill(COR_BRANCO)
        
        self.rect = self.image.get_rect()
        self.penetration = penetration # Quantos inimigos pode atravessar
        self.pos = pygame.math.Vector2(pos_inicial)
        self.rect.center = self.pos
        
        if isinstance(alvo, pygame.math.Vector2):
            direcao = alvo
        else: # alvo é a posição do mouse
            direcao = pygame.math.Vector2(alvo) - self.pos

        if direcao.length() > 0:
            self.vel = direcao.normalize() * velocidade
        else:
            self.vel = pygame.math.Vector2(0, -velocidade)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()

    def hit(self):
        """ Chamado quando o tiro atinge um inimigo. """
        self.penetration -= 1
        if self.penetration <= 0:
            self.kill()
