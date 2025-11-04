# Pseudo-código para projetode filtro FIR passa-alta

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parâmetros iniciais
fc_Hz = 400
Fs = 8000
fc = fc_Hz / Fs
M = 100

# Projeto do filtro Passa-Alta Hamming
n = np.arange(M + 1)
center = M / 2
h_ideal = np.sinc(2 * fc * (n - center))

hamming = 0.54 - 0.46 * np.cos(2 * np.pi * n / M)
h = h_ideal * hamming

h = h / np.sum(h)

h_saida = -h
h_saida[int(center)] += 1

# Plotagem da resposta ao impulso
plt.stem(h_saida)
plt.xlabel('n')
plt.ylabel('h[n]')
plt.title('Filtro FIR Passa-Alta com Janela Hamming')
plt.show()

# Resposta em frequência
w, H = signal.freqz(h_saida, 1, fs=Fs)
H_db = 20 * np.log10(np.abs(H)) 
plt.plot(w, H_db)
plt.xlabel('Frequência (Hz)')
plt.ylabel('Atenuação (dB)')
plt.grid(True)
plt.title('Resposta em frequência do filtro FIR Passa-Alta')
plt.ylim(-120, 10)
plt.xlim(0, Fs/2)
plt.show()

# salvar o vetor h
np.savetxt('Aula_10/sinal_saida/h_fir_pa.txt', h_saida)