# Arquivo: worm.py
# Contém a classe para o inimigo terrestre 'worm'.

import pygame
import random
import os
from .settings import *

class Worm(pygame.sprite.Sprite):
    def __init__(self, speed_multiplier=1.0):
        super().__init__()

        self.is_alive = True
        self.vida = WORM_HEALTH_BASE # Vida do worm
        self.walk_frames = []
        self.death_frames = []
        self.load_frames()
        
        self.current_frame = 0
        self.image = self.walk_frames[self.current_frame]
        self.rect = self.image.get_rect()

        self.last_anim_update = pygame.time.get_ticks()
        self.anim_cooldown = 80

        self.rect.bottom = ALTURA_CHAO
        self.rect.left = random.randrange(LARGURA_TELA, LARGURA_TELA + 400)
        self.velocidade_x = random.randrange(-5, -2) * speed_multiplier

    def load_frames(self):
        for i in range(1, 10):
            self._carregar_frame(f"assets/worm{i}.png", self.walk_frames)
        for i in range(1, 9):
            self._carregar_frame(f"assets/wormdeath{i}.png", self.death_frames)

    def _carregar_frame(self, caminho, lista_frames):
        try:
            frame = pygame.image.load(os.path.join(caminho)).convert_alpha()
            lista_frames.append(frame)
        except pygame.error:
            substituto = pygame.Surface((50, 20), pygame.SRCALPHA)
            substituto.fill((255, 100, 100))
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
            self.rect.x += self.velocidade_x
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
            bottomleft = self.rect.bottomleft
            self.image = frame_list[self.current_frame]
            self.rect = self.image.get_rect(bottomleft=bottomleft)
