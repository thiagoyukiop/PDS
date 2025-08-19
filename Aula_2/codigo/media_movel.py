# Implementação de algoritmos
# Média Móvel de k elementos da entrada
import numpy as np
import matplotlib.pyplot as plt

Amplitude = 16384
Fs = 8000

k = 20
amostras = int(Fs + 1)
n = np.arange(0, amostras)

# aux_1 = 0
# aux_2 = 0
# aux_3 = 0

# vetor aux recebe tamanho de k-1
aux = np.zeros(k - 1)

# sinal = [10, 2, 8, -4, -2, 3]
# sinal = [22, 100, 4, 8, 10, 6]
sinal = np.where(n == 0, Amplitude, 0.0)

sinal_aux = sinal.copy()

for i in range(len(sinal_aux)):
    sinal[i] = (sinal_aux[i] + np.sum(aux)) / k
    aux = np.roll(aux, -1)  # Desloca os valores para a esquerda
    aux[-1] = sinal_aux[i]  # Adiciona o novo valor no

# Plotando o sinal
plt.stem(n, sinal)
plt.title(f"Média Móvel de {k} elementos")
plt.grid(True)
plt.show()
output_file = "Aula_2/sinal_saida/media_movel.pcm"
out = np.memmap(output_file, dtype='int16', mode='w+', shape=(len(sinal),))
out[:] = sinal[:]