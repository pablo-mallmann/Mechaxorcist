# Arquivo: settings.py
# Este arquivo contém todas as constantes e configurações do jogo.

# Configurações da tela
LARGURA_TELA = 1080
ALTURA_TELA = 500
FPS = 60 # Frames por segundo
ALTURA_CHAO = ALTURA_TELA - 20 # Define a altura do chão

# Cores (Padrão RGB)
COR_PRETO = (0, 0, 0)
COR_BRANCO = (255, 255, 255)
COR_VERDE = (0, 255, 0)
COR_VERMELHO = (255, 0, 0)

# Configurações do Jogador
VELOCIDADE_JOGADOR = 5
GRAVIDADE = 0.3
FORCA_SALTO = -8
FRICCAO_JOGADOR = -0.12
VIDAS_JOGADOR = 3 # Vida inicial

# Configurações do Tiro
VELOCIDADE_TIRO = 10
MUNICAO_MAXIMA = 15
TEMPO_RECARGA = 3000

# Configurações de UI
NOME_FONTE = 'arial'
TAMANHO_FONTE = 24
