/* Implementação de um delay eco
Lê um arquivo binário com amostras em 16bits
a0 = 1.0 e a1 = 0.5
delay de 16 amostras
Salva arquivo filtrado também em 16 bits
*/
#include <stdio.h>
#include <fcntl.h>
#include <io.h>
#define D 16
int main()  {
    FILE *in_file, *out_file;
    int i, n, n_amost, n_delay = 16;
    short entrada, saida;
    short sample[D] = {0x0};
    float y=0;
    /* abre os arquivos de entrada e saida */
    if ((in_file = fopen("..//sinal_impulso.pcm","rb"))==NULL)
    {
    printf("\nErro: Nao abriu o arquivo de entrada\n");
    return 0;
    }
    if ((out_file = fopen("..//sai_sinal_impulso_eco.pcm","wb"))==NULL)
    {
    printf("\nErro: Nao abriu o arquivo de saida\n");
    return 0;
    }
    
    do{
        y=0 ; //zera saída do filtro;
        n_amost = fread(&entrada,sizeof(short),1,in_file); //lê dado do arquivo
        if(n_amost) {
            y = entrada;
            if(n_delay>0) {
                y+= 0.5*sample[n_delay-1];
            }
            for(i=n_delay-1; i>0; i--) //desloca vetor de amostras
            {
                sample[i]=sample[i-1];
            }
            if(n_delay>0) {
                sample[0] = y;
            }

            saida = (short) y;
            fwrite(&saida,sizeof(short),1,out_file); //escreve no arquivo de saída
        }
        // // implementação do delay eco
        // // y[n] = a0*x[n] + a1*x[n-D]
        // y = (1.0*entrada) + (0.5*sample[n_delay-1]);
        // // desloca vetor de amostras
        // for (i=n_delay-1; i>0; i--) //desloca vetor de amostras
        // {
        //     sample[i]=sample[i-1];
        // }
        // sample[0] = entrada;
        // saida = (short) y;
        // fwrite(&saida,sizeof(short),1,out_file); //escreve no arquivo de saída        
    } while(n_amost);

    // fecha os arquivos de entrada de saída
    fclose(out_file);
    fclose(in_file);
    return 0;
}