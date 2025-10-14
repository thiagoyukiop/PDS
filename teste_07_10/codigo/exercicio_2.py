# Projetar um filtro Passa Alta de 1º ordem com fc = 400Hz e Fs = 8kHz

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# -----------------------
# Parâmetros
# -----------------------
fc = 400          # frequência de corte (Hz)
Fs = 8000         # frequência de amostragem (Hz)
F = 2 * Fs
wc = 2 * np.pi * fc

# sweep de frequência para plots (não altera o filtro)
passo = np.pi / 1000
w = np.arange(0, np.pi, passo)

# -----------------------
# Coeficientes do filtro (numerador e denominador em z)
# -----------------------
# mantendo a mesma forma que você usou originalmente:
num = [F, -F]                       # numerador (zeros)
den = [F + wc, wc - F]              # denominador (polos)

# -----------------------
# Plot polos e zeros (plano z)
# -----------------------
polos = np.roots(den)
zeros = np.roots(num)

# determina limites do gráfico com base nas magnitudes
pts = polos + zeros
lim = max(1, max((abs(c) for c in pts), default=0)) * 1.5

ax = plt.gca()
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_aspect('equal')

# círculo unitário e eixos
ax.add_artist(plt.Circle((0, 0), 1, fill=False, linewidth=0.5))
ax.axhline(0, linewidth=0.5)
ax.axvline(0, linewidth=0.5)

# marcar polos (x) e zeros (o sem preenchimento)
ax.plot([p.real for p in polos], [p.imag for p in polos], 'xr')
ax.plot([z.real for z in zeros], [z.imag for z in zeros], 'or', mfc='none')

plt.xlabel('Re')
plt.ylabel('Im')
plt.title('Polos e Zeros')
plt.show()

# -----------------------
# Resposta em frequência (em dB)
# -----------------------
w_freq, h = signal.freqz(num, den, fs=Fs)
plt.plot(w_freq, 20 * np.log10(np.abs(h)))
plt.xlabel('Frequência (Hz)')
plt.ylabel('Atenuação (dB)')
plt.grid(True)
plt.title('Resposta em frequência (dB)')
plt.show()

# -----------------------
# Equação em diferença — processamento do sweep (implementação inline)
# -----------------------
# coeficientes usados na equação em diferença (mesma fórmula do código anterior)
a = F / (F + wc)
a1 = -a
b = (wc - F) / (F + wc)

# arquivos de entrada/saída (mesmos nomes que você vinha usando)
input_file = os.path.join("teste_07_10", "sinal_entrada", "sweep_20_3k4Hz.pcm")
output_file = os.path.join("teste_07_10", "sinal_saida", "out_sweep_20_3k4Hz_PA.pcm")

# lê sweep (int16) e converte para float64 para processamento
x = np.memmap(input_file, dtype=np.int16, mode='r').astype(np.float64)

# plot sinal de entrada (sub-plot 1)
plt.subplot(2, 1, 1)
plt.xlabel('k')
plt.ylabel('x[n]')
plt.stem(x)

# prepara vetor de saída
y = np.zeros_like(x, dtype=np.float64)

# processamento amostra-a-amostra (equação em diferença)
for n in range(len(x)):
    if n > 0:
        x_prev = x[n - 1]
        y_prev = y[n - 1]
    else:
        x_prev = 0.0
        y_prev = 0.0

    # y[n] = a*x[n] + a1*x[n-1] - b*y[n-1]
    y[n] = a * x[n] + a1 * x_prev - b * y_prev

# garante diretório de saída
os.makedirs(os.path.dirname(output_file), exist_ok=True)

out = np.memmap(output_file, dtype='int16', mode='w+', shape=x.shape)
out[:] = y[:]
out.flush()

# plot sinal de saída (sub-plot 2)
plt.subplot(2, 1, 2)
plt.xlabel('k')
plt.ylabel('y[n]')
plt.stem(y)
plt.tight_layout()
plt.show()
