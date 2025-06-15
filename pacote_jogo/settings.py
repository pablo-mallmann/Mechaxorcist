# Arquivo: settings.py
# Este arquivo contém todas as constantes e configurações do jogo.

# Configurações da tela
LARGURA_TELA = 1080 # Aumentei a tela para dar mais espaço
ALTURA_TELA = 500
FPS = 60 # Frames por segundo
ALTURA_CHAO = ALTURA_TELA - 20 # Define a altura do chão

# Cores (Padrão RGB)
COR_PRETO = (0, 0, 0)
COR_BRANCO = (255, 255, 255)
COR_VERDE = (0, 255, 0)
COR_VERMELHO = (255, 0, 0)

# Configurações do Jogador
VELOCIDADE_JOGADOR = 6
GRAVIDADE = 0.6
FORCA_SALTO = -15 # Valor negativo para ir para cima

# Configurações do Tiro
VELOCIDADE_TIRO = 12
COOLDOWN_TIRO = 250 # Tempo em ms entre os tiros automáticos

# Configurações dos Inimigos
VELOCIDADE_INIMIGO_X_INICIAL = 5
VELOCIDADE_INIMIGO_Y_INICIAL = 20
