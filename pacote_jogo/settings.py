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
COR_AZUL = (0, 0, 255)
COR_AMARELO = (255, 255, 0)

# Configurações do Jogador
VELOCIDADE_JOGADOR = 5
GRAVIDADE = 0.3
FORCA_SALTO = -8
FRICCAO_JOGADOR = -0.12
VIDAS_JOGADOR = 3

# Configurações do Tiro
VELOCIDADE_TIRO_BASE = 10.0
MUNICAO_MAXIMA_BASE = 15
TEMPO_RECARGA_BASE = 3000 # 3 segundos em milissegundos
TIRO_PENETRATION_BASE = 1
PLAYER_PROJECTILE_COUNT_BASE = 1

# Configurações de Dificuldade e Nível
INIMIGOS_PARA_BOSS_BASE = 10
AUMENTO_INIMIGOS_PARA_BOSS_POR_NIVEL = 5
VIDA_BOSS_BASE = 20
AUMENTO_VIDA_BOSS_POR_NIVEL = 5
VELOCIDADE_TIRO_BOSS_BASE = 7.0
AUMENTO_VELOCIDADE_TIRO_BOSS_POR_NIVEL = 0.5
COOLDOWN_TIRO_BOSS_BASE = 1500 # Tempo em ms
REDUCAO_COOLDOWN_BOSS_POR_NIVEL = 100 # Reduz 100ms a cada nível
AUMENTO_VELOCIDADE_INIMIGO_POR_NIVEL = 0.1 # Aumenta a velocidade em 10%

# Configurações de UI
NOME_FONTE = 'arial'
