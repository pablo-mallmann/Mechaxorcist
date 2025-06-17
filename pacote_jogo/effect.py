# Arquivo: effect.py
# Contém a classe genérica para gerenciar efeitos de animação (impactos, mortes, etc.).

import pygame
import os
from .settings import *

class Effect(pygame.sprite.Sprite):
    def __init__(self, center, effect_type, som_impacto=None):
        super().__init__()
        
        self.effect_type = effect_type
        self.anim_frames = []
        self.load_frames() # Carrega os frames corretos com base no tipo
        
        self.current_frame = 0
        self.image = self.anim_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.last_anim_update = pygame.time.get_ticks()
        
        # Toca o som de impacto, se houver um
        if som_impacto:
            som_impacto.play()

    def load_frames(self):
        """ Carrega os frames de animação com base no tipo de efeito. """
        if self.effect_type == 'player_hit':
            self.anim_cooldown = 50
            for i in range(1, 7):
                self._carregar_frame(f"assets/playerhit{i}.png")
        elif self.effect_type == 'demon_hit':
            self.anim_cooldown = 40
            for i in range(1, 13):
                self._carregar_frame(f"assets/demonhit{i}.png")
        elif self.effect_type == 'worm_death':
            self.anim_cooldown = 60
            for i in range(1, 9):
                self._carregar_frame(f"assets/wormdeath{i}.png")
                
    def _carregar_frame(self, caminho):
        """ Função auxiliar para carregar um único frame. """
        try:
            frame = pygame.image.load(caminho).convert_alpha()
            self.anim_frames.append(frame)
        except pygame.error:
            # Se um frame falhar, cria um substituto para não quebrar o jogo
            substituto = pygame.Surface((30, 30), pygame.SRCALPHA)
            self.anim_frames.append(substituto)
    
    def update(self):
        """ Anima o efeito e se autodestrói quando a animação termina. """
        agora = pygame.time.get_ticks()
        if agora - self.last_anim_update > self.anim_cooldown:
            self.last_anim_update = agora
            self.current_frame += 1
            if self.current_frame >= len(self.anim_frames):
                self.kill() # Remove o sprite
            else:
                center = self.rect.center
                self.image = self.anim_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
