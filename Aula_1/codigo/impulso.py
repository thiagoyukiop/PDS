import numpy as np
import matplotlib.pyplot as plt

Amplitude = 16384

# sinal impulso unitário
n = np.arange(-1000, 1001)

impulso = np.where(n == 0, Amplitude, 0.0)

# Plotando
plt.stem(n, impulso)
plt.title("Impulso Unitário (δ[n])")
plt.grid(True)
plt.show()

output_file = "Aula_1/saida_sinais_basicos/sinal_impulso.pcm"

out = np.memmap(output_file, dtype='int16', mode='w+', shape=(len(impulso),))
out[:] = impulso[:]