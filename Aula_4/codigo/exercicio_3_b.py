# Exercício y(k) = 0.2*x(k) + 0.3*x(k-1) + 0.3*x(k-2) + 0.2*x(k-3)
import numpy as np
import matplotlib.pyplot as plt

n = np.arange(-2, 9, 1)

x = np.where(n>=0, 1, 0.0)

y = np.zeros(len(n))

for k in range(len(n)):
    x_k_1 = x[k-1] if k-1 >= 0 else 0
    x_k_2 = x[k-2] if k-2 >= 0 else 0
    x_k_3 = x[k-3] if k-3 >= 0 else 0
    y[k] =  0.2*x[k] + 0.3*x_k_1 + 0.3*x_k_2 + 0.2*x_k_3

plt.subplot(2, 1, 1)
plt.stem(n, x)
plt.ylabel('x[n]')

plt.subplot(2, 1, 2)
plt.stem(n, y)
plt.ylabel('y[n]')
plt.show()