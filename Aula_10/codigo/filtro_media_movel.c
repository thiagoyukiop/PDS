/* Implementação de um filtro Média Móvel
Lê um arquivo binário com amostras em 16bits
Salva arquivo filtrado também em 16 bits
Walter versão 1.0
*/
#include <stdio.h>
#include <fcntl.h>
#include <io.h>
#define NSAMPLES 100 // Tamanho da média

int main()  {
    FILE *in_file, *out_file;
    int i, n, n_amost;
    short entrada, saida;
    short sample[NSAMPLES] = {0x0};
    float y=0;
    //Carregando os coeficientes do filtro média móvel
    float coef[NSAMPLES]={
        #include "..//sinal_saida/h_fir_pb_blackman_M100.txt"
    };
    /* abre os arquivos de entrada e saida */
    if ((in_file = fopen("..//sinal_entrada/seno_400Hz.pcm","rb"))==NULL)
    {
    printf("\nErro: Nao abriu o arquivo de entrada\n");
    return 0;
    }
    if ((out_file = fopen("..//sinal_saida/out_seno_400Hz_C.pcm","wb"))==NULL)
    {
    printf("\nErro: Nao abriu o arquivo de saida\n");
    return 0;
    }

    // zera vetor de amostras
    for (i=0; i<NSAMPLES; i++)
    {
    sample[i]=0;
    }

    // execução do filtro
    do {
    y=0 ; //zera saída do filtro;
    n_amost = fread(&entrada,sizeof(short),1,in_file); //lê dado do arquivo
    sample[0] = entrada;
    for (n=0; n<NSAMPLES; n++) //Convolução
    {
    y += coef[n]*sample[n];
    }
    for (n=NSAMPLES-1; n>0; n--) //desloca vetor de amostras
    {
    sample[n]=sample[n-1];
    }
    saida = (short) y;

    fwrite(&saida,sizeof(short),1,out_file); //escreve no arquivo de saída
    } while (n_amost);

    // fecha os arquivos de entrada de saída
    fclose(out_file);
    fclose(in_file);
    return 0;
}

// Calculo da atenualçao em db
// Atenuação(dB) = 20*log10( Vout / Vin )
// Atenuação(dB) = -6db