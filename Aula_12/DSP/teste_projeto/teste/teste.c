#include <stdio.h>

int main(void) {
    volatile int i;
    // Sem printf, apenas loop curto e set breakpoint na linha abaixo
    for (i=0; i<10000; ++i) {
        // Nada
    }
    // ponto onde queremos checar se chegou
    return 0;
}
