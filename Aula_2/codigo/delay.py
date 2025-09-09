# import numpy as np
# import matplotlib.pyplot as plt

# Fs = 8000
# Ts = 1 / Fs
# n1 = 10
# n2 = 15
# Amplitude = 16384

# # sinal impulso unitário
# n = np.arange(0, int(Fs+1))

# impulso = np.where(n == 0, Amplitude, 0.0)

# a0, a1, a2 = 0.5, 0.3, 0.2
# n1, n2 = 3000, 6000

# eco = a0*impulso + a1*np.roll(impulso, n1) + a2*np.roll(impulso, n2)

# # Plotando
# plt.stem(n, eco)
# plt.title("Eco de um Impulso Unitário (δ[n])")
# plt.grid(True)
# plt.show()

# out = np.memmap("Aula_2/sinal_saida/eco.pcm", dtype='int16', mode='w+', shape=(len(eco),))
# out[:] = eco[:]

import numpy as np
import matplotlib.pyplot as plt

# Definições iniciais
Fs = 8000                       # Frequência de amostragem
t1 = 1.0 * 10**-3               # 1ms
t2 = 1.5 * 10**-3               # 1.5ms
n1 = int(t1 * Fs)               # atraso 1 -> 8 amostras
n2 = int(t2 * Fs)               # atraso 2 -> 12 amostras

# Definição dos ganhos
a0 = 0.5
a1 = 0.3
a2 = 0.2

# Define o tamanho do maior delay
tama_delay = n2

# Vetor para armazenar os delays
vetor_delay = np.zeros((tama_delay, 1))

# Definindo a entrada (impulso unitário)
entrada = np.zeros((2 * tama_delay, 1))
entrada[0, 0] = 1  # impulso em n=0

# Configurações do loop
tama_loop = len(entrada)
vet_saida = np.zeros((tama_loop, 1))

# Loop principal para calcular a saída
for j in range(tama_loop):
    # Captura a entrada atual
    input_val = entrada[j, 0]

    # Armazena no buffer de delay
    vetor_delay[0, 0] = input_val

    # Calcula a saída com base nos ganhos e atrasos
    y = (a0 * vetor_delay[0, 0] +
         a1 * vetor_delay[n1-1, 0] +
         a2 * vetor_delay[n2-1, 0])

    # Atualiza o vetor de delay (desloca uma posição para baixo)
    vetor_delay[1:, 0] = vetor_delay[:-1, 0]

    # Armazena a saída
    vet_saida[j, 0] = y

# Plota o resultado
plt.figure(figsize=(8, 4))
plt.stem(vet_saida)
plt.title("Teste Delay")
plt.xlabel("n")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

out = np.memmap("Aula_2/sinal_saida/delay.pcm", dtype='int16', mode='w+', shape=(len(vet_saida),))
out[:] = y[:]
