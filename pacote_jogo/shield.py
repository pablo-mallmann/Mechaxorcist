# Arquivo: shield.py
# Contém a classe para o escudo protetor do jogador.

import pygame
import os
from .settings import *

class Shield(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        
        # --- Configuração da Animação ---
        self.anim_frames = []
        self.load_frames()
        self.current_frame = 0
        self.image = self.anim_frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Temporizadores
        self.last_anim_update = pygame.time.get_ticks()
        self.anim_cooldown = 100
        self.spawn_time = pygame.time.get_ticks()

    def load_frames(self):
        """ Carrega os frames da animação do escudo. """
        for i in range(1, 3):
            caminho = os.path.join("assets", f"escudo{i}.png")
            try:
                frame = pygame.image.load(caminho).convert_alpha()
                self.anim_frames.append(frame)
            except pygame.error:
                substituto = pygame.Surface((80, 80), pygame.SRCALPHA)
                pygame.draw.circle(substituto, (0, 100, 255, 100), (40, 40), 40)
                self.anim_frames.append(substituto)
    
    def update(self):
        """ Anima o escudo, segue o jogador e verifica a sua duração. """
        self.animate()
        self.rect.center = self.player.rect.center
        
        # Verifica se a duração do escudo terminou
        if pygame.time.get_ticks() - self.spawn_time > SHIELD_DURATION:
            self.kill()

    def animate(self):
        """ Alterna entre os frames para criar a animação. """
        agora = pygame.time.get_ticks()
        if agora - self.last_anim_update > self.anim_cooldown:
            self.last_anim_update = agora
            self.current_frame = (self.current_frame + 1) % len(self.anim_frames)
            
            center = self.rect.center
            self.image = self.anim_frames[self.current_frame]
            self.rect = self.image.get_rect(center=center)
