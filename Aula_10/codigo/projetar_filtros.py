import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parâmetros iniciais
fc1_Hz = 200
fc2_Hz = 400
Fs = 8000
# fc = fc_Hz / Fs
fc1 = fc1_Hz / Fs
fc2 = fc2_Hz / Fs
M = 200

# Projeto do filtro Passa-Baixa
n_PB = np.arange(M + 1)
center = M / 2
h_ideal_PB = np.sinc(2 * fc1 * (n_PB - center))

hamming = 0.54 - 0.46 * np.cos(2 * np.pi * n_PB / M)
h_PB = h_ideal_PB * hamming

h_PB = h_PB / np.sum(h_PB)

PB = h_PB

# Projeto do filtro Passa-Alta
n_PA = np.arange(M + 1)
center = M / 2
h_ideal_PA = np.sinc(2 * fc2 * (n_PA - center))

hamming = 0.54 - 0.46 * np.cos(2 * np.pi * n_PA / M)
h_PA = h_ideal_PA * hamming

h_PA = h_PA / np.sum(h_PA)

h_saida_PA = -h_PA
h_saida_PA[int(center)] += 1

PA = h_saida_PA

# Derivação dos filtros Rejeita-Faixa(RF) e Passa-Faixa(PF)
RF = PA + PB

PF = -RF
PF[int(center)] += 1

# Plotagem das respostas ao impulso
plt.subplot(2,2,1)
plt.stem(PB)
plt.xlabel('n')
plt.ylabel('h[n]')
plt.title('Filtro FIR Passa-Baixa')
# plt.show()

plt.subplot(2,2,2)
plt.stem(PA)
plt.xlabel('n')
plt.ylabel('h[n]')
plt.title('Filtro FIR Passa-Alta')

plt.subplot(2,2,3)
plt.stem(RF)
plt.xlabel('n')
plt.ylabel('h[n]')
plt.title('Filtro FIR Rejeita-Faixa')

plt.subplot(2,2,4)
plt.stem(PF)
plt.xlabel('n')
plt.ylabel('h[n]')
plt.title('Filtro FIR Passa-Faixa')
plt.show()

# Cálculo e plotagem das respostas em frequência
plt.subplot(2,2,1)
w, H = signal.freqz(PB, 1, fs=Fs)
H_db = 20 * np.log10(np.abs(H)) 
plt.plot(w, H_db)
plt.xlabel('Frequência (Hz)')
plt.ylabel('Atenuação (dB)')
plt.grid(True)
plt.title('Resposta em frequência do filtro FIR Passa-Baixa')
plt.ylim(-120, 10)
plt.xlim(0, Fs/2)
# plt.show()

plt.subplot(2,2,2)
w, H = signal.freqz(PA, 1, fs=Fs)
H_db = 20 * np.log10(np.abs(H)) 
plt.plot(w, H_db)
plt.xlabel('Frequência (Hz)')
plt.ylabel('Atenuação (dB)')
plt.grid(True)
plt.title('Resposta em frequência do filtro FIR Passa-Alta')
plt.ylim(-120, 10)
plt.xlim(0, Fs/2)

plt.subplot(2,2,3)
w, H = signal.freqz(RF, 1, fs=Fs)
H_db = 20 * np.log10(np.abs(H)) 
plt.plot(w, H_db)
plt.xlabel('Frequência (Hz)')
plt.ylabel('Atenuação (dB)')
plt.grid(True)
plt.title('Resposta em frequência do filtro FIR Rejeita-Faixa')
plt.ylim(-120, 10)
plt.xlim(0, Fs/2)

plt.subplot(2,2,4)
w, H = signal.freqz(PF, 1, fs=Fs)
H_db = 20 * np.log10(np.abs(H)) 
plt.plot(w, H_db)
plt.xlabel('Frequência (Hz)')
plt.ylabel('Atenuação (dB)')
plt.grid(True)
plt.title('Resposta em frequência do filtro FIR Passa-Faixa')
plt.ylim(-120, 10)
plt.xlim(0, Fs/2)
plt.show()