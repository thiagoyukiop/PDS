import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parâmetros iniciais
G = 10          
V0 = 10**(G/20) 
H0 = V0 - 1     
fc = 10000       
Fs = 44100      

# Projetando filtro shelving passa-alta

if(G >= 0):
    aB_num = np.tan(np.pi * fc / Fs) - 1
    aB_den = np.tan(np.pi * fc / Fs) + 1
    aB = aB_num / aB_den
else:
    aB_num = np.tan(np.pi * fc / Fs) - V0
    aB_den = np.tan(np.pi * fc / Fs) + V0
    aB = aB_num / aB_den


# Construindo função de transferência H(z) do filtro shelving passa-alta

# Coeficientes do Numerador de Hz (a)
a0 = 1 + H0/2 - H0/2 * aB
a1 = aB * (1 + H0/2) - H0/2
a = np.array([a0, a1])

# Coeficientes do Denominador de Hz (b)
b0 = 1
b1 = aB
b = np.array([b0, b1])

# Cálculo da resposta em frequência
w, H = signal.freqz(a, b, worN=8192, fs=Fs)

# Plotar (Magnitude em dB)
m_db_LF = 20 * np.log10(np.abs(H))
f_hz_LF = w

# plt.subplot(2,1,1)
plt.semilogx(f_hz_LF, m_db_LF) # Eixo X logarítmico para frequência
plt.grid(which='both', axis='both')
plt.axvline(fc, color='r', linestyle='--', label=f'Corte {fc} Hz')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude (dB)')
plt.title(f'Resposta em Frequência (HF Shelving, G={G} dB)')
plt.show()

# Leitura do sinal de entrada (sweep)
input_path_sweep = "Avaliacao_M2/sinal_entrada/sweep_20_20k.pcm"
sinal = np.memmap(input_path_sweep, dtype='int16', mode='r')
sinal_aux = sinal.copy()
n = np.arange(0, len(sinal_aux))

# Visualização do sinal de entrada
plt.subplot(2, 1, 1)
plt.stem(n, sinal)
plt.title("Sinal de Entrada (Sweep)")
plt.grid(True)

# y1(n) = aB*x(n) + x(n-1) - aB*y1(n-1)
# y(n) = H0*[x(n) + y1(n)] + x(n)
# y(n) = H0*[x(n) + aB*x(n) + x(n-1) - aB*y1(n-1)] + x(n)

sinal_saida = np.zeros(len(sinal_aux))

x_1 = 0  # x(n-1)
y1_1 = 0 # y1(n-1)

for i in range(1, len(sinal_aux)):
    y1 = aB * sinal_aux[i] + x_1 - aB * y1_1
    sinal_saida[i] = H0/2 * (sinal_aux[i] - y1) + sinal_aux[i]
    x_1 = sinal_aux[i]
    y1_1 = y1

plt.subplot(2, 1, 2)
plt.stem(n, sinal_saida)
plt.title(f"Executando filtro Shelving Passa-Alta (G={G} dB)")
plt.grid(True)
plt.tight_layout()
plt.show()