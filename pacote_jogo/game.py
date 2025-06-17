# Arquivo: game.py
# Contém a classe principal do jogo.

import pygame
import sys
import random

from .settings import *
from .background import Background
from .player import Player
from .inimigo import Inimigo
from .worm import Worm
from .crosshair import Crosshair
from .effect import Effect
from .boss import Boss
from .tiroboss import TiroBoss

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Mechaxorcist")
        self.clock = pygame.time.Clock()
        self.rodando = True
        self.fundo = Background(self.tela)
        
        pygame.mouse.set_visible(False)
        self.carregar_dados()

        self.frequencia_spawn_inimigo = 1200
        self.ultimo_spawn_inimigo = pygame.time.get_ticks()
        self.frequencia_spawn_worm = 3000
        self.ultimo_spawn_worm = pygame.time.get_ticks()

    def carregar_dados(self):
        self.fonte = pygame.font.SysFont(NOME_FONTE, TAMANHO_FONTE)
        try:
            self.som_tiro = pygame.mixer.Sound("assets/som_tiro.flac")
            self.som_tiro.set_volume(0.5)
        except pygame.error as e:
            print(f"Erro ao carregar o som assets/som_tiro.flac: {e}")
            self.som_tiro = None
        
        try:
            self.som_impacto = pygame.mixer.Sound("assets/playerhitsom.wav")
            self.som_impacto.set_volume(0.6)
        except pygame.error as e:
            print(f"Erro ao carregar o som assets/playerhitsom.wav: {e}")
            self.som_impacto = None
            
        try:
            pygame.mixer.music.load("assets/musica1.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(loops=-1)
        except pygame.error as e:
            print(f"Erro ao carregar a música assets/musica1.mp3: {e}")

    def novo_jogo(self):
        self.todos_sprites = pygame.sprite.Group()
        self.grupo_inimigos = pygame.sprite.Group()
        self.grupo_tiros = pygame.sprite.Group()
        self.grupo_tiros_boss = pygame.sprite.Group()
        self.grupo_boss = pygame.sprite.GroupSingle()

        self.jogador = Player(self.todos_sprites, self.grupo_tiros, self.som_tiro)
        self.todos_sprites.add(self.jogador)
        
        self.grupo_mira = pygame.sprite.GroupSingle()
        self.mira = Crosshair()
        self.grupo_mira.add(self.mira)
        
        self.abates = 0
        self.boss_spawned = False
        self.run()

    def run(self):
        self.jogando = True
        while self.jogando:
            self.clock.tick(FPS)
            self.eventos()
            self.atualizar_logica()
            self.desenhar()

    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.jogando = False
                self.rodando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.jogador.saltar()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.jogador.atirar()

    def atualizar_logica(self):
        self.fundo.update()
        self.todos_sprites.update()
        self.grupo_mira.update()

        # Verifica se o chefe deve ser invocado
        if not self.boss_spawned and self.abates >= INIMIGOS_PARA_BOSS:
            self.boss_spawned = True
            boss = Boss(self.todos_sprites, self.grupo_tiros_boss, self.jogador)
            self.todos_sprites.add(boss)
            self.grupo_boss.add(boss)

        # Para o spawn de inimigos normais se o chefe estiver em cena
        if not self.boss_spawned:
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_spawn_inimigo > self.frequencia_spawn_inimigo:
                self.ultimo_spawn_inimigo = agora
                inimigo_voador = Inimigo(self.jogador)
                self.todos_sprites.add(inimigo_voador)
                self.grupo_inimigos.add(inimigo_voador)

            if agora - self.ultimo_spawn_worm > self.frequencia_spawn_worm:
                self.ultimo_spawn_worm = agora
                worm = Worm()
                self.todos_sprites.add(worm)
                self.grupo_inimigos.add(worm)

        # Colisões
        self.checar_colisoes()
        
        if self.jogador.vidas <= 0:
            self.jogando = False

    def checar_colisoes(self):
        # Colisão de tiros do jogador com inimigos
        colisoes_tiro_inimigo = pygame.sprite.groupcollide(self.grupo_tiros, self.grupo_inimigos, True, False)
        for inimigos_atingidos in colisoes_tiro_inimigo.values():
            for inimigo in inimigos_atingidos:
                if isinstance(inimigo, Worm):
                    if inimigo.is_alive:
                        self.abates += 1
                        self.todos_sprites.add(Effect(inimigo.rect.center, 'player_hit', self.som_impacto))
                        inimigo.hit()
                else:
                    if inimigo.is_alive:
                        self.abates += 1
                        inimigo.is_alive = False
                        self.todos_sprites.add(Effect(inimigo.rect.center, 'player_hit', self.som_impacto))
                        inimigo.kill()
        
        # Colisão de tiros do jogador com o chefe
        if self.boss_spawned:
            colisoes_tiro_boss = pygame.sprite.groupcollide(self.grupo_tiros, self.grupo_boss, True, False)
            for boss_atingido in colisoes_tiro_boss.values():
                boss_atingido[0].hit()
                self.todos_sprites.add(Effect(boss_atingido[0].rect.center, 'player_hit', self.som_impacto))

        # Colisão do jogador com inimigos
        inimigos_colididos = pygame.sprite.spritecollide(self.jogador, self.grupo_inimigos, True)
        if inimigos_colididos:
            self.jogador.vidas -= len(inimigos_colididos)
            if isinstance(inimigos_colididos[0], Inimigo) and inimigos_colididos[0].tipo == 'perseguidor':
                self.todos_sprites.add(Effect(self.jogador.rect.center, 'demon_hit'))

        # Colisão do jogador com tiros do chefe
        tiros_boss_colididos = pygame.sprite.spritecollide(self.jogador, self.grupo_tiros_boss, True)
        if tiros_boss_colididos:
            self.jogador.vidas -= 1
            self.todos_sprites.add(Effect(self.jogador.rect.center, 'demon_hit'))

    def desenhar_texto(self, texto, x, y, cor=COR_BRANCO, ancora="midleft"):
        superficie_texto = self.fonte.render(texto, True, cor)
        rect_texto = superficie_texto.get_rect()
        setattr(rect_texto, ancora, (x, y))
        self.tela.blit(superficie_texto, rect_texto)

    def desenhar_hud(self):
        self.desenhar_texto(f"Mechaxorcizados: {self.abates}", 20, ALTURA_TELA - 25)
        
        if self.jogador.recarregando:
            self.desenhar_texto("Recarregando...", LARGURA_TELA - 20, ALTURA_TELA - 25, COR_VERMELHO, ancora="midright")
        else:
            self.desenhar_texto(f"Munição: {self.jogador.municao}", LARGURA_TELA - 20, ALTURA_TELA - 25, ancora="midright")
            
        self.desenhar_texto(f"Vidas: {self.jogador.vidas}", LARGURA_TELA // 2, ALTURA_TELA - 25, cor=COR_VERDE, ancora="midtop")

        # Barra de vida do chefe
        if self.boss_spawned and len(self.grupo_boss) > 0:
            boss = self.grupo_boss.sprite
            largura_barra = 300
            altura_barra = 25
            vida_atual_largura = (boss.vida / 30) * largura_barra
            
            borda_rect = pygame.Rect((LARGURA_TELA - largura_barra) / 2, 20, largura_barra, altura_barra)
            vida_rect = pygame.Rect((LARGURA_TELA - largura_barra) / 2, 20, vida_atual_largura, altura_barra)
            
            pygame.draw.rect(self.tela, COR_VERMELHO, borda_rect)
            pygame.draw.rect(self.tela, COR_VERDE, vida_rect)
            pygame.draw.rect(self.tela, COR_BRANCO, borda_rect, 2)

    def desenhar(self):
        self.fundo.draw()
        self.todos_sprites.draw(self.tela)
        self.desenhar_hud()
        self.grupo_mira.draw(self.tela)
        pygame.display.flip()
