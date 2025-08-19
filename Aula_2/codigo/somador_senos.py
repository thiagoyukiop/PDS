# Gerar um sinal senoidal formado por duas senoides
import numpy as np
import matplotlib.pyplot as plt

f1 = 200
f2 = 1000

Fs = 8000

A1 = 0.5
A2 = 0.3

A = 16384

amostras = int(Fs + 1)

n = np.arange(0, amostras)

sinal_1 = A1 * np.sin(2 * np.pi * f1/Fs * n)
sinal_2 = A2 * np.sin(2 * np.pi * f2/Fs * n)

sinal = A * (sinal_1 + sinal_2)

plt.stem(n, sinal)
plt.title("Sinal Senoidal 200Hz + 1000Hz")
plt.grid(True)
plt.show()

output_file = "Aula_2/sinal_saida/soma_seno_200+1000Hz.pcm"

out = np.memmap(output_file, dtype='int16', mode='w+', shape=(len(sinal),))
out[:] = sinal[:]