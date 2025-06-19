# Arquivo: inimigo.py
# Contém a classe para os inimigos.

import pygame
import random
import os
from .settings import *

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, jogador):
        super().__init__()
        
        self.jogador = jogador
        self.is_alive = True
        
        # Listas para as diferentes animações
        self.walk_frames = []
        self.death_frames = []
        
        self.load_frames()
        self.current_frame = 0
        self.image = self.walk_frames[self.current_frame]
        self.rect = self.image.get_rect()

        self.last_anim_update = pygame.time.get_ticks()
        self.anim_cooldown = 120

        # Decide aleatoriamente o tipo de inimigo
        if random.random() > 0.8:
            self.tipo = 'perseguidor'
            self.velocidade = random.randrange(8, 10)
        else:
            self.tipo = 'normal'
            self.velocidade_x = random.randrange(-4, -1)

        self.rect.x = random.randrange(LARGURA_TELA, LARGURA_TELA + 200)
        self.rect.y = random.randrange(0, ALTURA_TELA // 2)

    def load_frames(self):
        """ Carrega os frames de animação de caminhada e morte. """
        # Carrega frames de caminhada (demon1-4)
        for i in range(1, 5):
            self._carregar_frame(f"assets/demon{i}.png", self.walk_frames)
        # Carrega frames de morte (demondeath1-4)
        for i in range(1, 5):
            self._carregar_frame(f"assets/demondeath{i}.png", self.death_frames)
            
    def _carregar_frame(self, caminho, lista_frames):
        """ Função auxiliar para carregar um único frame. """
        try:
            frame = pygame.image.load(caminho).convert_alpha()
            lista_frames.append(frame)
        except pygame.error:
            substituto = pygame.Surface((40, 30), pygame.SRCALPHA)
            substituto.fill(COR_VERMELHO)
            lista_frames.append(substituto)

    def hit(self):
        """ Inicia a sequência de morte se estiver vivo. """
        if self.is_alive:
            self.is_alive = False
            self.current_frame = 0 # Reinicia o contador de frames para a nova animação
            self.last_anim_update = pygame.time.get_ticks()

    def update(self):
        if self.is_alive:
            self.animate(self.walk_frames, loop=True)
            # Lógica de movimento
            if self.tipo == 'normal':
                self.rect.x += self.velocidade_x
            elif self.tipo == 'perseguidor':
                direcao = pygame.math.Vector2(self.jogador.rect.center) - pygame.math.Vector2(self.rect.center)
                if direcao.length_squared() > 0:
                    direcao.normalize_ip()
                self.rect.centerx += direcao.x * self.velocidade
                self.rect.centery += direcao.y * self.velocidade
            # Remove se sair da tela
            if self.rect.right < 0:
                self.kill()
        else: # Estado de morte
            self.animate(self.death_frames, loop=False)

    def animate(self, frame_list, loop):
        """ Gere a animação para uma lista de frames específica. """
        agora = pygame.time.get_ticks()
        if agora - self.last_anim_update > self.anim_cooldown:
            self.last_anim_update = agora
            self.current_frame += 1
            
            # Se a animação terminou
            if self.current_frame >= len(frame_list):
                if loop:
                    self.current_frame = 0 # Reinicia
                else:
                    self.kill() # Autodestrói-se
                    return
            
            center = self.rect.center
            self.image = frame_list[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
