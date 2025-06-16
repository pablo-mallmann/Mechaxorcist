# Arquivo: main.py
# Este é o arquivo principal que fica FORA do pacote e serve apenas para iniciar o jogo.

import pygame
import sys
import random

# --- Importações do Pacote 'pacote_jogo' ---
from pacote_jogo.settings import *
from pacote_jogo.background import Background
from pacote_jogo.player import Player
from pacote_jogo.inimigo import Inimigo

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Space Shooter Dinâmico")
        self.clock = pygame.time.Clock()
        self.rodando = True
        self.fundo = Background(self.tela)
        
        self.carregar_sons()

        self.frequencia_spawn_inimigo = 1200
        self.ultimo_spawn_inimigo = pygame.time.get_ticks()
        self.frequencia_spawn_obstaculo = 3000
        self.ultimo_spawn_obstaculo = pygame.time.get_ticks()

    def carregar_sons(self):
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

    def atualizar_logica(self):
        self.fundo.update()
        self.todos_sprites.update()

        agora = pygame.time.get_ticks()
        if agora - self.ultimo_spawn_inimigo > self.frequencia_spawn_inimigo:
            self.ultimo_spawn_inimigo = agora
            inimigo = Inimigo()
            self.todos_sprites.add(inimigo)
            self.grupo_inimigos.add(inimigo)


        pygame.sprite.groupcollide(self.grupo_tiros, self.grupo_inimigos, True, True)

        if pygame.sprite.spritecollide(self.jogador, self.grupo_obstaculos, False):
            self.jogando = False
            
        if pygame.sprite.spritecollide(self.jogador, self.grupo_inimigos, False):
            self.jogando = False

    def desenhar(self):
        # 1. Desenha o fundo completo (céu e chão)
        self.fundo.draw()
        
        # 2. Desenha todos os sprites do jogo por cima do fundo
        self.todos_sprites.draw(self.tela)
        
        pygame.display.flip()

if __name__ == "__main__":
    g = Game()
    while g.rodando:
        g.novo_jogo()

    pygame.quit()
    sys.exit()
