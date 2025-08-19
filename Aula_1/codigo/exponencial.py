import numpy as np
import matplotlib.pyplot as plt

Amplitude = 16384

n = np.arange(0, 1001)

# Sequência exponencial
sinal_exponencial_convergente = Amplitude * (0.8 ** n)

# Plotando com pontos 
plt.subplot(3, 1, 1)
plt.stem(n, sinal_exponencial_convergente)
plt.title("Sequência Exponencial Convergente (alpha = 0.8))")
plt.grid(True)

# Sequência exponencial
sinal_exponencial_divergente = Amplitude * (2 ** n)

# Plotando com pontos 
plt.subplot(3, 1, 2)
plt.stem(n, sinal_exponencial_divergente)
plt.title("Sequência Exponencial Divergente (alpha = 2))")
plt.grid(True)

# Sequência exponencial
sinal_exponencial_constante = Amplitude * (1 ** n)

# Plotando com pontos 
plt.subplot(3, 1, 3)
plt.stem(n, sinal_exponencial_constante)
plt.title("Sequência Exponencial Discreto (alpha = 1))")
plt.grid(True)
plt.show()

output_file_1 = "Aula_1/saida_sinais_basicos/sinal_convergente.pcm"

out = np.memmap(output_file_1, dtype='int16', mode='w+', shape=(len(sinal_exponencial_convergente),))
out[:] = sinal_exponencial_convergente[:]

output_file_2 = "Aula_1/saida_sinais_basicos/sinal_divergente.pcm"

out = np.memmap(output_file_2, dtype='int16', mode='w+', shape=(len(sinal_exponencial_divergente),))
out[:] = sinal_exponencial_divergente[:]

output_file_3 = "Aula_1/saida_sinais_basicos/sinal_constante.pcm"

out = np.memmap(output_file_3, dtype='int16', mode='w+', shape=(len(sinal_exponencial_constante),))
out[:] = sinal_exponencial_constante[:]