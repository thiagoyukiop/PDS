# Considere o fitro média móvel da aula passada com k e obtenha:
# A saídado filtro para as seguintes entradas:
# 1. Impulso unitário
# 2. Degrau unitário
# 3. Vetor x = [1, 0.5, 0.25, 0.125]
import numpy as np
import matplotlib.pyplot as plt

# impulso = [1, 0, 0, 0, 0, 0]
# degrau = [1, 1, 1, 1, 1, 1]

amostras = 100

n = np.arange(-10, amostras)

impulso = np.where(n == 0, 1, 0.0)

degrau = np.where(n >= 0, 1, 0.0)

vetor = [1, 0.5, 0.25, 0.125]

x = np.zeros(len(n))

indice_zero = np.where(n == 0)[0][0]

x[indice_zero:indice_zero + len(vetor)] = vetor

plt.subplot(3, 1, 1)
plt.stem(n, impulso)

plt.subplot(3, 1, 2)
plt.stem(n, degrau)

plt.subplot(3, 1, 3)
plt.stem(n, x)
plt.show()

# Implementação do filtro média móvel
k = 8

aux = np.zeros(k - 1)

impulso_aux = impulso.copy()
degrau_aux = degrau.copy()
vetor_aux = x.copy()

for i in range(len(impulso_aux)):
    impulso[i] = (impulso_aux[i] + np.sum(aux)) / k
    aux = np.roll(aux, -1)  # Desloca os valores para a esquerda
    aux[-1] = impulso_aux[i]  # Adiciona o novo valor no

aux = np.zeros(k - 1)

for i in range(len(degrau_aux)):
    degrau[i] = (degrau_aux[i] + np.sum(aux)) / k
    aux = np.roll(aux, -1)  # Desloca os valores para a esquerda
    aux[-1] = degrau_aux[i]  # Adiciona o novo valor no

aux = np.zeros(k - 1)

for i in range(len(vetor_aux)):
    x[i] = (vetor_aux[i] + np.sum(aux)) / k
    aux = np.roll(aux, -1)  # Desloca os valores para a esquerda
    aux[-1] = vetor_aux[i]  # Adiciona o novo valor no

plt.subplot(3, 1, 1)
plt.stem(n, impulso)

plt.subplot(3, 1, 2)
plt.stem(n, degrau)

plt.subplot(3, 1, 3)
plt.stem(n, x)
plt.show()

output_file_1 = "Aula_3/sinal_saida/media_movel_impulso.pcm"
out_1 = np.memmap(output_file_1, dtype='int16', mode='w+', shape=(len(impulso),))
out_1[:] = impulso[:]

output_file_2 = "Aula_3/sinal_saida/media_movel_degrau.pcm"
out_2 = np.memmap(output_file_2, dtype='int16', mode='w+', shape=(len(degrau),))
out_2[:] = degrau[:]

output_file_3 = "Aula_3/sinal_saida/media_movel_vetor.pcm"
out_3 = np.memmap(output_file_3, dtype='int16', mode='w+', shape=(len(x),))
out_3[:] = x[:]