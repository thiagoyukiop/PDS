/*
 * Arquivo: main.c
 * Propósito: Implementa o loop principal para o Cancelamento de Ruído Adaptativo (LMS).
 * Lê o Sinal Contaminado (s[n]) e o Ruído de Referência (x[n]) em formato short (PCM),
 * converte para float, processa com proc_alg, e salva o Sinal Recuperado (e[n]) em short.
 * Plataforma: VisualDSP (ADSP-BF533).
 */

#include <stdio.h>
#include <string.h>
#include <cycles.h>

// --- Parâmetros ---
#define ORDEM_FILTRO   5       // M
#define NSAMPLES       8000    // Número de amostras
#define MAX_VAL_SHORT  32768.0f // Fator de normalização

// Prototipo da função LMS (Processamento em float)
extern float proc_alg( float, float );

int main(int argc,char *argv[])
{
 	cycle_stats_t stats;   
	FILE *fin,*fin_ref,*fout; 
	
	// Variáveis de I/O (short) e Processamento (float)
	short s_n_short, x_n_short, e_n_short;   
	float s_n_float, x_n_float, e_n_float;   
	
	printf("***************************************************************\n");
	printf("* TESTE COM ARQUIVOS - CANCELAMENTO DE RUÍDO LMS (FLOAT)       *\n");
	printf("***************************************************************\n");
	
	// --- Abertura de Arquivos ---
	// Abre o Sinal Contaminado (entrada primária) e o Ruído de Referência (entrada do filtro).
	fin = fopen("..\\sinal_contaminado.pcm","rb");
    if ((fin)==NULL) { printf("\nErro: nao abriu o arquivo de Sinal Contaminado\n"); return 0; }
    
    fin_ref = fopen("..\\ruido_referencia.pcm","rb"); 
    if ((fin_ref)==NULL) { printf("\nErro: nao abriu o arquivo de Ruído de Referência\n"); return 0; }
    
    // Arquivo de saída para o Sinal Recuperado.
    fout = fopen("..\\sinal_recuperado_float.pcm","wb");
    if ((fout)==NULL) { printf("\nErro: nao abriu o arquivo de Saida\n"); return 0; }
  	
  	CYCLES_INIT(stats);
	  	
    printf("Processando LMS em FLOAT (N=%d) ...\n ", NSAMPLES);
    
    // --- Loop de Processamento Principal (Amostra por Amostra) ---
    // Lê 1 short de cada arquivo de entrada por vez.
    while ( (fread(&s_n_short,sizeof(short),1,fin) == 1) && (fread(&x_n_short,sizeof(short),1,fin_ref) == 1) ) 
    {
        // Converte e Normaliza as entradas de short para float [+/- 1.0].
        s_n_float = (float)s_n_short / MAX_VAL_SHORT;
        x_n_float = (float)x_n_short / MAX_VAL_SHORT;
        
		CYCLES_START(stats);	
		
		// Executa o algoritmo LMS e retorna o Sinal de Erro/Recuperado e[n].
		e_n_float = proc_alg( s_n_float, x_n_float ); 

		CYCLES_STOP(stats);
		
        // Desnormaliza e converte a saída de float para short.
        e_n_short = (short)(e_n_float * MAX_VAL_SHORT);
        
        // Grava a amostra de saída.
		fwrite(&e_n_short,sizeof(short),1,fout);	
	}

    printf("Processamento terminado!\n");
    
	// --- Finalização ---
	CYCLES_PRINT(stats);
		fclose(fin);
		fclose(fin_ref);
		fclose(fout);
		
    return 0;
}