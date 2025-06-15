# Arquivo: tiro.py
# Contém a classe para os tiros do jogador, agora com vetores e sprite.

import pygame
from .settings import *

class Tiro(pygame.sprite.Sprite):
    def __init__(self, pos_inicial, pos_alvo):
        super().__init__()
        
        # --- Carrega a imagem do tiro ---
        try:
            # Carrega a imagem da pasta assets e a converte para um formato mais rápido
            self.image = pygame.image.load("assets/tiro1.png").convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar a imagem assets/tiro1.png: {e}")
            # Se a imagem não for encontrada, cria um substituto simples para o jogo não quebrar
            self.image = pygame.Surface([8, 8])
            self.image.fill(COR_BRANCO)

        self.rect = self.image.get_rect()
        
        # --- Posição e Física (usando vetores) ---
        self.pos = pygame.math.Vector2(pos_inicial)
        self.rect.center = self.pos
        
        # Calcula o vetor de direção normalizado
        direcao = pygame.math.Vector2(pos_alvo) - self.pos
        if direcao.length() == 0:
            direcao = pygame.math.Vector2(0, -1) # Evita divisão por zero se o mouse estiver no jogador
        self.vel = direcao.normalize() * VELOCIDADE_TIRO

    def update(self):
        # Move o tiro de acordo com seu vetor de velocidade
        self.pos += self.vel
        self.rect.center = self.pos
        
        # Remove o tiro se ele sair completamente da tela para economizar memória
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()
