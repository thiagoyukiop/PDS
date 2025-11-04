import numpy as np
import matplotlib.pyplot as plt

# Carregando filtro FIR projetado
input_path = "Aula_10/sinal_saida/h_fir_pb_blackman_M100.txt"
h = np.loadtxt(input_path)
print(f"Tamanho de h: {len(h)}")

k = len(h)
aux = np.zeros(k - 1)

# Leitura do sinal de entrada
input_path_sweep = "Aula_10/sinal_entrada/seno_400Hz.pcm"
sinal = np.memmap(input_path_sweep, dtype='int16', mode='r')
sinal_aux = sinal.copy()
n = np.arange(0, len(sinal_aux))

# Visualização do sinal de entrada
plt.subplot(2, 1, 1)
plt.stem(n, sinal)
plt.title("Sinal de Entrada (seno 400Hz)")
plt.grid(True)

# Aplicação do filtro FIR ao sinal de entrada
sinal_saida = np.zeros(len(sinal_aux))

for i in range(len(sinal_aux)):
    janela = np.concatenate((aux, [sinal_aux[i]]))
    sinal_saida[i] = np.sum(janela * h[::-1])
    aux = np.roll(aux, -1)
    aux[-1] = sinal_aux[i]


# Visualização do sinal filtrado
plt.subplot(2, 1, 2)
plt.stem(n, sinal_saida)
plt.title(f"Sinal de Saída - Média Móvel de {k} elementos")
plt.grid(True)
plt.tight_layout()
plt.show()

# Salvando o sinal filtrado
output_file = "Aula_10/sinal_saida/out_seno_400Hz.pcm"
out = np.memmap(output_file, dtype='int16', mode='w+', shape=(len(sinal_saida),))
out[:] = sinal_saida[:]
