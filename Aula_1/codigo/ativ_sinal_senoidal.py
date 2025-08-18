import numpy as np
import matplotlib.pyplot as plt
import os

Fs = 8000
f0 = 2000
Amplitude = 16384

t = np.linspace(0, 0.1, Fs)

# sinal senoidal
sinal = Amplitude * np.sin(2 * np.pi * f0 * t)

# plotar o sinal senoidal
plt.subplot(2, 1, 1)
plt.plot(t, sinal)
plt.title("Sinal Senoidal")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.grid(True)

amostras = (0.1*Fs)-1
print(f"Número de amostras: {amostras}")
t_amostras = np.linspace(0, 0.1, int(amostras))  
sinal_amostras = Amplitude * np.sin(2 * np.pi * f0 * t_amostras)

# Plotar apenas os pontos
plt.subplot(2, 1, 2)
plt.stem(t_amostras, sinal_amostras)
plt.title("Pontos da Senoide (stem)")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.tight_layout()
plt.show()

output_file = os.path.join("Aula_1/saida/", f"sinal_{f0}_Hz.pcm")

out = np.memmap(output_file, dtype='int16', mode='w+', shape=(len(sinal_amostras),))
out[:] = sinal_amostras[:]

# # Criar pasta de saída se não existir
# output_dir = "Aula_1/saida"
# os.makedirs(output_dir, exist_ok=True)
# output_file = os.path.join(output_dir, f"sinal_senoidal_saida.pcm")

# # Salvar o áudio processado em um novo arquivo PCM
# with open(output_file, "wb") as f:
#     sinal_amostras.tofile(f)

# print(f"Processamento concluído. Arquivo de saída salvo como: {output_file}")


