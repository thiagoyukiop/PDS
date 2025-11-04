#include <stdio.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#define M 100
#define FC 0.1

int main() {
    FILE *f = fopen("sinc.txt", "w");
    if (!f) return 1;

    int n;
    double h;
    int n_center = M / 2;

    for (n = 0; n <= M; n++) {
        double x = 2 * FC * (n - n_center);
        h = (x == 0.0) ? 1.0 : sin(M_PI * x) / (M_PI * x);  // sinc(x)
        fprintf(f, "%d\t%lf\n", n, h);
    }

    fclose(f);
    printf("Arquivo sinc.txt gerado.\n");
    return 0;
}
