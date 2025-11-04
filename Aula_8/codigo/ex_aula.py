import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import freqz

# Y(z) = 0.0.985 + 0.2956*z^-1 + 0.2956*z^-2 + 0.0985*z^-3
# X(z) = 1 - 0.577*z^-1 + 0.4218*z^-2 - 0.0563*z^-3
# H(z) = Y(z)/X(z)

## Variaveis
passo = np.pi/1000
#w = 0:passo:pi;
w = np.arange(0, np.pi, passo)
L = 8
Fs = 8000

# % Numerador e Denominador
num = [0.985, 0.2956, 0.2956, 0.0985]
den = [1, -0.577, 0.4218, -0.0563]

[w, h] = freqz(num, den, worN=Fs, fs=Fs)

# Plotando a frequencia em Rad
X = np.abs(h)

plt.figure(figsize = (12, 12))
plt.plot(w, 20 * np.log10(abs(h)), 'b')

plt.title('Magnitude da resposta em frequencia')
plt.grid()
plt.show()