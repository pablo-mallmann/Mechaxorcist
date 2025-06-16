# Arquivo: background.py
# Contém a classe para gerenciar o fundo parallax de múltiplas camadas.

import sys
import os
import pygame
from .settings import *

class Background:
    def __init__(self, tela):
        self.tela = tela
        # --- Camadas do Céu ---
        self.camadas_ceu = []
        self.velocidades_ceu = [0.1, 0.2, 0.3, 0.5, 0.8]
        self.posicoes_x_ceu = [0] * 5

        # --- Camada do Chão ---
        self.imagem_chao = None
        self.velocidade_chao = 1.2
        self.posicao_x_chao = 0

        # Carrega as 5 imagens do céu
        for i in range(1, 6):
            caminho_imagem = os.path.join("assets", f"fundo{i}.png")
            try:
                imagem = pygame.image.load(caminho_imagem).convert_alpha()
                altura = int(LARGURA_TELA * imagem.get_height() / imagem.get_width())
                imagem_redimensionada = pygame.transform.scale(imagem, (LARGURA_TELA, altura))
                self.camadas_ceu.append(imagem_redimensionada)
            except pygame.error as e:
                print(f"ERRO: Não foi possível carregar a imagem do céu: {caminho_imagem}")
                print(e)
                sys.exit()
        
        # Carrega a imagem do chão (fundo6.png)
        caminho_chao = os.path.join("assets", "fundo6.png")
        try:
            self.imagem_chao = pygame.image.load(caminho_chao).convert_alpha()
            altura_chao_img = int(LARGURA_TELA * self.imagem_chao.get_height() / self.imagem_chao.get_width())
            self.imagem_chao = pygame.transform.scale(self.imagem_chao, (LARGURA_TELA, altura_chao_img))
        except pygame.error as e:
            print(f"ERRO: Não foi possível carregar a imagem do chão: {caminho_chao}")
            print(e)
            sys.exit()

    def update(self):
        # Atualiza a posição X das camadas do céu
        for i in range(len(self.camadas_ceu)):
            self.posicoes_x_ceu[i] -= self.velocidades_ceu[i]
            if self.posicoes_x_ceu[i] <= -LARGURA_TELA:
                self.posicoes_x_ceu[i] = 0

        # Atualiza a posição X da camada do chão
        self.posicao_x_chao -= self.velocidade_chao
        if self.posicao_x_chao <= -LARGURA_TELA:
            self.posicao_x_chao = 0

    def draw(self):
        # 1. Desenha as camadas do céu primeiro
        for i in range(len(self.camadas_ceu)):
            self.tela.blit(self.camadas_ceu[i], (self.posicoes_x_ceu[i], 0))
            self.tela.blit(self.camadas_ceu[i], (self.posicoes_x_ceu[i] + LARGURA_TELA, 0))
        
        # 2. Desenha a camada do chão na posição correta
        if self.imagem_chao:
            # Calcula a posição Y para que a PARTE DE BAIXO da imagem alinhe com a PARTE DE BAIXO da tela
            pos_y_chao = ALTURA_TELA - self.imagem_chao.get_height()
            
            # Desenha a imagem do chão e sua cópia para o loop
            self.tela.blit(self.imagem_chao, (self.posicao_x_chao, pos_y_chao))
            self.tela.blit(self.imagem_chao, (self.posicao_x_chao + LARGURA_TELA, pos_y_chao))
