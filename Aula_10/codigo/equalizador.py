import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# importar os Passa-Baixa, Passa-Faixa e Passa-Alta

# ---- Equalizador ----
# Ganhos para cada faixa (em linear, 1 = sem alteração)
gain_PB = 1.5   # realça graves
gain_PF = 1.0   # médios neutros
gain_PA = 0.7   # reduz agudos

# Combina as bandas ponderadas
h_equalizador = gain_PB * PB + gain_PF * PF + gain_PA * PA

# Normaliza
h_equalizador /= np.sum(np.abs(h_equalizador))

# ---- Resposta em frequência ----
w, H = signal.freqz(h_equalizador, 1, fs=Fs)
H_db = 20 * np.log10(np.abs(H))


plt.plot(w, H_db)
plt.title("Resposta em Frequência - Equalizador 3 Bandas")
plt.xlabel("Frequência (Hz)")
plt.ylabel("Ganho (dB)")
plt.grid(True)
plt.show()