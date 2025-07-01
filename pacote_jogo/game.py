# Arquivo: game.py
# Contém a classe principal do jogo, agora com gestão de estados.

import pygame
import sys
import random
import os

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
        self.carregar_dados()

    def carregar_dados(self):
        caminho_fonte = os.path.join("assets", "fonts", "PressStart2P-Regular.ttf")
        try:
            self.fonte_grande = pygame.font.Font(caminho_fonte, 40)
            self.fonte_media = pygame.font.Font(caminho_fonte, 22)
            self.fonte_pequena = pygame.font.Font(caminho_fonte, 14)
        except pygame.error:
            print(f"Aviso: Ficheiro da fonte '{caminho_fonte}' não encontrado. A usar fonte padrão do sistema.")
            self.fonte_grande = pygame.font.SysFont(NOME_FONTE, 74)
            self.fonte_media = pygame.font.SysFont(NOME_FONTE, 36)
            self.fonte_pequena = pygame.font.SysFont(NOME_FONTE, TAMANHO_FONTE)
        # Carregamento de sons...
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
        pygame.mouse.set_visible(False)
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
        
        # Atributos de nível e abate
        self.abates = 0
        self.abates_para_vida_extra = 0
        self.nivel = 1
        self.boss_spawned = False
        self.abates_para_proximo_boss = INIMIGOS_PARA_BOSS
        
        # Atributos para o display de nível
        self.mostrar_level_up = False
        self.tempo_level_up = 0
        
        self.frequencia_spawn_inimigo = 1200
        self.ultimo_spawn_inimigo = pygame.time.get_ticks()
        self.frequencia_spawn_worm = 3000
        self.ultimo_spawn_worm = pygame.time.get_ticks()
        
        self.run_partida()

    def run_partida(self):
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

        self.gerir_spawn()
        self.checar_colisoes()
        
        if self.jogador.vidas <= 0:
            self.jogando = False

    def gerir_spawn(self):
        # Verifica se o chefe foi derrotado para reiniciar o spawn e subir de nível
        if self.boss_spawned and not self.grupo_boss:
            self.boss_spawned = False
            self.nivel += 1
            self.jogador.vidas += 1
            self.mostrar_level_up = True
            self.tempo_level_up = pygame.time.get_ticks()

        # Calcula os parâmetros de dificuldade com base no nível atual
        multiplicador_velocidade = 1 + (self.nivel - 1) * AUMENTO_VELOCIDADE_INIMIGO_POR_NIVEL
        velocidade_tiro_boss = VELOCIDADE_TIRO_BOSS_BASE + (self.nivel - 1) * AUMENTO_VELOCIDADE_TIRO_BOSS_POR_NIVEL
        cooldown_tiro_boss = max(500, COOLDOWN_TIRO_BOSS_BASE - (self.nivel - 1) * REDUCAO_COOLDOWN_BOSS_POR_NIVEL)

        if not self.boss_spawned and self.abates >= self.abates_para_proximo_boss:
            self.boss_spawned = True
            # Passa o cooldown calculado para o chefe
            boss = Boss(self.todos_sprites, self.grupo_tiros_boss, self.jogador, velocidade_tiro_boss, cooldown_tiro_boss)
            self.todos_sprites.add(boss)
            self.grupo_boss.add(boss)
            self.abates_para_proximo_boss += INIMIGOS_PARA_BOSS

        if not self.boss_spawned:
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_spawn_inimigo > self.frequencia_spawn_inimigo:
                self.ultimo_spawn_inimigo = agora
                self.todos_sprites.add(Inimigo(self.jogador, multiplicador_velocidade))
                self.grupo_inimigos.add(self.todos_sprites.sprites()[-1])

            if agora - self.ultimo_spawn_worm > self.frequencia_spawn_worm:
                self.ultimo_spawn_worm = agora
                self.todos_sprites.add(Worm(multiplicador_velocidade))
                self.grupo_inimigos.add(self.todos_sprites.sprites()[-1])

    def checar_colisoes(self):
        # Lógica manual para garantir que os tiros só colidam com inimigos vivos.
        for tiro in self.grupo_tiros:
            inimigos_atingidos = pygame.sprite.spritecollide(tiro, self.grupo_inimigos, False)
            for inimigo in inimigos_atingidos:
                if inimigo.is_alive:
                    tiro.kill()
                    self.abates += 1
                    self.abates_para_vida_extra += 1
                    if self.abates_para_vida_extra >= 16:
                        self.jogador.vidas += 1
                        self.abates_para_vida_extra = 0
                    self.todos_sprites.add(Effect(inimigo.rect.center, 'player_hit', self.som_impacto))
                    inimigo.hit()
                    break 

        if self.boss_spawned:
            colisoes_tiro_boss = pygame.sprite.groupcollide(self.grupo_tiros, self.grupo_boss, True, False)
            for boss_atingido in colisoes_tiro_boss.values():
                boss_atingido[0].hit()
                self.todos_sprites.add(Effect(boss_atingido[0].rect.center, 'player_hit', self.som_impacto))

        inimigos_colididos = pygame.sprite.spritecollide(self.jogador, self.grupo_inimigos, True)
        if inimigos_colididos:
            self.jogador.vidas -= len(inimigos_colididos)
            if isinstance(inimigos_colididos[0], Inimigo) and inimigos_colididos[0].tipo == 'perseguidor':
                self.todos_sprites.add(Effect(self.jogador.rect.center, 'demon_hit'))

        tiros_boss_colididos = pygame.sprite.spritecollide(self.jogador, self.grupo_tiros_boss, True)
        if tiros_boss_colididos:
            self.jogador.vidas -= 1
            self.todos_sprites.add(Effect(self.jogador.rect.center, 'demon_hit'))

    def desenhar_texto(self, texto, fonte, cor, x, y, ancora="center"):
        superficie_contorno = fonte.render(texto, True, COR_PRETO)
        offsets = [(-2, -2), (2, -2), (-2, 2), (2, 2)]
        for dx, dy in offsets:
            rect_contorno = superficie_contorno.get_rect(**{ancora: (x + dx, y + dy)})
            self.tela.blit(superficie_contorno, rect_contorno)
        superficie_texto = fonte.render(texto, True, cor)
        rect_texto = superficie_texto.get_rect(**{ancora: (x, y)})
        self.tela.blit(superficie_texto, rect_texto)

    def desenhar_hud(self):
        self.desenhar_texto(f"Mechaxorcizados: {self.abates}", self.fonte_pequena, COR_BRANCO, 20, 20, ancora="topleft")
        self.desenhar_texto(f"Nível: {self.nivel}", self.fonte_pequena, COR_BRANCO, 20, 40, ancora="topleft")

        if self.jogador.recarregando:
            self.desenhar_texto("Recarregando...", self.fonte_pequena, COR_VERMELHO, LARGURA_TELA - 20, 20, ancora="topright")
        else:
            self.desenhar_texto(f"Munição: {self.jogador.municao}", self.fonte_pequena, COR_BRANCO, LARGURA_TELA - 20, 20, ancora="topright")
        
        self.desenhar_texto(f"Vidas: {self.jogador.vidas}", self.fonte_pequena, COR_VERDE, LARGURA_TELA // 2, 50, ancora="midtop")

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

    def desenhar_level_up(self):
        if self.mostrar_level_up:
            agora = pygame.time.get_ticks()
            if agora - self.tempo_level_up < 2000:
                self.desenhar_texto(f"Nível {self.nivel}", self.fonte_grande, COR_VERDE, LARGURA_TELA / 2, ALTURA_TELA / 2)
            else:
                self.mostrar_level_up = False

    def desenhar(self):
        self.fundo.draw()
        self.todos_sprites.draw(self.tela)
        self.desenhar_hud()
        self.desenhar_level_up()
        self.grupo_mira.draw(self.tela)
        pygame.display.flip()
    
    def mostrar_tela_start(self):
        pygame.mouse.set_visible(True)
        self.fundo.draw()
        self.desenhar_texto("Mechaxorcist", self.fonte_grande, COR_BRANCO, LARGURA_TELA / 2, ALTURA_TELA / 4)
        botao_start = pygame.Rect(LARGURA_TELA/2 - 100, ALTURA_TELA/2 - 25, 200, 50)
        botao_sair = pygame.Rect(LARGURA_TELA/2 - 100, ALTURA_TELA/2 + 50, 200, 50)
        pygame.draw.rect(self.tela, COR_VERDE, botao_start)
        pygame.draw.rect(self.tela, COR_VERMELHO, botao_sair)
        self.desenhar_texto("Start", self.fonte_media, COR_BRANCO, botao_start.centerx, botao_start.centery)
        self.desenhar_texto("Sair", self.fonte_media, COR_BRANCO, botao_sair.centerx, botao_sair.centery)
        pygame.display.flip()
        self.esperar_por_input_menu(botao_start, botao_sair)

    def esperar_por_input_menu(self, botao_start, botao_sair):
        esperando = True
        while esperando:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    self.rodando = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if botao_start.collidepoint(event.pos):
                        esperando = False
                    if botao_sair.collidepoint(event.pos):
                        esperando = False
                        self.rodando = False
    
    def mostrar_tela_game_over(self):
        pygame.mouse.set_visible(True)
        self.fundo.draw()
        self.desenhar_texto("GAME OVER", self.fonte_grande, COR_VERMELHO, LARGURA_TELA / 2, ALTURA_TELA / 4)
        self.desenhar_texto(f"Mechaxorcizados: {self.abates}", self.fonte_media, COR_BRANCO, LARGURA_TELA / 2, ALTURA_TELA / 2)
        botao_reiniciar = pygame.Rect(LARGURA_TELA/2 - 125, ALTURA_TELA * 3/4 - 25, 250, 50)
        pygame.draw.rect(self.tela, COR_VERDE, botao_reiniciar)
        self.desenhar_texto("Reiniciar", self.fonte_media, COR_BRANCO, botao_reiniciar.centerx, botao_reiniciar.centery)
        pygame.display.flip()
        self.esperar_por_input_game_over(botao_reiniciar)
    
    def esperar_por_input_game_over(self, botao_reiniciar):
        esperando = True
        while esperando:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    self.rodando = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if botao_reiniciar.collidepoint(event.pos):
                        esperando = False
