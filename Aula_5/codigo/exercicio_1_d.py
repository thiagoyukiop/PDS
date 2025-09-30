# y[n] = a0*x[n] + a1*y[n-9]
import numpy as np
import matplotlib.pyplot as plt

n = np.arange(0, 101, 1)

a0 = 1

a1 = 1

x = np.where(n ==0, 1, 0.0)

y = np.zeros(len(n))

for k in range(len(n)):
    x_k_9 = x[k-9] if k-9 >= 0 else 0
    y_k_9 = y[k-9] if k-9 >= 0 else 0
    y[k] =  a0*x[k] + a1*y_k_9

plt.subplot(2, 1, 1)
plt.stem(n, x)
plt.ylabel('x[n]')
plt.subplot(2, 1, 2)
plt.stem(n, y)
plt.ylabel('y[n]')
plt.show()