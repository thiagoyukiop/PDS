import numpy as np
import matplotlib.pyplot as plt

Amplitude = 16384

# sinal degrau unitário
n = np.arange(-1000, 1001)

degrau = Amplitude * np.heaviside(n, 1)

# plotar o sinal degrau unitário
plt.stem(n, degrau)
plt.title("Sinal Degrau Unitário")
plt.grid(True)
plt.show()

output_file = "Aula_1/saida_sinais_basicos/sinal_degrau.pcm"

out = np.memmap(output_file, dtype='int16', mode='w+', shape=(len(degrau),))
out[:] = degrau[:]