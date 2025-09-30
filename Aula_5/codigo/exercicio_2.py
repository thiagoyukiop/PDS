# Exercício y(k) -1/4*y(k-1) 1/2*y(k-2) = x(k)
import numpy as np
import matplotlib.pyplot as plt

n = np.arange(-2, 9, 1)

x = np.where(n>=0, 1, 0.0)

y = np.zeros(len(n))

for k in range(len(n)):
    y_k_1 = y[k-1] if k-1 >= 0 else 0
    y_k_2 = y[k-2] if k-2 >= 0 else 0
    y[k] =  x[k] + 1/4*y_k_1 - 1/2*y_k_2

plt.subplot(2, 1, 1)
plt.stem(n, x)

plt.subplot(2, 1, 2)
plt.stem(n, y)
plt.show()