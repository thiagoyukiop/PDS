# Implementação de algoritmos
# Média Móvel de k elementos da entrada do sweep
import numpy as np
import matplotlib.pyplot as plt
import os

Amplitude = 16384
Fs = 80000

k = 4

# vetor aux recebe tamanho de k-1
aux = np.zeros(k - 1)

input_file = os.path.join("Aula_2/sinal_entrada", "sweep_20_3k4.pcm")
sinal = np.memmap(input_file, dtype='int16', mode='r')
sinal_aux = sinal.copy()
n = np.arange(0, len(sinal_aux))

plt.subplot(2, 1, 1)
plt.stem(n, sinal)
plt.title("Sinal de Entrada (Sweep)")
plt.grid(True)

sinal_saida = np.zeros(len(sinal_aux))

for i in range(len(sinal_aux)):
    sinal_saida[i] = (sinal_aux[i] + np.sum(aux)) / k
    aux = np.roll(aux, -1)  # Desloca os valores para a esquerda
    aux[-1] = sinal_aux[i]  # Adiciona o novo valor no

# Plotando o sinal entrada e saída
plt.subplot(2, 1, 2)
plt.stem(n, sinal_saida)
plt.title(f"Sinal de Saída - Média Móvel de {k} elementos")
plt.grid(True)
plt.tight_layout()
plt.show()

output_file = os.path.join("Aula_2/sinal_saida/", f"media_movel_20_3k4Hz_k{k}.pcm")

out = np.memmap(output_file, dtype='int16', mode='w+', shape=(len(sinal),))
out[:] = sinal[:]