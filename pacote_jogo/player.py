# Arquivo: player.py
# Contém a classe para a nave do jogador.

import pygame
from .settings import *
from .tiro import Tiro
from .shield import Shield

class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, bullets, som_tiro):
        super().__init__()
        self.todos_sprites = all_sprites
        self.grupo_tiros = bullets
        self.som_tiro = som_tiro
        
        # Atributos de Power-up
        self.damage = PLAYER_DAMAGE_BASE
        self.crit_chance = CRIT_CHANCE_BASE
        self.vamp_chance = VAMP_CHANCE_BASE # Novo atributo
        self.max_municao = MUNICAO_MAXIMA_BASE
        self.tempo_recarga = TEMPO_RECARGA_BASE
        self.velocidade_tiro = VELOCIDADE_TIRO_BASE
        self.tiro_penetration = TIRO_PENETRATION_BASE
        self.projectile_count = PLAYER_PROJECTILE_COUNT_BASE
        self.dano_boss_modifier = 1.0
        self.has_shield_chance = False

        # Atributos normais
        self.municao = self.max_municao
        self.vidas = VIDAS_JOGADOR
        self.recarregando = False
        self.tempo_inicio_recarga = 0
        self.shield_sprite = None

        # Animação e Física (código omitido por brevidade, permanece igual)
        self.anim_frames = []
        self.load_frames()
        self.current_frame = 0
        self.image = self.anim_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.last_anim_update = pygame.time.get_ticks()
        self.anim_cooldown = 100
        self.rect.centerx = LARGURA_TELA / 2
        self.rect.bottom = ALTURA_CHAO
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

    def aplicar_power_up(self, power_up_id):
        if power_up_id == 'aumento_municao':
            self.max_municao += 2
            self.municao += 2
        elif power_up_id == 'aumento_recarga':
            self.tempo_recarga = max(500, self.tempo_recarga - 50)
        elif power_up_id == 'aumento_velocidade_projetil':
            self.velocidade_tiro += 0.5
        elif power_up_id == 'aumento_dano_boss':
            self.dano_boss_modifier += 0.01
        elif power_up_id == 'aumento_penetracao':
            self.tiro_penetration += 1
        elif power_up_id == 'aumento_projeteis':
            self.projectile_count += 1
        elif power_up_id == 'aumento_dano_tiro':
            self.damage += 0.5
        elif power_up_id == 'aumento_crit_chance':
            self.crit_chance += 0.05
        elif power_up_id == 'chance_escudo':
            self.has_shield_chance = True
        elif power_up_id == 'vampirismo':
            self.vamp_chance += 0.05 # Aumenta a chance em 5%

    def activate_shield(self):
        if not self.shield_sprite or not self.shield_sprite.alive():
            self.shield_sprite = Shield(self)
            self.todos_sprites.add(self.shield_sprite)

    def atirar(self):
        if self.municao > 0 and not self.recarregando:
            self.municao -= 1
            pos_mouse = pygame.mouse.get_pos()
            
            if self.projectile_count == 1:
                tiro = Tiro(self.rect.center, pos_mouse, self.velocidade_tiro, self.tiro_penetration, self.damage)
                self.todos_sprites.add(tiro)
                self.grupo_tiros.add(tiro)
            else:
                angulo_spread = 10
                direcao_base = pygame.math.Vector2(pos_mouse) - pygame.math.Vector2(self.rect.center)
                angulo_inicial = -((self.projectile_count - 1) * angulo_spread) / 2
                for i in range(self.projectile_count):
                    angulo_atual = angulo_inicial + i * angulo_spread
                    direcao_projetil = direcao_base.rotate(angulo_atual)
                    tiro = Tiro(self.rect.center, direcao_projetil, self.velocidade_tiro, self.tiro_penetration, self.damage)
                    self.todos_sprites.add(tiro)
                    self.grupo_tiros.add(tiro)

            if self.som_tiro:
                self.som_tiro.play()
            
            if self.municao == 0:
                self.recarregando = True
                self.tempo_inicio_recarga = pygame.time.get_ticks()
    
    # O resto dos métodos permanece igual
    def checar_recarga(self):
        if self.recarregando:
            agora = pygame.time.get_ticks()
            if agora - self.tempo_inicio_recarga > self.tempo_recarga:
                self.municao = self.max_municao
                self.recarregando = False
    def load_frames(self):
        for i in range(1, 7):
            frame = pygame.image.load(f"assets/robo{i}.png").convert_alpha()
            self.anim_frames.append(frame)
    def animate(self):
        agora = pygame.time.get_ticks()
        if agora - self.last_anim_update > self.anim_cooldown:
            self.last_anim_update = agora
            self.current_frame = (self.current_frame + 1) % len(self.anim_frames)
            bottom = self.rect.bottom
            self.image = self.anim_frames[self.current_frame]
            self.rect = self.image.get_rect(bottom=bottom)
    def saltar(self):
        if self.rect.bottom >= ALTURA_CHAO:
            self.vel.y = FORCA_SALTO
    def update(self):
        self.animate()
        self.checar_recarga()
        self.acc = pygame.math.Vector2(0, GRAVIDADE)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.acc.x = -0.5
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.acc.x = 0.5
        self.acc.x += self.vel.x * FRICCAO_JOGADOR
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > LARGURA_TELA - self.rect.width / 2:
            self.pos.x = LARGURA_TELA - self.rect.width / 2
        if self.pos.x < self.rect.width / 2:
            self.pos.x = self.rect.width / 2
        if self.pos.y >= ALTURA_CHAO:
            self.pos.y = ALTURA_CHAO
            self.vel.y = 0
        self.rect.midbottom = self.pos
