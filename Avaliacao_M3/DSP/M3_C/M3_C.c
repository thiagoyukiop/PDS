#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <cycles.h>

// --- Parâmetros ---
#define N_AMOSTRAS      1000
#define Fs              8000.0f
#define F_SENOIDE       100.0f
#define PASSO_APRENDIZADO 0.005f
#define ORDEM_FILTRO    5
#define N_EPOCHS        10

#define M_PI 3.14159265358979323846f

// --- Variáveis Globais (ou alocadas estaticamente) ---
float d[N_AMOSTRAS];
float x[N_AMOSTRAS];
float r[N_AMOSTRAS];
float s[N_AMOSTRAS];
float e_final[N_AMOSTRAS];

float w[ORDEM_FILTRO];
float x_buffer[ORDEM_FILTRO];
float energy_error[N_EPOCHS];

// --- Função Auxiliar: Carrega o Buffer de Entrada (Invertido) ---
void load_x_buffer(int current_index, const float *input_signal, float *buffer, int M) {
    int k;
    for (k = 0; k < M; k++) {
        if (current_index - k >= 0) {
            buffer[k] = input_signal[current_index - k];
        } else {
            buffer[k] = 0.0f;
        }
    }
}

// --- Função Principal ---
int main() {
    int i, k, epoch;
    float t;
    float y_n;
    float e_n;
    
    // Inicialização da estrutura de ciclos
    cycle_stats_t stats;
    CYCLES_INIT(stats);

    // --- 1. Geração/Simulação de Sinais Iniciais ---
    srand(42); 
    float VAR_RUIDO = powf(10.0f, -8.0f / 10.0f);
    
    for (i = 0; i < N_AMOSTRAS; i++) {
        t = (float)i / Fs;
        d[i] = sinf(2.0f * M_PI * F_SENOIDE * t);
        
        x[i] = sqrtf(VAR_RUIDO) * ((float)rand() / (float)RAND_MAX * 2.0f - 1.0f);
        r[i] = 1.2f * x[i];
        s[i] = d[i] + r[i];
    }
    
    memset(w, 0, ORDEM_FILTRO * sizeof(float)); 
    memset(e_final, 0, N_AMOSTRAS * sizeof(float)); 
    memset(x_buffer, 0, ORDEM_FILTRO * sizeof(float)); 

    // --- 2. Loop Principal LMS com EPOCHS ---
    
    CYCLES_START(stats); // Inicia a contagem antes do processamento
    
    for (epoch = 0; epoch < N_EPOCHS; epoch++) {
        float int_error_sq = 0.0f;
        
        for (i = ORDEM_FILTRO; i < N_AMOSTRAS; i++) {
            
            // 1. Carrega o Buffer de Entrada
            load_x_buffer(i, x, x_buffer, ORDEM_FILTRO); 
            
            // 2. Saída do Filtro Adaptativo (y[n])
            y_n = 0.0f;
            for (k = 0; k < ORDEM_FILTRO; k++) {
                y_n += w[k] * x_buffer[k];
            }

            // 3. Sinal de Erro (e[n])
            e_n = s[i] - y_n;
            
            if (epoch == N_EPOCHS - 1) {
                e_final[i] = e_n;
            }

            // 4. Atualização dos Pesos
            for (k = 0; k < ORDEM_FILTRO; k++) {
                w[k] = w[k] + PASSO_APRENDIZADO * e_n * x_buffer[k];
            }
            
            // 5. Acumulação de Erro
            int_error_sq += e_n * e_n;
        }
        
        energy_error[epoch] = int_error_sq / N_AMOSTRAS; 
    }

    CYCLES_STOP(stats); // Pára a contagem após o processamento
    
    // --- 3. Resultados e Contagem de Ciclos ---
    
    printf("\n--- Resultados do Filtro LMS ---\n");
    CYCLES_PRINT(stats);

    // Opcional: Conversão para int16 (igual ao Python) para possível salvamento
    // OBS: O VisualDSP++ ou o simulador pode mostrar isso no console ou na memória.
    
    // Simulação da conversão para int16 (para uso futuro, se necessário)
    short d_int16[N_AMOSTRAS];
    short s_int16[N_AMOSTRAS];
    short e_int16[N_AMOSTRAS];

    for (i = 0; i < N_AMOSTRAS; i++) {
        d_int16[i] = (short) (d[i] * 32767.0f / 2.0f);
        s_int16[i] = (short) (s[i] * 32767.0f / 2.0f);
        e_int16[i] = (short) (e_final[i] * 32767.0f / 2.0f);
    }
    
    return 0;
}