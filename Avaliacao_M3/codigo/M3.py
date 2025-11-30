import numpy as np
import matplotlib.pyplot as plt

# ------------------ PARÂMETROS ------------------
frame_size = 1024
hop = 512
alpha = 0.9
threshold = 500.0
# -------------------------------------------------

# ------- CARREGA PCM (int16) -------
input_path_sweep = "Avaliacao_M3/sinal_entrada/teste_audio_3.pcm"

sinal = np.memmap(input_path_sweep, dtype='int16', mode='r')

# CONVERSÃO PARA FLOAT (IMPORTANTE!)
sinal = sinal.astype(np.float32)

# ------- INICIALIZAÇÕES -------
output = np.zeros(len(sinal), dtype=np.float32)
noise_profile = np.zeros(frame_size)
pos = 0

# ------- LOOP PRINCIPAL -------
while pos + frame_size < len(sinal):

    frame = sinal[pos:pos + frame_size]

    F = np.fft.fft(frame)

    if np.mean(np.abs(frame)) < threshold:
        noise_profile = alpha * noise_profile + (1 - alpha) * np.abs(F)

    mag_clean = np.abs(F) - noise_profile
    mag_clean[mag_clean < 0] = 0

    F_clean = mag_clean * np.exp(1j * np.angle(F))
    clean = np.fft.ifft(F_clean).real

    output[pos:pos + frame_size] += clean

    pos += hop

# ---- SALVA EM PCM ----
out_int16 = np.clip(output, -32768, 32767).astype(np.int16)
out_int16.tofile("Avaliacao_M3/sinal_saida/saida.pcm")

# # Salvando o sinal filtrado
# output_file = "Aula_10/sinal_saida/out_sweep_20_3k4_PA.pcm"
# out = np.memmap(output_file, dtype='int16', mode='w+', shape=(len(out_int16),))
# out[:] = out_int16[:]

