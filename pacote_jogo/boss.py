# Arquivo: boss.py
# Contém a classe para o chefe final.

import pygame
import random
import os
from .settings import *
from .tiroboss import TiroBoss

class Boss(pygame.sprite.Sprite):
    def __init__(self, all_sprites, grupo_tiros_boss, jogador):
        super().__init__()
        self.todos_sprites = all_sprites
        self.grupo_tiros_boss = grupo_tiros_boss
        self.jogador = jogador

        self.anim_frames = []
        self.load_frames()
        self.current_frame = 0
        self.image = self.anim_frames[self.current_frame]
        self.rect = self.image.get_rect()

        self.last_anim_update = pygame.time.get_ticks()
        self.anim_cooldown = 100

        self.rect.left = LARGURA_TELA
        self.rect.centery = ALTURA_TELA / 3
        self.velocidade_x = -2
        self.posicao_alvo_x = LARGURA_TELA - self.rect.width - 50

        self.chegou_posicao = False
        self.vida = 30
        self.ultimo_tiro = pygame.time.get_ticks()
        self.cooldown_tiro = 1500 # Dispara a cada 1.5 segundos

    def load_frames(self):
        for i in range(1, 10):
            caminho = os.path.join("assets", f"boss{i}.png")
            try:
                frame = pygame.image.load(caminho).convert_alpha()
                self.anim_frames.append(frame)
            except pygame.error:
                substituto = pygame.Surface((150, 150), pygame.SRCALPHA)
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

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.cooldown_tiro:
            self.ultimo_tiro = agora
            tiro = TiroBoss(self.rect.midleft, self.jogador)
            self.todos_sprites.add(tiro)
            self.grupo_tiros_boss.add(tiro)

    def update(self):
        self.animate()
        if not self.chegou_posicao:
            self.rect.x += self.velocidade_x
            if self.rect.left <= self.posicao_alvo_x:
                self.rect.left = self.posicao_alvo_x
                self.chegou_posicao = True
        else:
            self.atirar()

    def hit(self):
        self.vida -= 1
        if self.vida <= 0:
            self.kill() # Chefe morre
