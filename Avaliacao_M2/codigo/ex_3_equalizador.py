import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parâmetros iniciais
Fs = 44100

# PB
G_PB = 20
V0_PB = 10**(G_PB/20)
H0_PB = V0_PB - 1
fc_PB = 1000

# PF
G_PF = 10
V0_PF = 10**(G_PF/20)
H0_PF = V0_PF - 1
fc_PF = 5000
fb = 2000
d = -np.cos(2 * np.pi *fc_PF / Fs)

# PA
G_PA = -10
V0_PA = 10**(G_PA/20)
H0_PA = V0_PA - 1
fc_PA = 10000

# Definindo aB para cada tipo de filtro

# aB Passa-baixa
if(G_PB >= 0):
    aB_num_PB = np.tan(np.pi * fc_PB / Fs) - 1
    aB_den_PB = np.tan(np.pi * fc_PB / Fs) + 1
    aB_PB = aB_num_PB / aB_den_PB
else:
    aB_num_PB = np.tan(np.pi * fc_PB / Fs) - V0_PB
    aB_den_PB = np.tan(np.pi * fc_PB / Fs) + V0_PB
    aB_PB = aB_num_PB / aB_den_PB

# aB Passa-faixa
if(G_PF >= 0):
    aB_num_PF = np.tan(np.pi * fb / Fs) - 1
    aB_den_PF = np.tan(np.pi * fb / Fs) + 1
    aB_PF = aB_num_PF / aB_den_PF
else:
    aB_num_PF = np.tan(np.pi * fb / Fs) - V0_PF
    aB_den_PF = np.tan(np.pi * fb / Fs) + V0_PF
    aB_PF = aB_num_PF / aB_den_PF

# aB Passa-alta
if(G_PA >= 0):
    aB_num_PA = np.tan(np.pi * fc_PA / Fs) - 1
    aB_den_PA = np.tan(np.pi * fc_PA / Fs) + 1
    aB_PA = aB_num_PA / aB_den_PA
else:
    aB_num_PA = np.tan(np.pi * fc_PA / Fs) - V0_PA
    aB_den_PA = np.tan(np.pi * fc_PA / Fs) + V0_PA
    aB_PA = aB_num_PA / aB_den_PA

# Construindo os coeficientes dos filtros
# ---- Filtro Passa-baixa ----
# Coeficientes do Numerador de Hz (a)
a0_PB = 1 + H0_PB/2 + H0_PB/2 * aB_PB
a1_PB = aB_PB * (1 + H0_PB/2) + H0_PB/2
a_PB = np.array([a0_PB, a1_PB])

# Coeficientes do Denominador de Hz (b)

# ---- Filtro Passa-faixa ----
# Coeficientes do Numerador de Hz (a)
a0_PF = 1 + H0_PF/2 + H0_PF/2*aB_PF
a1_PF = (d - d*aB_PF)
a2_PF = -H0_PF/2 - H0_PF/2*aB_PF - aB_PF
a_PF = np.array([a0_PF, a1_PF, a2_PF])

# Coeficientes do Denominador de Hz (b)
b0_PF = 1
b1_PF = (d - d*aB_PF)
b2_PF = -aB_PF
b_PF = np.array([b0_PF, b1_PF, b2_PF])
b0_PB = 1
b1_PB = aB_PB
b_PB = np.array([b0_PB, b1_PB])

# ---- Filtro Passa-alta ----
# Coeficientes do Numerador de Hz (a)
a0_PA = 1 + H0_PA/2 - H0_PA/2 * aB_PA
a1_PA = aB_PA * (1 + H0_PA/2) - H0_PA/2
a_PA = np.array([a0_PA, a1_PA])

# Coeficientes do Denominador de Hz (b)
b0_PA = 1
b1_PA = aB_PA
b_PA = np.array([b0_PA, b1_PA])

w, H_PB = signal.freqz(a_PB, b_PB, worN=8192, fs=Fs)
_, H_PF = signal.freqz(a_PF, b_PF, worN=8192, fs=Fs)
_, H_PA = signal.freqz(a_PA, b_PA, worN=8192, fs=Fs)

# ---- Resposta em frequência ----
H_total = H_PB * H_PF * H_PA
H_db = 20 * np.log10(np.abs(H_total))

plt.plot(w, H_db)
plt.title("Resposta em Frequência - Equalizador 3 Bandas")
plt.xlabel("Frequência (Hz)")
plt.ylabel("Ganho (dB)")
plt.grid(True)
plt.show()

# ---------- Execução do filtro no sinal de entrada ----------

# Leitura do sinal de entrada (sweep)
input_path_sweep = "Avaliacao_M2/sinal_entrada/sweep_20_20k.pcm"
sinal = np.memmap(input_path_sweep, dtype='int16', mode='r')
sinal = sinal.astype(np.float32) # Normalizando o sinal
sinal /= np.max(np.abs(sinal))
n = np.arange(len(sinal))

saida = signal.lfilter(a_PB, b_PB, sinal)
saida = signal.lfilter(a_PF, b_PF, saida)
saida = signal.lfilter(a_PA, b_PA, saida)

saida /= np.max(np.abs(saida)) # Normalizando o sinal de saída

# Visualização do sinal de entrada
plt.subplot(2, 1, 1)
plt.plot(n, sinal)
plt.title("Sinal de Entrada (Sweep)")
plt.grid(True)

# Visualização do sinal de saída
plt.subplot(2, 1, 2)
plt.plot(n, saida)
plt.title("Executando Equalizador 3 Bandas")
plt.grid(True)
plt.tight_layout()
plt.show()