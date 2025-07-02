# Arquivo: inimigo.py
# Contém a classe para os inimigos.

import pygame
import random
import os
from .settings import *

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, jogador, speed_multiplier=1.0):
        super().__init__()
        
        self.jogador = jogador
        self.is_alive = True
        self.vida = INIMIGO_HEALTH_BASE # Vida do inimigo
        
        self.walk_frames = []
        self.death_frames = []
        
        self.load_frames()
        self.current_frame = 0
        self.image = self.walk_frames[self.current_frame]
        self.rect = self.image.get_rect()

        self.last_anim_update = pygame.time.get_ticks()
        self.anim_cooldown = 120

        if random.random() > 0.8:
            self.tipo = 'perseguidor'
            self.velocidade = random.randrange(1, 3) * speed_multiplier
        else:
            self.tipo = 'normal'
            self.velocidade_x = random.randrange(-4, -1) * speed_multiplier

        self.rect.x = random.randrange(LARGURA_TELA, LARGURA_TELA + 200)
        self.rect.y = random.randrange(0, ALTURA_TELA // 2)

    def load_frames(self):
        for i in range(1, 5):
            self._carregar_frame(f"assets/demon{i}.png", self.walk_frames)
        for i in range(1, 5):
            self._carregar_frame(f"assets/demondeath{i}.png", self.death_frames)
            
    def _carregar_frame(self, caminho, lista_frames):
        try:
            frame = pygame.image.load(os.path.join(caminho)).convert_alpha()
            lista_frames.append(frame)
        except pygame.error:
            substituto = pygame.Surface((40, 30), pygame.SRCALPHA)
            substituto.fill(COR_VERMELHO)
            lista_frames.append(substituto)

    def hit(self, damage):
        if self.is_alive:
            self.vida -= damage
            if self.vida <= 0:
                self.is_alive = False
                self.current_frame = 0
                self.last_anim_update = pygame.time.get_ticks()

    def update(self):
        if self.is_alive:
            self.animate(self.walk_frames, loop=True)
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
        else:
            self.animate(self.death_frames, loop=False)

    def animate(self, frame_list, loop):
        agora = pygame.time.get_ticks()
        if agora - self.last_anim_update > self.anim_cooldown:
            self.last_anim_update = agora
            self.current_frame += 1
            if self.current_frame >= len(frame_list):
                if loop:
                    self.current_frame = 0
                else:
                    self.kill()
                    return
            center = self.rect.center
            self.image = frame_list[self.current_frame]
            self.rect = self.image.get_rect(center=center)
