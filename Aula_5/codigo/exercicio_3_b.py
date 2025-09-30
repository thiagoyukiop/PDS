# y[n] = x[n] - x[n-1] + 0,95*y[n-1]
# x[n] = u[n]
import numpy as np
import matplotlib.pyplot as plt

n = np.arange(0, 5, 1)
x = np.where(n>=0, 1, 0.0)
y = np.zeros(len(n))

for k in range(len(n)):
    x_k_1 = x[k-1] if k-1 >= 0 else 0
    y_k_1 = y[k-1] if k-1 >= 0 else 0
    y[k] =  x[k] - x_k_1 + 0.95*y_k_1

plt.subplot(2, 1, 1)
plt.stem(n, x)
plt.ylabel('x[n]')
plt.subplot(2, 1, 2)
plt.stem(n, y)
plt.ylabel('y[n]')
plt.show()