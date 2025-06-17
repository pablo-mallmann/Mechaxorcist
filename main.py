# Arquivo: main.py
# Ponto de entrada do jogo.

import sys
import pygame
from pacote_jogo.game import Game

class App:
    def __init__(self):
        self.jogo = Game()

    def run(self):
        while self.jogo.rodando:
            self.jogo.mostrar_tela_start()
            if not self.jogo.rodando:
                break
            self.jogo.novo_jogo()
            if self.jogo.rodando: # Só mostra a tela de game over se o jogo não foi fechado
                self.jogo.mostrar_tela_game_over()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.run()
