# Arquivo: game.py
# Contém a classe principal do jogo.

import pygame
import sys
import random

from .settings import *
from .background import Background
from .player import Player
from .inimigo import Inimigo
from .crosshair import Crosshair

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
        self.frequencia_spawn_obstaculo = 3000
        self.ultimo_spawn_obstaculo = pygame.time.get_ticks()

    def carregar_dados(self):
        self.fonte = pygame.font.SysFont(NOME_FONTE, TAMANHO_FONTE)
        try:
            self.som_tiro = pygame.mixer.Sound("assets/som_tiro.flac")
            self.som_tiro.set_volume(0.5)
        except pygame.error as e:
            print(f"Erro ao carregar o som assets/som_tiro.flac: {e}")
            self.som_tiro = None
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
        self.grupo_obstaculos = pygame.sprite.Group()
        
        self.jogador = Player(self.todos_sprites, self.grupo_tiros, self.som_tiro)
        self.todos_sprites.add(self.jogador)
        
        self.grupo_mira = pygame.sprite.GroupSingle()
        self.mira = Crosshair()
        self.grupo_mira.add(self.mira)
        
        self.abates = 0
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

        agora = pygame.time.get_ticks()
        if agora - self.ultimo_spawn_inimigo > self.frequencia_spawn_inimigo:
            self.ultimo_spawn_inimigo = agora
            self.todos_sprites.add(Inimigo(self.jogador))
            self.grupo_inimigos.add(self.todos_sprites.sprites()[-1])


        colisoes_tiro = pygame.sprite.groupcollide(self.grupo_tiros, self.grupo_inimigos, True, True)
        self.abates += len(colisoes_tiro)

        # Verifica colisões que causam dano
        colisoes_obstaculo = pygame.sprite.spritecollide(self.jogador, self.grupo_obstaculos, True)
        if colisoes_obstaculo:
            self.jogador.vidas -= 1

        colisoes_inimigo = pygame.sprite.spritecollide(self.jogador, self.grupo_inimigos, True)
        if colisoes_inimigo:
            self.jogador.vidas -= len(colisoes_inimigo)

        # Se a vida chegar a zero, termina a partida (o loop principal em main.py reiniciará)
        if self.jogador.vidas <= 0:
            self.jogando = False

    def desenhar_texto(self, texto, x, y, cor=COR_BRANCO, ancora="midleft"):
        superficie_texto = self.fonte.render(texto, True, cor)
        rect_texto = superficie_texto.get_rect()
        setattr(rect_texto, ancora, (x, y))
        self.tela.blit(superficie_texto, rect_texto)

    def desenhar_hud(self):
        # Contador de Abates
        self.desenhar_texto(f"Mechaxorcizados: {self.abates}", 20, ALTURA_TELA - 25)
        
        # Contador de Munição
        if self.jogador.recarregando:
            self.desenhar_texto("Recarregando...", LARGURA_TELA - 20, ALTURA_TELA - 25, COR_VERMELHO, ancora="midright")
        else:
            self.desenhar_texto(f"Munição: {self.jogador.municao}", LARGURA_TELA - 20, ALTURA_TELA - 25, ancora="midright")
            
        # Contador de Vidas
        self.desenhar_texto(f"Vidas: {self.jogador.vidas}", LARGURA_TELA // 2, ALTURA_TELA - 25, cor=COR_VERDE, ancora="midtop")

    def desenhar(self):
        self.fundo.draw()
        self.todos_sprites.draw(self.tela)
        self.desenhar_hud()
        self.grupo_mira.draw(self.tela)
        pygame.display.flip()
