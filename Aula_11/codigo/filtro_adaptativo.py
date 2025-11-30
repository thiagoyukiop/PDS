# identificacao_nlms.py
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import soundfile as sf   # pip install soundfile

def nlms(u, d, M, mu=0.5, eps=1e-8):
    N = len(u)
    w = np.zeros(M)
    w_hist = np.zeros((N, M))
    e = np.zeros(N)
    # buffer for input vector
    xbuf = np.zeros(M)
    for n in range(N):
        # shift and insert newest sample
        xbuf[1:] = xbuf[:-1]
        xbuf[0] = u[n]
        y = np.dot(w, xbuf)
        e[n] = d[n] - y
        norm_x = np.dot(xbuf, xbuf) + eps
        w = w + (mu / norm_x) * e[n] * xbuf
        w_hist[n, :] = w
    return w_hist, e

def simulate_ma_plant(u, b):
    return signal.lfilter(b, [1.0], u)

def fir_from_iir(num, den, n_taps=64):
    impulse = np.zeros(n_taps)
    impulse[0] = 1.0
    h = signal.lfilter(num, den, impulse)
    return h

def main():
    fs = 44100
    duration = 3.0
    N = int(duration * fs)

    # --- INPUT: white noise (you can replace by reading a file with soundfile.read) ---
    # Option A: generate white noise here:
    # u = np.random.normal(0, 1, N)

    # Option B: load a WAV/PCM you made in Ocenaudio (uncomment to use):
    # path = "white_noise.wav"
    # u, fs = sf.read(path)
    # if u.ndim>1: u = u[:,0]  # single channel
    # N = len(u)

    path = 'Aula_11/sinal_entrada/white_noise.pcm'
    u = np.fromfile(path, dtype=np.int16).astype(np.float32)

# Normaliza para [-1, 1]
    u = u / 32768.0
    N = len(u)

    # ---------------------------------------------------
    # 1) Planta = média móvel (MA) — exemplo simples
    b_ma = np.array([0.3, 0.5, 0.2])   # coeficientes da média móvel (planta desconhecida)
    y_ma = simulate_ma_plant(u, b_ma)
    # adiciona ruído de medição
    noise_sigma = 0.01 * np.std(y_ma)
    y_ma_noisy = y_ma + np.random.normal(0, noise_sigma, len(y_ma))

    # Identificar com NLMS (M = número de taps escolhido)
    M = 8   # tentar >= len(b_ma)
    mu = 0.8
    w_hist_ma, e_ma = nlms(u, y_ma_noisy, M, mu=mu)
    w_final_ma = w_hist_ma[-1, :]

    # Plots para MA
    plt.figure(figsize=(10,6))
    plt.subplot(2,1,1)
    plt.plot(w_hist_ma[:, :len(b_ma)])
    plt.title("Convergência dos primeiros coeficientes (Planta MA)")
    plt.xlabel("Amostra")
    plt.ylabel("Coeficiente")
    plt.legend([f"w{i}" for i in range(len(b_ma))])
    plt.grid()
    plt.subplot(2,1,2)
    plt.plot(20*np.log10(np.abs(e_ma)+1e-12))
    plt.title("Erro (dB) - Planta MA")
    plt.xlabel("Amostra")
    plt.ylabel("Erro (dB)")
    plt.grid()
    plt.tight_layout()
    plt.show()

    print("Coeficientes reais (MA):", b_ma)
    print("Coeficientes estimados (final):", w_final_ma[:len(b_ma)])

    # ---------------------------------------------------
    # 2) Planta = filtro passa-baixa projetado (IIR)
    # Vamos usar a formula do seu script proj_exec_PB.py para obter num/den do shelving.
    # Parâmetros (ajuste conforme necessário)
    G = 10
    V0 = 10**(G/20)
    H0 = V0 - 1
    fc = 1000
    # Fs já definido
    tan_term = np.tan(np.pi * fc / fs)
    if G >= 0:
        aB = (tan_term - 1) / (tan_term + 1)
    else:
        aB = (tan_term - V0) / (tan_term + V0)

    # coeficientes conforme seu script (numerador 'a' e denominador 'b' no seu script)
    a0 = 1 + H0/2 + H0/2 * aB
    a1 = aB * (1 + H0/2) + H0/2
    num_iir = np.array([a0, a1])
    den_iir = np.array([1.0, aB])

    # Obtém resposta ao impulso e aproximação FIR (truncada)
    n_taps = 64
    h_approx = fir_from_iir(num_iir, den_iir, n_taps=n_taps)

    # Planta real (aplica o IIR original ao sinal para gerar y)
    y_iir = signal.lfilter(num_iir, den_iir, u)
    y_iir_noisy = y_iir + np.random.normal(0, 0.01*np.std(y_iir), len(y_iir))

    # Agora identifique a resposta FIR truncada com NLMS (M = n_taps)
    M2 = n_taps
    w_hist_iir, e_iir = nlms(u, y_iir_noisy, M2, mu=0.8)
    w_final_iir = w_hist_iir[-1, :]

    # Plots para IIR aproximado
    plt.figure(figsize=(10,6))
    plt.subplot(2,1,1)
    # mostra comparação entre h_approx e w_final_iir
    plt.stem(h_approx, linefmt='C0-', markerfmt='C0o', basefmt=" ", label="h (impulso truncado)")
    plt.stem(w_final_iir, linefmt='C1--', markerfmt='C1x', basefmt=" ", label="w_est (final)", use_line_collection=True)
    plt.legend()
    plt.title("Resposta ao impulso truncada (h) vs. Estimativa (w_final)")
    plt.xlabel("Índice do coeficiente")
    plt.grid()
    plt.subplot(2,1,2)
    plt.plot(20*np.log10(np.abs(e_iir)+1e-12))
    plt.title("Erro (dB) - Planta IIR identificada como FIR")
    plt.xlabel("Amostra")
    plt.ylabel("Erro (dB)")
    plt.grid()
    plt.show()

    print("Primeiros 10 coef. h_approx:", h_approx[:10])
    print("Primeiros 10 coef. w_final_iir:", w_final_iir[:10])

if __name__ == "__main__":
    main()
