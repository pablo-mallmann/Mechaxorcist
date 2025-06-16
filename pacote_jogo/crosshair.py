# Arquivo: crosshair.py
# Contém a classe para a mira (crosshair).

import pygame
from .settings import *

class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Define o tamanho e a aparência da mira
        tamanho = 25
        self.image = pygame.Surface([tamanho, tamanho], pygame.SRCALPHA)
        cor = (255, 255, 255, 180) # Branco com um pouco de transparência

        # Desenha as duas linhas da mira (horizontal e vertical)
        pygame.draw.line(self.image, cor, (0, tamanho // 2), (tamanho, tamanho // 2), 2)
        pygame.draw.line(self.image, cor, (tamanho // 2, 0), (tamanho // 2, tamanho), 2)

        self.rect = self.image.get_rect()

    def update(self):
        # A mira segue a posição do mouse
        self.rect.center = pygame.mouse.get_pos()
