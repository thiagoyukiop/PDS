import numpy as np
import matplotlib.pyplot as plt

M = 100
n = np.arange(M)
hamming = 0.54 - 0.46 * np.cos(2*np.pi*n/M)
blackman = 0.42 - 0.5*np.cos(2*np.pi*n/M) + 0.08*np.cos(4*np.pi*n/M)

plt.plot(n, hamming, label="Hamming")
plt.plot(n, blackman, label="Blackman")
plt.legend()
plt.title("Janelas de Hamming e Blackman")
plt.show()
