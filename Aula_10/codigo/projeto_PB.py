# Pseudo-código para projeto de filtro FIR passa-baixa

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parâmetros iniciais
fc_Hz = 400
Fs = 8000
fc = fc_Hz / Fs
M = 100

# Projeto do filtro Passa-Baixa usando janela Blackman
n = np.arange(M + 1)
center = M / 2
h_ideal = np.sinc(2 * fc * (n - center))

blackman = 0.42 - 0.5*np.cos(2 * np.pi * n / M) + 0.08 * np.cos(4 * np.pi * n / M)
h = h_ideal * blackman

h = h / np.sum(h)

# Resposta em frequência
w, H = signal.freqz(h, 1, fs=Fs)
H_db = 20 * np.log10(np.abs(H)) 
plt.plot(w, H_db)
plt.xlabel('Frequência (Hz)')
plt.ylabel('Atenuação (dB)')
plt.grid(True)
plt.title('Resposta em frequência do filtro FIR Passa-Baixa, vermelho M=40, azul M=100')
plt.ylim(-120, 10)
plt.xlim(0, Fs/2)
# plt.show()

# salvar o vetor h
np.savetxt('Aula_10/sinal_saida/h_fir_pb_blackman_M100.txt', h, "%E,")

# Comparando com um M de 40

M = 40

# Projeto do filtro Passa-Baixa usando janela Hamming
n = np.arange(M + 1)
center = M / 2
h_ideal = np.sinc(2 * fc * (n - center))

hamming = 0.54 - 0.46 * np.cos(2 * np.pi * n / M)
h = h_ideal * hamming

h = h / np.sum(h)

# Resposta em frequência
w, H = signal.freqz(h, 1, fs=Fs)
H_db = 20 * np.log10(np.abs(H)) 
plt.plot(w, H_db, "red")
plt.grid(True)
plt.ylim(-120, 10)
plt.xlim(0, Fs/2)
plt.show()
