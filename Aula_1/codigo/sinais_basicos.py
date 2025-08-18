import numpy as np
import matplotlib.pyplot as plt

Fs = 8000
f0 = 2000
Amplitude = 16384

# sinal impulso unitário
n = np.arange(-10, 11)

impulso = np.where(n == 0, Amplitude, 0.0)

# Plotando
plt.subplot(2, 2, 1)
plt.stem(n, impulso)
plt.title("Impulso Unitário (δ[n])")
plt.grid(True)
# plt.show()

# sinal degrau unitário
n = np.arange(-10, 11)

degrau = Amplitude * np.heaviside(n, 1)

# plotar o sinal degrau unitário
plt.subplot(2, 2, 2)
plt.stem(n, degrau)
plt.title("Sinal Degrau Unitário")
plt.grid(True)

# Sinal senoidal
senoidal = Amplitude * np.sin(2 * np.pi * 0.1 * n)

# Plotando como linha
plt.subplot(2, 2, 3)
plt.stem(n, senoidal)
plt.title("Sequência Sinosoidal ")
plt.grid(True)

# Sequência exponencial
sinal_exponencial = Amplitude * (0.8 ** n)

# Plotando com pontos (sequência discreta)
plt.subplot(2, 2, 4)
plt.stem(n, sinal_exponencial)
plt.title("Sequência Exponencial (alpha = 0.8))")
plt.grid(True)
plt.show()