# Soma de um degrau pelo seu próprio valor anterior
import numpy as np
import matplotlib.pyplot as plt

Amplitude = 16384

Fs = 8000

amostras = int(Fs + 1)
n = np.arange(-1000, amostras)

# sinal degrau unitário
degrau = Amplitude * np.heaviside(n, 1)

degrau_aux = degrau.copy()

aux = 0

for i in range(len(degrau_aux)):
    degrau[i] = degrau_aux[i] - aux
    aux = degrau_aux[i]

# plotar o sinal degrau unitário
plt.stem(n, degrau)
plt.title("Sinal Degrau Unitário")
plt.grid(True)
plt.show()

output_file = "Aula_2/saida_sinais_basicos/sinal_degrau.pcm"

out = np.memmap(output_file, dtype='int16', mode='w+', shape=(len(degrau),))
out[:] = degrau[:]