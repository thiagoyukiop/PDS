import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import freqz

fc = 1000
Fs = 8000
F = 2*Fs
wc = 2*np.pi*fc
passo = np.pi/1000
w = np.arange(0, np.pi, passo)

# y[n] = 0.282*x[n] + 0.282*x[n-1] - (-0.4361)*y[n-1] 
# H(z) = Y(z)/X(z) = (0.282 + 0.282*z^-1) / (1 + 0.4361*z^-1)
num = [0.282, 0.282]
den = [1, 0.4361]

polos = np.roots(den)
zeros = np.roots(num)

# --- Plot polos e zeros ---
plt.figure(figsize=(6,6))
# círculo unitário
theta = np.linspace(0, 2*np.pi, 400)
plt.plot(np.cos(theta), np.sin(theta), 'k--')

# eixos
plt.axhline(0, color='gray')
plt.axvline(0, color='gray')

# Zeros (bolinhas) e Polos (x)
plt.plot(np.real(zeros), np.imag(zeros), 'ob', markersize=10, label='Zeros')
plt.plot(np.real(polos), np.imag(polos), 'xr', markersize=10, label='Polos')

plt.title('Polos e Zeros no Plano-z')
plt.xlabel('Parte Real')
plt.ylabel('Parte Imaginária')
plt.axis('equal')
plt.legend()
plt.grid(True)
plt.show()