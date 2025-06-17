# Arquivo: inimigo.py
# Contém a classe para os inimigos.

import pygame
import random
from .settings import *

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, jogador):
        super().__init__()
        
        self.jogador = jogador
        self.is_alive = True # Adicionado para consistência
        self.anim_frames = []
        self.load_frames()
        self.current_frame = 0
        self.image = self.anim_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.last_anim_update = pygame.time.get_ticks()
        self.anim_cooldown = 120

        if random.random() > 0.8:
            self.tipo = 'perseguidor'
            self.velocidade = random.randrange(8, 10)
            
        else:
            self.tipo = 'normal'
            self.velocidade_x = random.randrange(-4, -1)

        self.rect.x = random.randrange(LARGURA_TELA, LARGURA_TELA + 200)
        self.rect.y = random.randrange(0, ALTURA_TELA // 2)

    def load_frames(self):
        for i in range(1, 5):
            try:
                frame = pygame.image.load(f"assets/demon{i}.png").convert_alpha()
                self.anim_frames.append(frame)
            except pygame.error as e:
                print(f"Erro ao carregar a imagem assets/demon{i}.png: {e}")
                substituto = pygame.Surface([40, 30])
                substituto.fill(COR_VERMELHO)
                self.anim_frames.append(substituto)

    def animate(self):
        agora = pygame.time.get_ticks()
        if agora - self.last_anim_update > self.anim_cooldown:
            self.last_anim_update = agora
            self.current_frame = (self.current_frame + 1) % len(self.anim_frames)
            center = self.rect.center
            self.image = self.anim_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = center

    def update(self):
        self.animate()
        
        if self.tipo == 'normal':
            self.rect.x += self.velocidade_x
        elif self.tipo == 'perseguidor':
            direcao = pygame.math.Vector2(self.jogador.rect.center) - pygame.math.Vector2(self.rect.center)
            if direcao.length_squared() > 0:
                direcao.normalize_ip()
            self.rect.centerx += direcao.x * self.velocidade
            self.rect.centery += direcao.y * self.velocidade

        if self.rect.right < 0:
            self.kill()
