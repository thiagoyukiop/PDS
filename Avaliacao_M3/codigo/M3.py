import numpy as np
import matplotlib.pyplot as plt
import os

# Parâmetros
N_AMOSTRAS = 8000  # Número total de amostras
Fs = 8000        # Frequência de amostragem (Hz)
F_Senoide = 100
PASSO_APRENDIZADO = 0.005  # Coeficiente de taxa de aprendizado (mu)
ORDEM_FILTRO = 5  # Número de coeficientes do filtro adaptativo
N_EPOCHS = 10    # Número de épocas para o treinamento do filtro

# --- Geração de Sinais ---

# 1. Sinal puro (d[n]): Senoide de baixa frequência (o que queremos preservar)
t = np.arange(N_AMOSTRAS) / Fs
d = np.sin(2 * np.pi * F_Senoide * t)

# 2. Ruído de Referência (x[n]): Ruído branco gaussiano (o ruído que tentaremos cancelar)

POWER_DB = -8
VAR_RUIDO = 10**(POWER_DB / 10)
np.random.seed(42)
x = np.sqrt(VAR_RUIDO) * np.random.randn(N_AMOSTRAS)

# 3. Caminho do Ruído (simulado pelo "Noise Path Filter")
r = 1.2*x.copy()

# 4. Sinal Contaminado (s[n]): Sinal puro + Ruído filtrado
s = d + r

w = np.zeros(ORDEM_FILTRO)
e_final = np.zeros(N_AMOSTRAS) # Sinal de erro final (e[n])

# Buffer de entrada para as amostras x[n]
x_buffer = np.zeros(ORDEM_FILTRO)

# Vetor para plotar a função custo (opcional)
energy_error = np.zeros(N_EPOCHS)

# --- Loop Principal LMS com EPOCHS (Convergência Forçada) ---

for epoch in range(N_EPOCHS):
    int_error_sq = 0 # Erro intermediário (acumulador de energia)
    
    # O loop LMS é executado para TODAS as amostras N a cada época
    for i in range(ORDEM_FILTRO, N_AMOSTRAS):
        # 1. Desloca o buffer de entrada x_buffer 
        # (usamos i:i - M:-1 para obter o vetor de amostras no formato correto)
        x_buffer = x[i:i - ORDEM_FILTRO:-1] 

        # 2. Saída do Filtro Adaptativo (y[n])
        y_n = np.dot(w, x_buffer)

        # 3. Sinal de Erro (e[n])
        e_n = s[i] - y_n
        
        # Salva o erro da última época para plotagem (e[n] recuperado)
        if epoch == N_EPOCHS - 1:
            e_final[i] = e_n

        # 4. Atualização dos Pesos do Filtro
        w = w + PASSO_APRENDIZADO * e_n * x_buffer
        
        # 5. Acumulação de Erro (para a função custo)
        int_error_sq += e_n**2
    
    energy_error[epoch] = int_error_sq / N_AMOSTRAS # Média quadrática do erro por amostra


# --- Plotagem dos Resultados ---

plt.figure(figsize=(10, 8))

# 1. Sinal Puro (d[n])
plt.subplot(3, 1, 1)
plt.plot(t, d)
plt.title('1. Desired Signal: d[n]', fontsize=12)
plt.ylabel('Amplitude')
plt.grid(True)

# 2. Sinal Contaminado (s[n])
plt.subplot(3, 1, 2)
plt.plot(t, s)
plt.title('2. Contaminated Signal: s[n]', fontsize=12)
plt.ylabel('Amplitude')
plt.grid(True)

# 3. Sinal Recuperado (e[n]) - Erro da Última Época
plt.subplot(3, 1, 3)
plt.plot(t, e_final)
plt.title('3. Recovered Signal: e[n] (Última Época)', fontsize=12)
plt.xlabel('t (s)')
plt.ylabel('Amplitude')
plt.grid(True)

plt.tight_layout()
plt.show()

# Normalização e Conversão para int16 (PCM de 16 bits)
# Não foi usado com amplitude máximo devido a Prevenção de Saturação (Clipping) e Estabilidade do Filtro Adaptativo.
d_int16 = (d * 32767/2).astype(np.int16)
s_int16 = (s * 32767/2).astype(np.int16)
e_int16 = (e_final * 32767/2).astype(np.int16)

# --- Salvamento dos Sinais em Arquivos PCM ---

out_1 = np.memmap("Avaliacao_M3/sinal_saida/sinal_puro.pcm", dtype='int16', mode='w+', shape=(len(d_int16),))
out_1[:] = d_int16[:]

out_2 = np.memmap("Avaliacao_M3/sinal_saida/sinal_contaminado.pcm", dtype='int16', mode='w+', shape=(len(s_int16),))
out_2[:] = s_int16[:]

out_3 = np.memmap("Avaliacao_M3/sinal_saida/sinal_recuperado.pcm", dtype='int16', mode='w+', shape=(len(e_int16),))
out_3[:] = e_int16[:]