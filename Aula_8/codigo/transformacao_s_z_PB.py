import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import signal
# F = 2*Fs

# Y(z) = wc + wc*z^-1
# X(z) = (F + wc) + (wc - F)*z^-1
# H(z) = Y(z)/X(z)

## Variaveis
fc = 1000
passo = np.pi/1000
wc = 2*np.pi*fc
#w = 0:passo:pi;
w = np.arange(0, np.pi, passo)
Fs = 8000
F = 2*Fs

# % Numerador e Denominador
num = [wc, wc]
den = [F + wc, wc - F]

polos = np.roots(den)
zeros = np.roots(num)
print('Polos: ', polos)
print('Zeros: ', zeros)
# Zeros (bolinhas) e Polos (x)
pts = polos + zeros

# limite baseado na maior magnitude (garante visual do círculo unitário)
lim = max(1, max((abs(c) for c in pts), default=0)) * 1.5

ax = plt.gca()
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_aspect('equal')

ax.add_artist(plt.Circle((0, 0), 1, fill=False, linewidth=0.5))
ax.axhline(0, linewidth=0.5)
ax.axvline(0, linewidth=0.5)

ax.plot([c.real for c in polos], [c.imag for c in polos], 'xr')
ax.plot([c.real for c in zeros], [c.imag for c in zeros], 'or', mfc='none')
plt.xlabel('Re')
plt.ylabel('Im')
plt.show()

w, h = signal.freqz(num, den, fs=Fs)
plt.plot(w, 20 * np.log10(abs(h)))
plt.xlabel('Frequência (Hz)')
plt.ylabel('Atenuação (dB)')
plt.grid(True)
plt.show()

# ler sweep (int16)
input_file = os.path.join("Aula_8/sinal_entrada", "sweep_20_3k4.pcm")
x = np.memmap(input_file, dtype=np.int16, mode='r').astype(np.float64)

y = np.zeros(len(x))

# y[n] = a*x[n] + a*x[n-1] - b*y[n-1]
# onde a = wc/(F+wc) e b = (wc-F)/(F+wc)

a = wc / (F + wc)
b = (wc - F) / (F + wc)

for tam in range(len(x)):
    if tam > 0:
        x_1 = x[tam-1]
        y_1 = y[tam-1]
    else:
        x_1 = 0
        y_1 = 0
    y[tam] = a*x[tam] + a*x_1 - b*y_1

out = np.memmap('out_sweep_20_3k4_PB.pcm', dtype='int16', mode='w+', shape=x.shape)
out[:] = y[:]
out.flush()

plt.xlabel('k')
plt.ylabel('y')
plt.stem(y)
plt.show()