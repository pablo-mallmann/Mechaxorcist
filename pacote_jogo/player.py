# Arquivo: player.py
# Contém a classe para a nave do jogador.

import pygame
from .settings import *
from .tiro import Tiro

class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, bullets, som_tiro):
        super().__init__()
        self.todos_sprites = all_sprites
        self.grupo_tiros = bullets
        self.som_tiro = som_tiro # Armazena o som do tiro
        
        # --- Configuração da Animação ---
        self.anim_frames = []
        self.load_frames()
        self.current_frame = 0
        self.image = self.anim_frames[self.current_frame]
        self.rect = self.image.get_rect()
        
        self.last_anim_update = pygame.time.get_ticks()
        self.anim_cooldown = 100

        # --- Posição e Física ---
        self.rect.centerx = LARGURA_TELA / 2
        self.rect.bottom = ALTURA_CHAO
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

        self.ultimo_tiro = pygame.time.get_ticks()

    def load_frames(self):
        """ Carrega os 6 frames da animação do robô. """
        for i in range(1, 7):
            frame = pygame.image.load(f"assets/robo{i}.png").convert_alpha()
            self.anim_frames.append(frame)

    def animate(self):
        """ Alterna entre os frames para criar a animação. """
        agora = pygame.time.get_ticks()
        if agora - self.last_anim_update > self.anim_cooldown:
            self.last_anim_update = agora
            self.current_frame = (self.current_frame + 1) % len(self.anim_frames)
            
            bottom = self.rect.bottom
            self.image = self.anim_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def saltar(self):
        if self.rect.bottom >= ALTURA_CHAO:
            self.vel.y = FORCA_SALTO

    def update(self):
        self.animate()
        
        self.acc = pygame.math.Vector2(0, GRAVIDADE)
        
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.acc.x = -0.8
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.acc.x = 0.8

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        if self.pos.x > LARGURA_TELA - self.rect.width / 2:
            self.pos.x = LARGURA_TELA - self.rect.width / 2
        if self.pos.x < self.rect.width / 2:
            self.pos.x = self.rect.width / 2
        if self.pos.y >= ALTURA_CHAO:
            self.pos.y = ALTURA_CHAO
            self.vel.y = 0

        self.rect.midbottom = self.pos
        
        self.atirar_automatico()
            
    def atirar_automatico(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > COOLDOWN_TIRO:
            self.ultimo_tiro = agora
            pos_mouse = pygame.mouse.get_pos()
            tiro = Tiro(self.rect.center, pos_mouse)
            self.todos_sprites.add(tiro)
            self.grupo_tiros.add(tiro)
            # Toca o som do tiro, se ele foi carregado corretamente
            if self.som_tiro:
                self.som_tiro.play()
