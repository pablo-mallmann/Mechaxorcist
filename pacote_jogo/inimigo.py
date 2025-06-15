# Arquivo: inimigo.py
# Contém a classe para os inimigos.

import pygame
import random
from .settings import *

class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # --- Configuração da Animação ---
        self.anim_frames = []
        self.load_frames() # Carrega os sprites do demônio
        self.current_frame = 0
        self.image = self.anim_frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Temporizador para controlar a velocidade da animação
        self.last_anim_update = pygame.time.get_ticks()
        self.anim_cooldown = 120 # Tempo em ms entre cada frame

        # --- Posição e Física ---
        # Posição de surgimento: na direita (fora da tela) e na metade superior
        self.rect.x = random.randrange(LARGURA_TELA, LARGURA_TELA + 200)
        self.rect.y = random.randrange(0, ALTURA_TELA // 2)
        
        # Velocidade horizontal (aleatória para variedade)
        self.velocidade_x = random.randrange(-4, -1)

    def load_frames(self):
        """ Carrega os 4 frames da animação do demônio. """
        for i in range(1, 5):
            try:
                # Carrega a imagem da pasta assets
                frame = pygame.image.load(f"assets/demon{i}.png").convert_alpha()
                # Você pode redimensionar se precisar com pygame.transform.scale()
                self.anim_frames.append(frame)
            except pygame.error as e:
                print(f"Erro ao carregar a imagem assets/demon{i}.png: {e}")
                # Cria um substituto se a imagem não for encontrada
                substituto = pygame.Surface([40, 30])
                substituto.fill(COR_VERMELHO)
                self.anim_frames.append(substituto)


    def animate(self):
        """ Alterna entre os frames para criar a animação. """
        agora = pygame.time.get_ticks()
        if agora - self.last_anim_update > self.anim_cooldown:
            self.last_anim_update = agora
            self.current_frame = (self.current_frame + 1) % len(self.anim_frames)
            
            # Atualiza a imagem, mas mantém o centro do retângulo para não "pular"
            center = self.rect.center
            self.image = self.anim_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = center

    def update(self):
        # Atualiza a animação a cada quadro
        self.animate()
        
        # Move o inimigo para a esquerda
        self.rect.x += self.velocidade_x
        # Remove o inimigo se ele sair da tela pela esquerda
        if self.rect.right < 0:
            self.kill()
