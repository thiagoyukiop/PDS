/*
 * Arquivo: proc_rot.c
 * Propósito: Implementa o Algoritmo LMS (Least Mean Squares) para Cancelamento de Ruído.
 * Usa aritmética de Ponto Fixo Q15 (short) com acumulação em 32/64 bits (long/long long).
 */

#define ORDEM_FILTRO   5       // Ordem do filtro (M)
#define MU_FIXED       164     // Representação Q15 de 0.005 (mu)

// Variáveis Estáticas: Mantêm o estado do filtro entre chamadas
static short x_buffer[ORDEM_FILTRO] = {0}; // Buffer de amostras de referência
static short w[ORDEM_FILTRO] = {0};      // Vetor de pesos do filtro

/*
 * Função principal do processamento LMS
 * @param s_n: Sinal Contaminado (Entrada Primária)
 * @param x_n: Sinal de Referência (Entrada do Filtro)
 * @return O Sinal de Erro (e[n]) - Sinal Recuperado
 */
 
short proc_alg( short s_n, short x_n )
{
    long y_n_long = 0; // Acumulador Q30 para a saída do filtro
    int i;
    
    // --- 1. Atualização do Buffer de Entrada ---
    // Desloca as amostras e insere a nova amostra (x_n) em x_buffer[0].
    for( i = ORDEM_FILTRO - 1; i > 0; i-- ) 
    {
		x_buffer[i] = x_buffer[i-1];	
	}
	x_buffer[0] = x_n;
    
    
    // --- 2. Saída do Filtro (y[n]) ---
    // Calcula y[n]. Multiplicação Q15*Q15 = Q30.
    for( i = 0; i < ORDEM_FILTRO; i++ ) 
    {
		y_n_long += (long)w[i] * (long)x_buffer[i];	
	}
	// Normaliza de Q30 para Q15 (desloca 15 bits).
	short y_n = (short) (y_n_long >> 15); 
	
    
    // --- 3. Sinal de Erro (e[n]) ---
    // Calcula o erro: e[n] = s[n] - y[n]
	short e_n = s_n - y_n;
	
	
    // --- 4. Atualização dos Pesos ---
    // Regra LMS: w[i](n+1) = w[i](n) + MU * e[n] * x[n-i]
    // Cálculo triplo Q15*Q15*Q15 = Q45, armazenado em long long.
    for( i = 0; i < ORDEM_FILTRO; i++ ) 
    {
        long grad_term = (long)e_n * (long)x_buffer[i];    	 // e*x (Q30)
        long long update = (long long)MU_FIXED * grad_term;  // MU*e*x (Q45)
        
        // Normaliza de Q45 para Q15 (desloca 30 bits).
        short w_update = (short) (update >> 30); 
        
        // Atualiza o peso
		w[i] += w_update;	
	}
    
    return e_n;
}