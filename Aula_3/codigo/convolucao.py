import numpy as np
import matplotlib.pyplot as plt

# x = [1, 1, 1, 1, 1, 1]          # Sinal de entrada
# h = [1, 0.5, 0.25, 0.125]       # Resposta ao impulso

# x = [1, 0, 0, 0, 0, 0]          # Sinal de entrada
h = [1, 0.5, 0.25, 0.125, 0, 0]       # Resposta ao impulso

# x = [1, 0, 1, 0, 1]

x = [-1, -1, 0, 1, 1]

n = len(x) + len(h) - 1         # Tamanho do sinal de saída

sinal = np.convolve(x, h)        # Convolução

plt.subplot(3, 1, 1)
plt.stem(np.arange(-2, len(x) - 2), x)

plt.subplot(3, 1, 2)
plt.stem(h)

plt.subplot(3, 1, 3)
plt.stem(np.arange(-2, len(sinal) - 2), sinal)
plt.show()

# print(sinal)