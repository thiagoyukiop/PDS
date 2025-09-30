import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

b = [0, 0, 1, 0.6]          # numerador correto
a = [1, 0.4, -0.4, 0.2]     # denominador

w, h = freqz(b, a, worN=512)

plt.figure(figsize=(10,5))
plt.subplot(2,1,1)
plt.plot(w/np.pi, 20*np.log10(np.abs(h)))
plt.title('Resposta em Frequência')
plt.ylabel('Magnitude (dB)')
plt.grid()

plt.subplot(2,1,2)
plt.plot(w/np.pi, np.angle(h))
plt.ylabel('Fase (rad)')
plt.xlabel('Frequência Normalizada (xπ rad/amostra)')
plt.grid()

plt.tight_layout()
plt.show()