# Implementar a função sinc
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

M = 20
# h[i] = sin(2*pi*fc*(i-M/2))/(i-M/2)

fc_Hz = 400
Fs = 8000

fc = fc_Hz / Fs 

h = np.array([np.sin(2*np.pi*fc*(i-M/2))/(i-M/2) if i != M/2 else 2 * np.pi * fc for i in range(M + 1)])

# h[M/2] = 2 * np.pi * fc

plt.stem(h)
plt.xlabel('n')
plt.ylabel('h[n]')
plt.title('Função sinc')
plt.show()

# Freq(z)
w, h = signal.freqz(h, 1, fs=Fs)
plt.plot(w, h)
plt.xlabel('Frequência (Hz)')
plt.ylabel('Atenuação (linear)')
plt.grid(True)
plt.title('Resposta em frequência do filtro sinc')
plt.show()