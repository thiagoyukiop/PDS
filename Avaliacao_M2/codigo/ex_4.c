#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Parâmetros do sistema
#define FS 44100.0
#define PI 3.141592653589793

// Tamanho máximo de amostras
#define N 441000 // 10 segundos a 44.1 kHz

// Estrutura para um filtro IIR
typedef struct {
    int ordem;
    double a[3]; // Numerador
    double b[3]; // Denominador
    double x[3]; // Amostras de entrada anteriores
    double y[3]; // Amostras de saída anteriores
} FiltroIIR;

// Função para aplicar um filtro IIR
double aplicar_filtro(FiltroIIR *f, double entrada) {
    // Desloca histórico
    for (int i = f->ordem; i > 0; i--) {
        f->x[i] = f->x[i - 1];
        f->y[i] = f->y[i - 1];
    }
    f->x[0] = entrada;

    // Calcula saída: y[n] = a0*x[n] + a1*x[n-1] + a2*x[n-2] - b1*y[n-1] - b2*y[n-2]
    double y = 0.0;
    for (int i = 0; i <= f->ordem; i++) {
        y += f->a[i] * f->x[i];
    }
    for (int i = 1; i <= f->ordem; i++) {
        y -= f->b[i] * f->y[i];
    }

    f->y[0] = y;
    return y;
}

// Função auxiliar para calcular aB
double calc_aB(double fc, double G, double V0) {
    double t = tan(PI * fc / FS);
    double num, den;
    if (G >= 0) {
        num = t - 1;
        den = t + 1;
    } else {
        num = t - V0;
        den = t + V0;
    }
    return num / den;
}

// Programa principal
int main() {
    // Ganhos e frequências
    double G_PB = 5.0, G_PF = 2.5, G_PA = -5.0;
    double fc_PB = 1000.0, fc_PA = 10000.0, fc_PF = 5000.0, fb = 2000.0;

    // Cálculo de V0 e H0
    double V0_PB = pow(10.0, G_PB / 20.0);
    double H0_PB = V0_PB - 1.0;

    double V0_PF = pow(10.0, G_PF / 20.0);
    double H0_PF = V0_PF - 1.0;

    double V0_PA = pow(10.0, G_PA / 20.0);
    double H0_PA = V0_PA - 1.0;

    double d = -cos(2.0 * PI * fc_PF / FS);

    // Cálculo de aB para cada filtro
    double aB_PB = calc_aB(fc_PB, G_PB, V0_PB);
    double aB_PF = calc_aB(fb, G_PF, V0_PF);
    double aB_PA = calc_aB(fc_PA, G_PA, V0_PA);

    // Configura filtros
    FiltroIIR PB, PF, PA;

    // ----- Passa-baixa -----
    PB.ordem = 1;
    PB.a[0] = 1 + H0_PB/2 + H0_PB/2 * aB_PB;
    PB.a[1] = aB_PB * (1 + H0_PB/2) + H0_PB/2;
    PB.b[0] = 1;
    PB.b[1] = aB_PB;
    PB.x[0] = PB.x[1] = PB.y[0] = PB.y[1] = 0;

    // ----- Passa-faixa -----
    PF.ordem = 2;
    PF.a[0] = 1 + H0_PF/2 - H0_PF/2 * aB_PF;
    PF.a[1] = (d - d * aB_PF) * (1 + H0_PF);
    PF.a[2] = H0_PF/2 - H0_PF/2 * aB_PF - aB_PF;
    PF.b[0] = 1;
    PF.b[1] = (d - d * aB_PF);
    PF.b[2] = -aB_PF;
    for (int i = 0; i < 3; i++) PF.x[i] = PF.y[i] = 0;

    // ----- Passa-alta -----
    PA.ordem = 1;
    PA.a[0] = 1 + H0_PA/2 - H0_PA/2 * aB_PA;
    PA.a[1] = aB_PA * (1 + H0_PA/2) - H0_PA/2;
    PA.b[0] = 1;
    PA.b[1] = aB_PA;
    PA.x[0] = PA.x[1] = PA.y[0] = PA.y[1] = 0;

    // Leitura do arquivo sweep .pcm
    FILE *fin = fopen("../sinal_entrada/sweep_20_20k.pcm", "rb");
    if (!fin) {
        printf("Erro ao abrir arquivo sweep.\n");
        return 1;
    }

    short buffer[N];
    int nSamples = fread(buffer, sizeof(short), N, fin);
    fclose(fin);

    printf("Processando %d amostras...\n", nSamples);

    // Aplicação em cascata dos filtros
    FILE *fout = fopen("../sinal_saida/sweep_equalizado.pcm", "wb");
    if (!fout) {
        printf("Erro ao criar arquivo de saída.\n");
        return 1;
    }

    for (int i = 0; i < nSamples; i++) {
        double x = buffer[i] / 32768.0; // normaliza
        double y = aplicar_filtro(&PB, x);
        y = aplicar_filtro(&PF, y);
        y = aplicar_filtro(&PA, y);

        if (y > 1.0) y = 1.0;
        if (y < -1.0) y = -1.0;

        short out = (short)(y * 32767.0);
        fwrite(&out, sizeof(short), 1, fout);
    }

    fclose(fout);
    printf("Equalização concluída. Arquivo: sweep_equalizado.pcm\n");
    return 0;
}
