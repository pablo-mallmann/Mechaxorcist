# Arquivo: background.py
# Contém a classe para gerenciar o fundo parallax de múltiplas camadas.

import sys
import pygame
from .settings import *

class Background:
    def __init__(self, tela):
        self.tela = tela
        self.camadas = []
        self.velocidades = [0.1, 0.2, 0.3, 0.5, 0.8] # Velocidades diferentes para cada camada

        # Carrega as 6 imagens do fundo
        for i in range(1, 6):
            try:
                # Carrega a imagem e a converte para um formato mais rápido de desenhar
                imagem = pygame.image.load(f"assets/fundo{i}.png").convert_alpha()
                # Redimensiona a imagem para preencher a largura da tela, mantendo a proporção
                altura = int(LARGURA_TELA * imagem.get_height() / imagem.get_width())
                imagem_redimensionada = pygame.transform.scale(imagem, (LARGURA_TELA, altura))
                self.camadas.append(imagem_redimensionada)
            except pygame.error as e:
                print(f"Erro ao carregar a imagem assets/fundo{i}.png: {e}")
                # Se uma imagem não puder ser carregada, saímos para evitar mais erros.
                # Você pode adicionar uma imagem placeholder aqui se preferir.
                sys.exit()

        # Posições de rolagem para cada camada
        self.posicoes_x = [0] * 5

    def update(self):
        # Atualiza a posição X de cada camada baseada em sua velocidade
        for i in range(len(self.camadas)):
            self.posicoes_x[i] -= self.velocidades[i]
            # Se a imagem saiu completamente da tela pela esquerda, reseta sua posição
            if self.posicoes_x[i] <= -LARGURA_TELA:
                self.posicoes_x[i] = 0

    def draw(self):
        # Desenha cada camada na tela em sua respectiva posição
        for i in range(len(self.camadas)):
            # Posição da primeira imagem da camada
            pos_1 = (self.posicoes_x[i], 0)
            # Posição da segunda imagem, que aparece logo em seguida para criar o loop
            pos_2 = (self.posicoes_x[i] + LARGURA_TELA, 0)
            
            self.tela.blit(self.camadas[i], pos_1)
            self.tela.blit(self.camadas[i], pos_2)

