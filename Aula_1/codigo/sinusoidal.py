import numpy as np
import matplotlib.pyplot as plt

Amplitude = 16384

n = np.arange(-1000, 1001)

# Sinal de sequência sinusoidal
senoidal = Amplitude * np.sin(2 * np.pi * 0.001 * n)

# Plotando com pontos 
plt.stem(n, senoidal)
plt.title("Sequência Sinosoidal ")
plt.grid(True)
plt.show()

output_file = "Aula_1/saida_sinais_basicos/sinal_sinusoidal.pcm"

out = np.memmap(output_file, dtype='int16', mode='w+', shape=(len(senoidal),))
out[:] = senoidal[:]