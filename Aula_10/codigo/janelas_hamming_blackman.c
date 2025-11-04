#include <stdio.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#define M 100

int main() {
    FILE *f = fopen("janelas.txt", "w");
    if (!f) return 1;

    int n;
    double hamming, blackman;

    for (n = 0; n <= M; n++) {
        hamming = 0.54 - 0.46 * cos(2 * M_PI * n / M);
        blackman = 0.42 - 0.5 * cos(2 * M_PI * n / M) + 0.08 * cos(4 * M_PI * n / M);
        fprintf(f, "%d\t%lf\t%lf\n", n, hamming, blackman);
    }

    fclose(f);
    printf("Arquivo janelas.txt gerado (Hamming e Blackman).\n");
    return 0;
}
