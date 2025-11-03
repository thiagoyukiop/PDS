import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import signal

# H(s) = s/(s + wc)

## Variaveis
fc = 1000
passo = np.pi/1000
wc = 2*np.pi*fc
w = np.arange(0, np.pi, passo)
Fs = 8000
F = 2*Fs

# % Numerador e Denominador
num = [wc, -wc]
den = [F + wc, F - wc]

# Cálculo de Polos e Zeros (raízes de den e num)
polos = np.roots(den)
zeros = np.roots(num)
print('Polos: ', polos)
print('Zeros: ', zeros)
pts = polos + zeros

lim = max(1, max((abs(c) for c in pts), default=0)) * 1.5

ax = plt.gca()
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_aspect('equal')

ax.add_artist(plt.Circle((0, 0), 1, fill=False, linewidth=0.5))
ax.axhline(0, linewidth=0.5)
ax.axvline(0, linewidth=0.5)

# Plotagem do Diagrama de Polos e Zeros
ax.plot([c.real for c in polos], [c.imag for c in polos], 'xr')
ax.plot([c.real for c in zeros], [c.imag for c in zeros], 'or', mfc='none')
plt.xlabel('Re')
plt.ylabel('Im')
plt.show()

# Resposta em frequência
w, h = signal.freqz(num, den, fs=Fs)
plt.plot(w, 20 * np.log10(abs(h)))
plt.xlabel('Frequência (Hz)')
plt.ylabel('Atenuação (dB)')
plt.grid(True)
plt.show()

# Coeficientes da forma de diferença (normalizados)
a = wc / (F + wc)
a1 = -a
b = (F - wc) / (F + wc)

# Leitura do arquivo PCM
input_file = os.path.join("Aula_8/sinal_entrada", "sweep_20_3k4.pcm")
x = np.memmap(input_file, dtype=np.int16, mode='r').astype(np.float64)
y = np.zeros(len(x))

for n in range(len(x)):
    if n > 0:
        x_1 = x[n-1]
        y_1 = y[n-1]
    else:
        x_1 = 0
        y_1 = 0
    y[n] = a*x[n] + a1*x_1 - b*y_1

out = np.memmap('out_sweep_20_3k4_PA.pcm', dtype='int16', mode='w+', shape=x.shape)
out[:] = y[:]
out.flush()

plt.xlabel('k')
plt.ylabel('y')
plt.stem(y)
plt.show()