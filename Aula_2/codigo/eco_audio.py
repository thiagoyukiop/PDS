import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema
Fs = 8000           # Frequência de amostragem (Hz)
# D = int(0.001 * Fs) # Delay de 1 ms -> 8 amostras
D = 4000             # Delay de 100 ms -> 800 amostras     
a0 = 1.0            # Ganho do sinal direto
a1 = 0.5            # Ganho do eco

x = np.memmap('Aula_2/sinal_entrada/alo.pcm', dtype='int16', mode='r')

# Plotar o sinal do áudio de entrada
plt.subplot(2, 1, 1)
plt.plot(x)
plt.grid(True)
plt.title("Sinal de Áudio de Entrada")

# x = x*10

# Inicializa vetor de saída
y = np.empty(len(x)*2)

# Implementação do eco com realimentação
for i in range(len(y)):
    if i < len(x):
        x_val = x[i]
    else:
        x_val = 0        
    # Parte direta do sinal
    y[i] = a0 * x_val

    # Adiciona eco com atraso D
    if i >= D:
        y[i] += a1 * y[i - D]

# Plot do resultado
plt.subplot(2, 1, 2)
plt.plot(y)
# plt.stem(n, y, basefmt=" ")
plt.title("Saída com Eco")
plt.xlabel("n")
plt.ylabel("y[n]")
plt.grid(True)
plt.show()

out = np.memmap("Aula_2/sinal_saida/eco_alo.pcm", dtype='int16', mode='w+', shape=(len(y),))
out[:] = y[:]
