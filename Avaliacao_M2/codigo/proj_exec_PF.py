import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parâmetros iniciais
G = 10          
V0 = 10**(G/20) 
H0 = V0 - 1     
fc = 5000
fb = 2000
Fs = 44100
d = -np.cos(2 * np.pi *fc / Fs)

# Projetando filtro peak passa-faixa
if(G >= 0):
    aB_num = np.tan(np.pi * fb / Fs) - 1
    aB_den = np.tan(np.pi * fb / Fs) + 1
    aB = aB_num / aB_den
else:
    aB_num = np.tan(np.pi * fb / Fs) - V0
    aB_den = np.tan(np.pi * fb / Fs) + V0
    aB = aB_num / aB_den

# Construindo função de transferência H(z) do filtro peak passa-faixa

# Coeficientes do Numerador de Hz (a)
a0 = 1 + H0/2 + H0/2*aB
a1 = (d - d*aB)
a2 = -aB - H0/2 * aB - H0/2
a = np.array([a0, a1, a2]) 

# Coeficientes do Denominador de Hz (b)
b0 = 1
b1 = (d - d*aB)
b2 = -aB
b = np.array([b0, b1, b2])

# Cálculo da resposta em frequência
w, H = signal.freqz(a, b, worN=8192, fs=Fs)

# Plotar (Magnitude em dB)
m_db_HF = 20 * np.log10(np.abs(H))
f_hz_HF = w

plt.plot(f_hz_HF, m_db_HF)
plt.grid(which='both', axis='both')
plt.axvline(fc, color='r', linestyle='--', label=f'Corte {fc} Hz')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude (dB)')
plt.title(f'Resposta em Frequência (HF Peak, G={G} dB)')
plt.show()

# ---------- Execução do filtro no sinal de entrada ----------

# Leitura do sinal de entrada (sweep)
input_path_sweep = "Avaliacao_M2/sinal_entrada/sweep_20_20k.pcm"
sinal = np.memmap(input_path_sweep, dtype='int16', mode='r')
sinal_aux = sinal.copy()
n = np.arange(0, len(sinal_aux))

# Visualização do sinal de entrada
plt.subplot(2, 1, 1)
plt.plot(n, sinal)
plt.title("Sinal de Entrada (Sweep)")
plt.grid(True)

# y1(n) = -aB*x(n) + d*(1-aB)*x(n - 1) + x*(n-2) - d*(1 - aB)*y1(n-1) + aB*y1(n-2)
# y(n) = H0/2*[x(n) - y1(n)] + x(n)
# y(n) = H0/2*[x(n) - (-aB*x(n) + d*(1-aB)*x*(n - 1) + x*(n-2) - d*(1 - aB)*y1(n-1) + aB*y1(n-2))] + x(n)

sinal_saida = np.zeros(len(sinal_aux))

x_1 = 0  # x(n-1)
x_2 = 0  # x(n-2)
y1_1 = 0 # y1(n-1)
y1_2 = 0 # y1(n-2)

for i in range(1, len(sinal_aux)):
    y1 = -aB * sinal_aux[i] + d * (1 - aB) * x_1 + x_2 - d * (1 - aB) * y1_1 + aB * y1_2
    sinal_saida[i] = H0/2 * (sinal_aux[i] - y1) + sinal_aux[i]
    x_2 = x_1
    x_1 = sinal_aux[i]
    y1_2 = y1_1
    y1_1 = y1

plt.subplot(2, 1, 2)
plt.plot(n, sinal_saida)
plt.title(f"Executando filtro Peak Passa-Faixa (G={G} dB)")
plt.grid(True)
plt.tight_layout()
plt.show()

