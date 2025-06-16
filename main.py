# Arquivo: main.py
# Ponto de entrada do jogo.

import sys
import pygame
from pacote_jogo.game import Game # Importa a classe Game do novo módulo

# --- Bloco de Execução Principal ---
# Garante que o jogo só rode quando este arquivo é executado diretamente
if __name__ == "__main__":
    g = Game()
    while g.rodando:
        g.novo_jogo()

    pygame.quit()
    sys.exit()
