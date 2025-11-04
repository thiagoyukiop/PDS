# Implementar a janela hamming
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

M = 20
# w[i] = 0.54 - 0.46*cos(2*pi*i/M)

# w[0] e w[20]

# Plotar no tempo Hamming e Blackman
# Hamming em azul e Blackman em vermelho

w_hm = np.array([0.54 - 0.46 * np.cos(2 * np.pi * i / M) for i in range(M + 1)])
plt.stem(w_hm)
plt.xlabel('n')
plt.ylabel('w[n]')
plt.title('Janela de Hamming (azul) e Janela Blackman (vermelho)')
w_bm = np.array([0.42 - 0.5 * np.cos(2 * np.pi * i / M) + 0.08 * np.cos(4 * np.pi * i / M) for i in range(M + 1)])
plt.stem(w_bm, "red")
plt.show()


# Freq(z)
# de 10 a 120 dB

w_freq_hm, h_hm = signal.freqz(w_hm, worN=512)
plt.plot(w_freq_hm, 20 * np.log10(np.abs(h_hm)))
plt.xlabel('Frequência (rad/amostra)')
plt.ylabel('Atenuação (dB)')
plt.grid(True)
plt.title('Resposta em frequência da Janela de Hamming (azul) e Janela Blackman (vermelho)')
w_freq_bm, h_bm = signal.freqz(w_bm, worN=512)
plt.plot(w_freq_bm, 20 * np.log10(np.abs(h_bm)), "red")
plt.ylim([-120, 10])
plt.show()