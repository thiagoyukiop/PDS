# Implementação de algoritmos
# Média Móvel de k elementos da entrada do sweep
import numpy as np
import matplotlib.pyplot as plt
import os

Amplitude = 16384
Fs = 8000

k = 20
amostras = int(Fs + 1)
n = np.arange(0, amostras)

# vetor aux recebe tamanho de k-1
aux = np.zeros(k - 1)

input_file = os.path.join("Aula_2/sinal_entrada", "sweep_20_3k4.pcm")
sinal = np.memmap(input_file, dtype='int16', mode='r+', shape=(amostras,))


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
output_file = os.path.join("Aula_2/sinal_saida/", f"media_movel_20_3k4Hz_k{k}.pcm")

out = np.memmap(output_file, dtype='int16', mode='w+', shape=(len(sinal),))
out[:] = sinal[:]