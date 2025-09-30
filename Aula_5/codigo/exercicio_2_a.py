# Considere 𝑦[𝑛] = 𝑥[𝑛] * ℎ[𝑛] , 𝑥[𝑛] = 𝑢[𝑛] − 𝑢[𝑛 − 2] e h[n] = (0.5)^n * u[n]
import numpy as np
import matplotlib.pyplot as plt

n = np.arange(0, 9, 1)

x = np.where((n >= 0) & (n < 2), 1, 0.0)
h = np.where(n >= 0, 0.5**n, 0.0)

n = len(x) + len(h) - 1         # Tamanho do sinal de saída

y = np.convolve(x, h)        # Convolução

plt.subplot(3, 1, 1)
plt.stem(np.arange(0, len(x)), x)
plt.ylabel('x[n]')

plt.subplot(3, 1, 2)
plt.stem(np.arange(0, len(h)), h)
plt.ylabel('h[n]')

plt.subplot(3, 1, 3)
plt.stem(np.arange(0, len(y)), y)
plt.ylabel('y[n]')
plt.show()