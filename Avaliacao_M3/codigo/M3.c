/* am_mod_demod.c
   Simples modulação AM e demodulação com filtro FIR (janela sinc + Hamming).
   Input/Output: raw PCM 16-bit signed little-endian, mono.
   Compile: gcc -O2 -o am_mod_demod am_mod_demod.c -lm
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>

# define M_PI 3.14159265358979323846

/* Configurações do FIR */
#define FIR_TAPS 101  /* número de coeficientes (ímpar para ter simetria) */

int main(int argc, char *argv[]) {
    if (argc < 7) {
        printf("Uso: %s entrada.pcm sample_rate carrier_freq modulation_index out_mod.pcm out_demod.pcm\n", argv[0]);
        return 1;
    }

    const char *infile = argv[1];
    int sample_rate = atoi(argv[2]);
    double fc = atof(argv[3]); /* frequência do portador */
    double mod_index = atof(argv[4]); /* 0..1 */
    const char *out_mod = argv[5];
    const char *out_demod = argv[6];

    FILE *fin = fopen(infile, "rb");
    if (!fin) { perror("fopen Avaliacao_M3/sinal_entrada/teste_audio_4.pcm"); return 1; }
    FILE *fmod = fopen(out_mod, "wb");
    if (!fmod) { perror("fopen out_mod"); fclose(fin); return 1; }
    FILE *fdem = fopen(out_demod, "wb");
    if (!fdem) { perror("fopen out_demod"); fclose(fin); fclose(fmod); return 1; }

    /* Lê todo arquivo em memória (simples) */
    fseek(fin, 0, SEEK_END);
    long flen = ftell(fin);
    fseek(fin, 0, SEEK_SET);
    long nsamples = flen / sizeof(int16_t);
    int16_t *buffer = (int16_t*)malloc(nsamples * sizeof(int16_t));
    if (!buffer) { fprintf(stderr,"Memória insuficiente\n"); fclose(fin); fclose(fmod); fclose(fdem); return 1; }
    if (fread(buffer, sizeof(int16_t), nsamples, fin) != (size_t)nsamples) {
        fprintf(stderr,"Erro leitura arquivo\n");
        free(buffer); fclose(fin); fclose(fmod); fclose(fdem); return 1;
    }
    fclose(fin);

    /* Prepara coeficientes do filtro FIR passa-baixas (sinc * Hamming) */
    int M = FIR_TAPS;
    double *h = (double*)calloc(M, sizeof(double));
    if (!h) { fprintf(stderr,"Memória insuficiente\n"); free(buffer); fclose(fmod); fclose(fdem); return 1; }

    /* Corte para o LPF (depois da demodulação queremos passar apenas frequências do sinal base).
       Escolha fc_lpf como metade da frequência do portador ou algo adequado ao conteúdo.
       Aqui usamos fc_lpf = sample_rate * 0.1 (10% Nyquist) por simplicidade. */
    double fc_lpf = sample_rate * 0.08; /* corte em Hz (ajustável) */
    double fc_norm = fc_lpf / sample_rate; /* normalizado (0..0.5) - but sinc uses cycles/sample */
    int mid = M/2;
    for (int n = 0; n < M; ++n) {
        int k = n - mid;
        double x;
        if (k == 0) x = 2.0 * fc_norm; /* sinc(0) -> 2*fc */
        else x = sin(2.0 * M_PI * fc_norm * k) / (M_PI * k);
        /* Hamming window */
        double w = 0.54 - 0.46 * cos(2.0 * M_PI * n / (M - 1));
        h[n] = x * w;
    }
    /* Normaliza ganho do filtro para 1 em DC */
    double sumh = 0.0;
    for (int n = 0; n < M; ++n) sumh += h[n];
    for (int n = 0; n < M; ++n) h[n] /= sumh;

    /* Buffers de processamento */
    double *x = (double*)malloc(nsamples * sizeof(double)); /* sinal original em double [-1,1] */
    double *mod = (double*)malloc(nsamples * sizeof(double));
    double *demod = (double*)malloc(nsamples * sizeof(double));
    if (!x || !mod || !demod) {
        fprintf(stderr,"Memória insuficiente\n");
        free(buffer); free(h); free(x); free(mod); free(demod); fclose(fmod); fclose(fdem);
        return 1;
    }

    /* Converte para double em -1..1 */
    for (long i = 0; i < nsamples; ++i) {
        x[i] = buffer[i] / 32768.0;
    }

    /* Gera modulado AM: s(t) * (1 + m * cos(2πf_ct))  -- modulação por produto com portador */
    double two_pi_fc = 2.0 * M_PI * fc;
    for (long n = 0; n < nsamples; ++n) {
        double t = (double)n / sample_rate;
        double carrier = cos(two_pi_fc * t);
        /* modulado */
        mod[n] = x[n] * (1.0 + mod_index * carrier);
        /* para escrever em arquivo vamos escalar depois */
    }

    /* Escreve modulado em 16-bit PCM */
    for (long n = 0; n < nsamples; ++n) {
        double v = mod[n];
        /* limitar */
        if (v > 0.9999) v = 0.9999;
        if (v < -0.9999) v = -0.9999;
        int16_t out = (int16_t) (v * 32767.0);
        fwrite(&out, sizeof(int16_t), 1, fmod);
    }
    fflush(fmod);

    /* Demodulação (produto novamente pelo portador) */
    for (long n = 0; n < nsamples; ++n) {
        double t = (double)n / sample_rate;
        double carrier = cos(two_pi_fc * t);
        demod[n] = mod[n] * carrier; /* produto --> componentes em DC e em 2*fc */
    }

    /* Filtragem FIR (convolução direta, simples) -> saída y[n] */
    double *y = (double*)calloc(nsamples, sizeof(double));
    if (!y) { fprintf(stderr,"Memória insuficiente\n"); free(buffer); free(h); free(x); free(mod); free(demod); fclose(fmod); fclose(fdem); return 1; }

    for (long n = 0; n < nsamples; ++n) {
        double acc = 0.0;
        for (int k = 0; k < M; ++k) {
            long idx = n - k + mid; /* alinhamento para centro do filtro */
            /* outra forma: standard conv: y[n] = sum_{k=0..M-1} h[k]*demod[n-k]  (cuidado com índices negativos) */
            long dindex = n - k;
            if (dindex >= 0) acc += h[k] * demod[dindex];
        }
        y[n] = acc;
    }

    /* Opcional: remover DC offset e ajustar ganho — aqui só normalizamos */
    double maxabs = 1e-12;
    for (long n = 0; n < nsamples; ++n) {
        if (fabs(y[n]) > maxabs) maxabs = fabs(y[n]);
    }
    double gain = 1.0;
    if (maxabs > 0.0) gain = 0.9 / maxabs; /* evita clipping */

    for (long n = 0; n < nsamples; ++n) {
        double v = y[n] * gain;
        if (v > 0.9999) v = 0.9999;
        if (v < -0.9999) v = -0.9999;
        int16_t out = (int16_t)(v * 32767.0);
        fwrite(&out, sizeof(int16_t), 1, fdem);
    }
    fflush(fdem);

    /* Limpeza */
    fclose(fmod);
    fclose(fdem);
    free(buffer);
    free(h);
    free(x);
    free(mod);
    free(demod);
    free(y);

    printf("Processamento concluído.\n");
    printf("Arquivo modulado: %s\n", out_mod);
    printf("Arquivo demodulado: %s\n", out_demod);
    printf("Abra-os no Ocenaudio: Raw -> Signed 16-bit PCM, little-endian, mono, %d Hz.\n", sample_rate);

    return 0;
}
