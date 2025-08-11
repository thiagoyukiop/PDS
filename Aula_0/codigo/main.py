# Importar bibliotecas necessárias
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import Tk, filedialog

print("Iniciando o processamento de áudio...")

# Configurar a janela Tkinter (não será exibida)
root = Tk()      # Criar a janela principal
root.withdraw()  # Esconder a janela principal

# Abrir diálogo para seleção do arquivo
print("Selecione o arquivo PCM de entrada...")
input_file = filedialog.askopenfilename(
    title="Selecione o arquivo PCM",
    filetypes=(("Arquivos PCM", "*.pcm"), ("Todos os arquivos", "*.*"))
)

# Verificar se o usuário cancelou a seleção
if not input_file:
    print("Nenhum arquivo selecionado. Processamento cancelado.")
    exit()

# Ler o arquivo binário de entrada de áudio PCM
with open(input_file, "rb") as f:
    samples = np.frombuffer(f.read(), dtype=np.int16)

itera = len(samples)

# Plotar o sinal do áudio de entrada
print("Plotando o sinal do áudio de entrada...")
plt.subplot(2, 1, 1)
plt.plot(samples)
plt.xlabel("Número de Amostras")
plt.ylabel("Amplitude da Entrada")
plt.grid(True)
plt.title("Sinal de Áudio de Entrada")

# Criar vetor para salvar valores do áudio da saída
saida = np.zeros(itera, dtype=np.int16)

# Pedir para o usuário digitar o valor do ganho
while True:
    try:
        ganho = float(input("Digite o valor do ganho: "))
        break
    except ValueError:
        print("Valor inválido! Digite um número (ex: 0.5, 1, 2, etc.)")

print(f"Processando áudio com ganho = {ganho}...")

# Processar o áudio com ganho
print("Processando o áudio com ganho...")
for i in range(itera):
    x = samples[i]
    y = x * ganho
    y = np.clip(y, -32768, 32767)  # Limitar o valor para evitar overflow
    saida[i] = y

# Plotar o sinal do áudio de saída
print("Plotando o sinal do áudio de saída...")
plt.subplot(2, 1, 2)
plt.plot(saida, "r")
plt.title("Sinal de Áudio de Saída")
plt.xlabel("Número de Amostras")
plt.ylabel("Amplitude da Saída")
plt.grid(True)
plt.tight_layout()
plt.show()

# Criar pasta de saída se não existir
output_dir = "audio_processado"
os.makedirs(output_dir, exist_ok=True)

# Gerar nome do arquivo de saída
base_name = os.path.basename(input_file)  # Pega apenas o nome do arquivo, sem caminho
output_file = os.path.join(output_dir, f"{os.path.splitext(base_name)[0]}_ganho{ganho}.pcm")

# Salvar o áudio processado em um novo arquivo PCM
with open(output_file, "wb") as f:
    saida.tofile(f)

print(f"Processamento concluído. Arquivo de saída salvo como: {output_file}")