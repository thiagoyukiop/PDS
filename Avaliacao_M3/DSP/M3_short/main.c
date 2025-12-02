/*
 * Arquivo: main.c
 * Propósito: Implementa o loop principal para o Cancelamento de Ruído Adaptativo (LMS).
 * Lê o Sinal Contaminado (s[n]) e o Ruído de Referência (x[n]) em formato short, 
 * processa com aritmética de Ponto Fixo (Q15), e salva o Sinal Recuperado (e[n]).
 * Plataforma: VisualDSP (ADSP-BF533).
 */

#include <stdio.h>
#include <string.h>
#include <cycles.h>

// --- Parâmetros de Ponto Fixo ---
#define ORDEM_FILTRO   5       // Ordem do filtro (M)
#define NSAMPLES       8000    // Número de amostras
#define MU_FIXED       164     // Representação Q15 de 0.005 (mu)

// Prototipo da função LMS (Processamento em short)
extern short proc_alg( short, short );

int main(int argc,char *argv[])
{
 	cycle_stats_t stats;
	FILE *fin,*fin_ref,*fout; 
	short s_n;       // Sinal Contaminado (entrada)
	short x_n;       // Sinal de Referência (entrada)
	short e_n;       // Sinal de Erro/Recuperado (saída)
	
	printf("***************************************************************\n");
	printf("* TESTE COM ARQUIVOS - CANCELAMENTO DE RUÍDO LMS               *\n");
	printf("* *\n");
	printf("***************************************************************\n");
	printf("\n");
	
	// --- Abertura de Arquivos ---
	
	// 1. Sinal Contaminado (s[n] = d[n] + r[n])
	// Abre o Sinal Contaminado (entrada primária) e o Ruído de Referência (entrada do filtro).
	fin = fopen("..\\sinal_contaminado.pcm","rb");
    if ((fin)==NULL)
  	{
    	printf("\nErro: nao abriu o arquivo de Sinal Contaminado\n");
    	return 0;
  	}

    fin_ref = fopen("..\\ruido_referencia.pcm","rb"); 
    if ((fin_ref)==NULL)
  	{
    	printf("\nErro: nao abriu o arquivo de Ruído de Referência\n");
    	return 0;
  	}
    
    // Arquivo de saída para o Sinal Recuperado.
    fout = fopen("..\\sinal_recuperado_short.pcm","wb");
    if ((fout)==NULL)
  	{
    	printf("\nErro: nao abriu o arquivo de Saida\n");
    	return 0;
  	}
  	
  	CYCLES_INIT(stats);
	  	
    printf("Processando LMS (N=%d) ...\n ", NSAMPLES);
    
    // --- Loop de Processamento Principal (Amostra por Amostra) ---
    // Lê 1 short de cada arquivo de entrada por vez.
    while ( (fread(&s_n,sizeof(short),1,fin) == 1) && (fread(&x_n,sizeof(short),1,fin_ref) == 1) ) 
    {
		CYCLES_START(stats);	
		
		// Executa o algoritmo LMS (ponto fixo) e retorna o Sinal de Erro/Recuperado e[n].
		e_n = proc_alg( s_n, x_n ); 

		CYCLES_STOP(stats);
		
        // Grava a amostra de saída (curto).
		fwrite(&e_n,sizeof(short),1,fout);	
	}

    printf("Processamento terminado!\n");
    
	// --- Finalização ---
	CYCLES_PRINT(stats);
		fclose(fin);
		fclose(fin_ref);
		fclose(fout);
		
    return 0;
}