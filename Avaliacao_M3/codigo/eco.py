import numpy as np
import os

# --- Parâmetros de Geração ---
Fs = 8000           # Frequência de amostragem
D = 800             # Atraso do Eco (100 ms * 8000 Hz)
a1 = 0.5            # Ganho do Eco
DURACAO_S = 3       # Duração da simulação em segundos
N_AMOSTRAS = Fs * DURACAO_S # Número total de amostras (24000)

FAR_FILE = 'Avaliacao_M3/sinal_entrada/far.pcm'
NEAR_FILE = 'Avaliacao_M3/sinal_entrada/near_com_eco_2.pcm'

# --- 1. Geração do Sinal de Referência (FAR) ---

# Gera ruído branco normalizado entre -1.0 e 1.0
sinal_far_float = np.random.uniform(-1.0, 1.0, N_AMOSTRAS).astype(np.float32)

# --- 2. Geração do Sinal com Eco (NEAR) ---

sinal_near_float = np.zeros(N_AMOSTRAS, dtype=np.float32)

# O sinal 'near' é a soma do sinal local (zero para este teste)
# mais o sinal 'far' com eco.

for i in range(N_AMOSTRAS):
    # Simula o componente de eco (Atraso D)
    if i - D >= 0:
        sinal_near_float[i] = a1 * sinal_far_float[i - D]
    # Aqui não adicionamos sinal de voz local ou ruído adicional,
    # focando apenas no eco que o LMS deve cancelar.

# --- 3. Normalização e Conversão para int16 ---

# Encontra o pico máximo para evitar clipping ao escalar para int16
max_val = np.max(np.abs(sinal_far_float))
if max_val == 0:
    max_val = 1.0

# Escala os sinais para caberem em int16 (-32768 a 32767)
sinal_far_int16 = (sinal_far_float / max_val * 32767).astype(np.int16)
sinal_near_int16 = (sinal_near_float / max_val * 32767).astype(np.int16)

# --- 4. Criação de Diretórios e Escrita dos Arquivos PCM ---

# Cria o diretório se não existir
diretorio = os.path.dirname(FAR_FILE)
os.makedirs(diretorio, exist_ok=True)

# Salva o arquivo FAR
with open(FAR_FILE, 'wb') as f:
    sinal_far_int16.tofile(f)

# Salva o arquivo NEAR (com eco)
with open(NEAR_FILE, 'wb') as f:
    sinal_near_int16.tofile(f)

print(f"Arquivos gerados com sucesso:")
print(f"  - {FAR_FILE} ({N_AMOSTRAS} amostras)")
print(f"  - {NEAR_FILE} ({N_AMOSTRAS} amostras)")