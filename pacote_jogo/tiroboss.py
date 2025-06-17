# Arquivo: tiroboss.py
# Contém a classe para os tiros do chefe.

import pygame
import os
from .settings import *

class TiroBoss(pygame.sprite.Sprite):
    def __init__(self, pos_inicial, alvo):
        super().__init__()
        try:
            self.image = pygame.image.load(os.path.join("assets", "tiroboss.png")).convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((20, 10))
            self.image.fill((255, 100, 0)) # Laranja
        
        self.rect = self.image.get_rect(center=pos_inicial)
        
        # --- CORREÇÃO DO ERRO ---
        # Verifica se o 'alvo' é um sprite (como o jogador) ou já um vetor de direção
        if isinstance(alvo, pygame.sprite.Sprite):
            # Se for um sprite, calcula o vetor de direção para o centro dele
            direcao = pygame.math.Vector2(alvo.rect.center) - pygame.math.Vector2(pos_inicial)
        else:
            # Se não, assume que 'alvo' já é o vetor de direção
            direcao = alvo
            
        # Usa o vetor de direção calculado para definir a velocidade
        if direcao.length() > 0:
            self.vel = direcao.normalize() * 11 # Velocidade do tiro do chefe
        else:
            # Caso de segurança se o vetor for nulo
            self.vel = pygame.math.Vector2(-7, 0)

    def update(self):
        self.rect.move_ip(self.vel)
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()
