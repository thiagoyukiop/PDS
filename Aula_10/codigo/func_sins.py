import numpy as np
import matplotlib.pyplot as plt

n = np.arange(-50, 51)
fc = 0.1
h = np.sinc(2 * fc * n)
plt.plot(n, h)
plt.title("Função Sinc")
plt.show()
