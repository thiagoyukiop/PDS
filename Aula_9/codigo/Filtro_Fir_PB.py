# Pseudo-código para projetode filtro FIR passa-baixa

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

fc_Hz = 1000
Fs = 8000
fc = fc_Hz / Fs
M = 100

n = np.arange(M + 1)
center = M / 2
h_ideal = np.sinc(2 * fc * (n - center))

hamming = 0.54 - 0.46 * np.cos(2 * np.pi * n / M)
h = h_ideal * hamming

h = h / np.sum(h)
plt.stem(h)
plt.xlabel('n')
plt.ylabel('h[n]')
plt.title('Filtro FIR Passa-Baixa com Janela Hamming')
plt.show()

# Resposta em frequência
w, H = signal.freqz(h, 1, fs=Fs)
H_db = 20 * np.log10(np.abs(H)) 
plt.plot(w, H_db)
plt.xlabel('Frequência (Hz)')
plt.ylabel('Atenuação (dB)')
plt.grid(True)
plt.title('Resposta em frequência do filtro FIR Passa-Baixa')
plt.ylim(-120, 10)
plt.xlim(0, Fs/2)
plt.show()

# salvar o vetor h
np.savetxt('Aula_9/sinal_saida/h_fir_pb.txt', h)