import numpy as np
import matplotlib.pyplot as plt

# a = 0.5

# w = np.arange(-np.pi, np.pi, np.pi/100)

# Num = 1
# Den = 1 - a * np.exp(-1j * w)
# X = Num / Den

w = np.linspace(-np.pi, np.pi, 1000)

# # Mesma coisa abaixo:
# X = np.exp(1j * w) + 1 + np.exp(-1j * w)
X = 1 + 2*np.cos(w)

Mod_X = np.abs(X)
Fase_X = np.angle(X)

plt.subplot(2, 1, 1)
plt.plot(w, Mod_X)
plt.title("Módulo de X")
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(w, Fase_X)
plt.title("Fase de X")
plt.grid(True)
plt.show()