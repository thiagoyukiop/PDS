#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

// --- Parâmetros ---
#define N_AMOSTRAS      8000
#define Fs              8000.0f
#define F_SENOIDE       100.0f
#define PASSO_APRENDIZADO 0.005f
#define ORDEM_FILTRO    5
#define N_EPOCHS        10
#define M_PI 3.14159265358979323846f

// Variáveis globais/estáticas para alocação simples
static float d[N_AMOSTRAS];
static float x[N_AMOSTRAS];
static float r[N_AMOSTRAS];
static float s[N_AMOSTRAS];
static float e_final[N_AMOSTRAS];

static float w[ORDEM_FILTRO];
static float x_buffer[ORDEM_FILTRO];
static float energy_error[N_EPOCHS];

// Função para simular o buffer x[i:i - M:-1] do Python
// Carrega o buffer em ordem reversa (necessário para a convolução)
static void load_x_buffer(int idx) {
	int k;
    for (k = 0; k < ORDEM_FILTRO; k++) {
        int pos = idx - k;
        // Se a posição for válida (>= 0), usa a amostra, senão, usa 0
        x_buffer[k] = (pos >= 0 ? x[pos] : 0.0f);
    }
}

// Função para escrever o vetor float em um arquivo binário PCM (int16)
static int write_pcm_file(const char *filename, const float *data, int num_samples) {
    FILE *file;
    short *data_int16;
    int i;
    
    file = fopen(filename, "wb");
    if (file == NULL) {
        perror("Erro ao abrir o arquivo para escrita");
        return -1;
    }

    // Aloca buffer para conversão
    data_int16 = (short*)malloc(num_samples * sizeof(short));
    if (data_int16 == NULL) {
        fclose(file);
        return -1;
    }

    // Conversão para int16 (16-bit PCM) com fator de escala (igual ao Python)
    for (i = 0; i < num_samples; i++) {
        // Amplitude máxima é 32767. Divisão por 2 no Python para evitar clipping
        data_int16[i] = (short)(data[i] * (32767.0f / 2.0f)); 
    }

    // Escreve os dados no arquivo
    if (fwrite(data_int16, sizeof(short), num_samples, file) != num_samples) {
        perror("Erro ao escrever no arquivo");
        free(data_int16);
        fclose(file);
        return -1;
    }

    free(data_int16);
    fclose(file);
    return 0;
}


int main() {
	int i, k, epoch;
    
    // Configura o seed para compatibilidade com o Python (rand() é menos robusto)
    srand(42);

    // --- Geração dos sinais ---
    float VAR_RUIDO = powf(10.0f, -8.0f / 10.0f);

    for (i = 0; i < N_AMOSTRAS; i++) {
        float t = (float)i / Fs;

        // 1. Sinal Puro d[n]
        d[i] = sinf(2 * M_PI * F_SENOIDE * t);

        // 2. Ruído de Referência x[n] (Ruído branco uniforme em C, em vez de Gaussiano do Python)
        // Isso é uma diferença, mas simula um ruído aleatório.
        float rnd = (float)rand() / (float)RAND_MAX * 2.0f - 1.0f;
        x[i] = sqrtf(VAR_RUIDO) * rnd;

        // 3. Caminho do Ruído r[n]
        r[i] = 1.2f * x[i];
        
        // 4. Sinal Contaminado s[n]
        s[i] = d[i] + r[i];
    }

    // Inicializa pesos e buffer final
    memset(w, 0, sizeof(w));
    memset(e_final, 0, sizeof(e_final));

    // --- Loop Principal LMS com EPOCHS ---
    for (epoch = 0; epoch < N_EPOCHS; epoch++) {

        float int_error_sq = 0.0f;

        for (i = ORDEM_FILTRO; i < N_AMOSTRAS; i++) {

            load_x_buffer(i);

            // 1. Saída do Filtro Adaptativo (y[n])
            float y_n = 0.0f;
            for (k = 0; k < ORDEM_FILTRO; k++)
                y_n += w[k] * x_buffer[k];

            // 2. Sinal de Erro (e[n])
            float e_n = s[i] - y_n;

            // Salva o erro da última época para o arquivo de saída
            if (epoch == N_EPOCHS - 1)
                e_final[i] = e_n;

            // 3. Atualização dos Pesos do Filtro
            for (k = 0; k < ORDEM_FILTRO; k++)
                w[k] += PASSO_APRENDIZADO * e_n * x_buffer[k];

            // 4. Acumulação de Erro (para a função custo)
            int_error_sq += e_n * e_n;
        }

        // Média Quadrática do Erro (MSE)
        energy_error[epoch] = int_error_sq / N_AMOSTRAS;
    }

    // --- Resultados e Validação ---

    printf("\n--- Resultados LMS (C) ---\n");
    
    // Imprime os pesos finais
    printf("Pesos Finais do Filtro w: [");
    for(k = 0; k < ORDEM_FILTRO; k++) {
        printf(" %.8e%s", w[k], (k < ORDEM_FILTRO - 1) ? "," : "");
    }
    printf(" ]\n");
    
    // Imprime o erro final
    printf("MSE da Ultima Epoca: %.8e\n", energy_error[N_EPOCHS - 1]);

    // --- Salvamento dos Arquivos PCM ---
    
    if (write_pcm_file("../sinal_saida/sinal_puro_c.pcm", d, N_AMOSTRAS) == 0 &&
        write_pcm_file("../sinal_saida/sinal_contaminado_c.pcm", s, N_AMOSTRAS) == 0 &&
        write_pcm_file("../sinal_saida/sinal_recuperado_c.pcm", e_final, N_AMOSTRAS) == 0) {
        
        printf("\nArquivos PCM salvos com sucesso na pasta do projeto:\n");
        printf("- ../sinal_saida/sinal_puro_c.pcm\n");
        printf("- ../sinal_saida/sinal_contaminado_c.pcm\n");
        printf("- ../sinal_saida/sinal_recuperado_c.pcm\n");
    } else {
        printf("\nErro ao salvar arquivos PCM.\n");
    }

    return 0;
}