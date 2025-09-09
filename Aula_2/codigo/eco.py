import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema
Fs = 8000           # Frequência de amostragem (Hz)
# D = int(0.001 * Fs) # Delay de 1 ms -> 8 amostras
D = 100             # Delay de 100 ms -> 800 amostras     
a0 = 1.0            # Ganho do sinal direto
a1 = 0.5            # Ganho do eco

# Vetor de tempo discreto
n = np.arange(0, 1000)  # 100 amostras para visualização

# Sinal de entrada: impulso unitário
x = np.where(n == 0, 1.0, 0.0)

# Inicializa vetor de saída
y = np.zeros(len(n))

# Implementação do eco com realimentação
for i in range(len(n)):
    # Parte direta do sinal
    y[i] = a0 * x[i]

    # Adiciona eco com atraso D
    if i - D >= 0:
        y[i] += a1 * y[i - D]

# Plot do resultado
plt.figure(figsize=(8, 4))
plt.stem(n, y, basefmt=" ")
plt.title("Implementação do Eco com Realimentação")
plt.xlabel("n")
plt.ylabel("y[n]")
plt.grid(True)
plt.show()

out = np.memmap("Aula_2/sinal_saida/eco.pcm", dtype='int16', mode='w+', shape=(len(y),))
out[:] = y[:]
