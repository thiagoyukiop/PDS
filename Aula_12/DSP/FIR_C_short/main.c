/* programa para testes com arquivos
-- Lendo arquivos de entrada (Sinal Contaminado 's' e Referencia 'x')
-- Processa: Executa o filtro LMS (Cancelamento de Ruído)
-- Gera arquivo de saida (Sinal de Erro 'e')
-- Thiago Pacheco (LMS)
*/

#include <stdio.h>
#include <string.h>
#include <cycles.h>

// --- Parâmetros do Filtro LMS (Definidos no M3.py) ---
#define ORDEM_FILTRO   5       // M (ORDEM_FILTRO)
#define NSAMPLES       8000    // Número de amostras total (N_AMOSTRAS)
#define MU_DEN_SHIFT   10      // Fator para representar mu (PASSO_APRENDIZADO) em ponto fixo
                               // PASSO_APRENDIZADO = 0.005 (M3.py) ~= 1/200.
                               // 2^10 = 1024. Usaremos 1/1024 (aprox 0.00097) ou um ajuste.
                               // O ADSP-BF533 tem uma MAC de 16x16 -> 32 bits, 
                               // mas o M3 usa 0.005. Vamos simplificar com um MU_SHIFT para 16 bits.
                               // Vamos usar 16-bit Q15 para representar 1.0.
                               
                               // 0.005 * 32768 ~= 164. Usaremos 164.
#define MU_FIXED       164     // Representação Q15 de 0.005 (164/32768)

// O vetor de coeficientes fixo não é mais necessário no main
// short Coefs[NSAMPLES]={...}; 


// Prototipo da função LMS. Agora ela é chamada para processar uma amostra de cada vez.
extern short proc_alg( short, short );

int main(int argc,char *argv[])
{
 	cycle_stats_t stats;   
	// fin é o Sinal Contaminado (s[n]), fin_ref é o Ruído de Referência (x[n])
	FILE *fin,*fin_ref,*fout; 
	short s_n;       // Sinal Contaminado (entrada)
	short x_n;       // Sinal de Referência (entrada)
	short e_n;       // Sinal de Erro/Recuperado (saída)

  	// O Vetor de entrada agora é gerenciado internamente em proc_alg
  
	
	int i;
	
	printf("***************************************************************\n");
	printf("* TESTE COM ARQUIVOS - CANCELAMENTO DE RUÍDO LMS               *\n");
	printf("* *\n");
	printf("***************************************************************\n");
	printf("\n");
	
	// --- Abertura de Arquivos ---
	
	// 1. Sinal Contaminado (s[n] = d[n] + r[n])
	// Nota: M3.py salva como 'sinal_contaminado.pcm'
	fin = fopen("..\\sinal_contaminado.pcm","rb");
    if ((fin)==NULL)
  	{
    	printf("\nErro: nao abriu o arquivo de Sinal Contaminado\n");
    	return 0;
  	}

	// 2. Ruído de Referência (x[n])
    fin_ref = fopen("..\\ruido_referencia.pcm","rb"); 
    if ((fin_ref)==NULL)
  	{
    	printf("\nErro: nao abriu o arquivo de Ruído de Referência\n");
    	return 0;
  	}
    
    // 3. Sinal de Saída (e[n]) - Sinal Recuperado
    fout = fopen("..\\sinal_recuperado_c.pcm","wb");
    if ((fout)==NULL)
  	{
    	printf("\nErro: nao abriu o arquivo de Saida\n");
    	return 0;
  	}
  	
  	CYCLES_INIT(stats);
	  	
    printf("Processando LMS (N=%d) ...\n ", NSAMPLES);
    
    // Loop de leitura/processamento
    while ( (fread(&s_n,sizeof(short),1,fin) == 1) && (fread(&x_n,sizeof(short),1,fin_ref) == 1) ) 
    {
		
		CYCLES_START(stats);	
		
		// Chamada da função LMS com as duas amostras de entrada
		// Retorna o erro/sinal recuperado (e[n])
		e_n = proc_alg( s_n, x_n ); 

		CYCLES_STOP(stats);
		
        // Grava o sinal recuperado (erro)
		fwrite(&e_n,sizeof(short),1,fout);	
	
	}

    printf("terminado!\n");
		
    
	CYCLES_PRINT(stats);
		fclose(fin);
		fclose(fin_ref);
		fclose(fout);
		
    return 0;
}