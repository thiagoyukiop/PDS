import numpy as np
import matplotlib.pyplot as plt

# Carregando o filtro PA
input_path = "Aula_10/sinal_saida/h_fir_pa.txt"
h = np.loadtxt(input_path)
print(f"Tamanho de h: {len(h)}")

k = len(h)
aux = np.zeros(k - 1)

# Leitura do sinal de entrada (sweep)
input_path_sweep = "Aula_10/sinal_entrada/sweep_20_3k4.pcm"
sinal = np.memmap(input_path_sweep, dtype='int16', mode='r')
sinal_aux = sinal.copy()
n = np.arange(0, len(sinal_aux))

# Visualização do sinal de entrada
plt.subplot(2, 1, 1)
plt.stem(n, sinal)
plt.title("Sinal de Entrada (Sweep)")
plt.grid(True)

# Aplicação do filtro FIR
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
output_file = "Aula_10/sinal_saida/out_sweep_20_3k4_PA.pcm"
out = np.memmap(output_file, dtype='int16', mode='w+', shape=(len(sinal_saida),))
out[:] = sinal_saida[:]
