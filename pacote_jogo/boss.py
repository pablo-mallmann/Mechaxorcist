# Arquivo: boss.py
# Contém a classe para o chefe final.

import pygame
import random
import os
from .settings import *
from .tiroboss import TiroBoss

class Boss(pygame.sprite.Sprite):
    def __init__(self, all_sprites, grupo_tiros_boss, jogador, velocidade_projetil, fire_cooldown, max_vida):
        super().__init__()
        self.todos_sprites = all_sprites
        self.grupo_tiros_boss = grupo_tiros_boss
        self.jogador = jogador
        self.velocidade_projetil = velocidade_projetil
        self.cooldown_tiro = fire_cooldown

        self.anim_frames = []
        self.death_frames = []
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
        self.is_alive = True
        self.max_vida = max_vida # Vida máxima para este nível
        self.vida = self.max_vida # Vida atual começa no máximo
        self.ultimo_tiro = pygame.time.get_ticks()

    def hit(self, damage_modifier):
        if self.is_alive:
            self.vida -= 1 * damage_modifier
            if self.vida <= 0:
                self.is_alive = False
                self.current_frame = 0
                self.last_anim_update = pygame.time.get_ticks()
    
    # O resto dos métodos permanece igual
    def load_frames(self):
        for i in range(1, 7):
            self._carregar_frame(f"assets/boss{i}.png", self.anim_frames)
        for i in range(1, 8):
            self._carregar_frame(f"assets/bossmorte{i}.png", self.death_frames)
    def _carregar_frame(self, caminho, lista_frames):
        try:
            frame = pygame.image.load(os.path.join(caminho)).convert_alpha()
            lista_frames.append(frame)
        except pygame.error:
            substituto = pygame.Surface((150, 150), pygame.SRCALPHA)
            substituto.fill(COR_VERMELHO)
            lista_frames.append(substituto)
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
    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.cooldown_tiro:
            self.ultimo_tiro = agora
            num_projeteis = random.randint(3, 5)
            angulo_spread = 15
            direcao_base = pygame.math.Vector2(self.jogador.rect.center) - pygame.math.Vector2(self.rect.midleft)
            angulo_inicial = -((num_projeteis - 1) * angulo_spread) / 2
            for i in range(num_projeteis):
                angulo_atual = angulo_inicial + i * angulo_spread
                direcao_projetil = direcao_base.rotate(angulo_atual)
                tiro = TiroBoss(self.rect.midleft, direcao_projetil, self.velocidade_projetil)
                self.todos_sprites.add(tiro)
                self.grupo_tiros_boss.add(tiro)
    def update(self):
        if self.is_alive:
            self.animate(self.anim_frames, loop=True)
            if not self.chegou_posicao:
                self.rect.x += self.velocidade_x
                if self.rect.left <= self.posicao_alvo_x:
                    self.rect.left = self.posicao_alvo_x
                    self.chegou_posicao = True
            else:
                self.atirar()
        else:
            self.animate(self.death_frames, loop=False)
