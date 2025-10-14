import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import signal

# -----------------------
# Coeficientes (H(z) = Y(z)/X(z))
# Y(z) = 0.7294 - 2.1883*z^-1 + 2.1883*z^-2 - 0.7294*z^-3
# X(z) = 1 - 2.3741*z^-1 + 1.9294*z^-2 - 0.5321*z^-3
# -----------------------
Fs = 8000
passo = np.pi / 1000
w = np.arange(0, np.pi, passo)
F = 2 * Fs

num = [0.7294, -2.1883, 2.1883, -0.7294]
den = [1, -2.3741, 1.9294, -0.5321]

# -----------------------
# A) Determinar polos e zeros (plano z)
# -----------------------
polos = np.roots(den)
zeros = np.roots(num)

# limites do gráfico baseado na maior magnitude (garante visual do círculo unitário)
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
ax.plot([c.real for c in polos], [c.imag for c in polos], 'xr')
ax.plot([c.real for c in zeros], [c.imag for c in zeros], 'or', mfc='none')

plt.xlabel('Re')
plt.ylabel('Im')
plt.title('Polos e Zeros')
plt.show()

# -----------------------
# B) Verificar estabilidade
# -----------------------
if all(abs(p) < 1 for p in polos):
    print("O sistema é estável.")
else:
    print("O sistema não é estável.")

# -----------------------
# C) Resposta em frequência (dB)
# -----------------------
w_freq, h = signal.freqz(num, den, fs=Fs)
plt.plot(w_freq, 20 * np.log10(np.abs(h)))
plt.xlabel('Frequência (Hz)')
plt.ylabel('Atenuação (dB)')
plt.grid(True)
plt.title('Resposta em frequência (dB)')
plt.show()

# -----------------------
# D) Equação em diferença (comentada no código original)
# y[n] - 2.3741*y[n-1] + 1.9294*y[n-2] - 0.5321*y[n-3] =
#     0.7294*x[n] - 2.1883*x[n-1] + 2.1883*x[n-2] - 0.7294*x[n-3]
# -----------------------

# -----------------------
# E) Gerar no ocean um sweep de 20Hz a 3k4Hz, e avaliar a saída y[n]
# (processamento do sweep com a equação em diferença — implementação inline)
# -----------------------
input_file = os.path.join("teste_07_10", "sinal_entrada", "sweep_20_3k4Hz.pcm")
x = np.memmap(input_file, dtype=np.int16, mode='r').astype(np.float64)

y = np.zeros(len(x), dtype=np.float64)

a = num
b = den

# y[n] = a0*x[n] + a1*x[n-1] + a2*x[n-2] + a3*x[n-3]
#      - b1*y[n-1] - b2*y[n-2] - b3*y[n-3]
for n in range(len(x)):
    y[n] = 0.0
    for i in range(len(a)):
        if n - i >= 0:
            y[n] += a[i] * x[n - i]
    for j in range(1, len(b)):
        if n - j >= 0:
            y[n] -= b[j] * y[n - j]

# gravação segura em int16 (clipping)
output_file = os.path.join("teste_07_10", "sinal_saida", "out_sweep_20_3k4Hz.pcm")
os.makedirs(os.path.dirname(output_file), exist_ok=True)
y_int16 = np.clip(np.round(y), np.iinfo(np.int16).min, np.iinfo(np.int16).max).astype(np.int16)
out = np.memmap(output_file, dtype='int16', mode='w+', shape=x.shape)
out[:] = y_int16
out.flush()

# plot do resultado do sweep
plt.xlabel('k')
plt.ylabel('y[n]')
plt.stem(y)
plt.show()

# -----------------------
# F) Aplicar senos f1=100Hz e f2=1kHz e calcular saída
# -----------------------
# seno 100 Hz
input_file_seno_100 = os.path.join("teste_07_10", "sinal_entrada", "sweep_seno_100Hz.pcm")
seno_100 = np.memmap(input_file_seno_100, dtype=np.int16, mode='r').astype(np.float64)
y_100 = np.zeros(len(seno_100), dtype=np.float64)

plt.subplot(2, 1, 1)
plt.xlabel('k')
plt.ylabel('x (100 Hz)')
plt.stem(seno_100)

for n in range(len(seno_100)):
    y_100[n] = 0.0
    for i in range(len(a)):
        if n - i >= 0:
            y_100[n] += a[i] * seno_100[n - i]
    for j in range(1, len(b)):
        if n - j >= 0:
            y_100[n] -= b[j] * y_100[n - j]

plt.subplot(2, 1, 2)
plt.xlabel('k')
plt.ylabel('y (100 Hz)')
plt.stem(y_100)
plt.tight_layout()
plt.show()

# seno 1 kHz
input_file_seno_1k = os.path.join("teste_07_10", "sinal_entrada", "sweep_seno_1kHz.pcm")
seno_1k = np.memmap(input_file_seno_1k, dtype=np.int16, mode='r').astype(np.float64)
y_1k = np.zeros(len(seno_1k), dtype=np.float64)

plt.subplot(2, 1, 1)
plt.xlabel('k')
plt.ylabel('x (1 kHz)')
plt.stem(seno_1k)

for n in range(len(seno_1k)):
    y_1k[n] = 0.0
    for i in range(len(a)):
        if n - i >= 0:
            y_1k[n] += a[i] * seno_1k[n - i]
    for j in range(1, len(b)):
        if n - j >= 0:
            y_1k[n] -= b[j] * y_1k[n - j]

plt.subplot(2, 1, 2)
plt.xlabel('k')
plt.ylabel('y (1 kHz)')
plt.stem(y_1k)
plt.tight_layout()
plt.show()

# -----------------------
# Soma dos senos (entrada) -> avaliar saída e salvar
# -----------------------
soma_seno = seno_100 + seno_1k
y_soma = np.zeros(len(soma_seno), dtype=np.float64)

# salvar a entrada soma dos senos (seguro)
output_file_soma_entrada = os.path.join("teste_07_10", "sinal_entrada", "sweep_soma_senos_entrada.pcm")
os.makedirs(os.path.dirname(output_file_soma_entrada), exist_ok=True)
out_soma_senos_entrada = np.memmap(output_file_soma_entrada, dtype='int16', mode='w+', shape=soma_seno.shape)
out_soma_senos_entrada[:] = np.clip(np.round(soma_seno), np.iinfo(np.int16).min, np.iinfo(np.int16).max).astype(np.int16)
out_soma_senos_entrada.flush()

plt.subplot(2, 1, 1)
plt.xlabel('k')
plt.ylabel('x (soma)')
plt.stem(soma_seno)

for n in range(len(soma_seno)):
    y_soma[n] = 0.0
    for i in range(len(a)):
        if n - i >= 0:
            y_soma[n] += a[i] * soma_seno[n - i]
    for j in range(1, len(b)):
        if n - j >= 0:
            y_soma[n] -= b[j] * y_soma[n - j]

plt.subplot(2, 1, 2)
plt.xlabel('k')
plt.ylabel('y_soma')
plt.stem(y_soma)
plt.tight_layout()
plt.show()

# salvar saída y_soma (seguro)
output_file_soma_saida = os.path.join("teste_07_10", "sinal_saida", "out_sweep_soma_senos.pcm")
os.makedirs(os.path.dirname(output_file_soma_saida), exist_ok=True)
out_soma_senos = np.memmap(output_file_soma_saida, dtype='int16', mode='w+', shape=y_soma.shape)
out_soma_senos[:] = np.clip(np.round(y_soma), np.iinfo(np.int16).min, np.iinfo(np.int16).max).astype(np.int16)
out_soma_senos.flush()
