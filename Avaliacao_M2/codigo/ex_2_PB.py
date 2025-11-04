import numpy as np
import matplotlib.pyplot as plt

# Parâmetros iniciais
G = 10          
V0 = 10**(G/20) 
H0 = V0 - 1     
fc = 1000       
Fs = 44100 

if(G >= 0):
    aB_num = np.tan(np.pi * fc / Fs) - 1
    aB_den = np.tan(np.pi * fc / Fs) + 1
    aB = aB_num / aB_den
else:
    aB_num = np.tan(np.pi * fc / Fs) - V0
    aB_den = np.tan(np.pi * fc / Fs) + V0
    aB = aB_num / aB_den

# Leitura do sinal de entrada (sweep)
input_path_sweep = "Aula_10/sinal_entrada/sweep_20_3k4.pcm"
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
    sinal_saida[i] = H0 * (sinal_aux[i] + y1) + sinal_aux[i]
    x_1 = sinal_aux[i]
    y1_1 = y1

plt.subplot(2, 1, 2)
plt.stem(n, sinal_saida)
plt.title(f"Executando filtro Shelving Passa-Baixa (G={G} dB)")
plt.grid(True)
plt.tight_layout()
plt.show()