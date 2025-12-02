/*
 * Implementação do Algoritmo LMS (Least Mean Squares)
 * para Cancelamento de Ruído.
 * Aritmética de Ponto Fixo (Short - Q15).
 */

#define ORDEM_FILTRO   5       // M
#define MU_FIXED       82     // Representação Q15 de 0.005 (164/32768)

// Variáveis Estáticas (Variáveis Globais internas ao arquivo)
// Elas retêm o estado entre as chamadas da função proc_alg.
// Devem ser iniciadas uma vez.

// Buffer de amostras de Referência (x_buffer)
static short x_buffer[ORDEM_FILTRO] = {0}; 

// Pesos do filtro (w) - Inicializados em zero
static short w[ORDEM_FILTRO] = {0};

/*
 * Função principal do processamento LMS (adaptada de proc_alg)
 *
 * @param s_n: Sinal Contaminado (d[n] + r[n]) - Entrada Desejada
 * @param x_n: Sinal de Referência (x[n]) - Entrada do Filtro
 * @return O Sinal de Erro (e[n]) - Sinal Recuperado
 */
short proc_alg( short s_n, short x_n )
{
    long y_n_long = 0; // Acumulador para a saída do filtro (y[n])
    int i;
    
    // --- 1. Desloca o Buffer de Entrada (x_buffer) ---
    for( i = ORDEM_FILTRO - 1; i > 0; i-- ) 
    {
		x_buffer[i] = x_buffer[i-1];	
	}
    // O novo elemento (x[n]) entra na posição 0
	x_buffer[0] = x_n;
    
    
    // --- 2. Saída do Filtro Adaptativo (y[n]) - Convolução no tempo discreto ---
    for( i = 0; i < ORDEM_FILTRO; i++ ) 
    {
		// Multiplicação de 16-bit (Q15) * 16-bit (Q15) -> 32-bit (Q30)
		y_n_long += (long)w[i] * (long)x_buffer[i];	
	}
	
    // Normaliza para Q15 e converte para short
	short y_n = (short) (y_n_long >> 15); 
	
    
    // --- 3. Sinal de Erro (e[n]) ---
    // e[n] = s[n] - y[n]
	short e_n = s_n - y_n;
	
	
    // --- 4. Atualização dos Pesos do Filtro ---
    // w[i](n+1) = w[i](n) + MU * e[n] * x[n-i]
    
    // O termo de correção é: MU * e[n] * x[n-i]
    // MU (Q15) * e[n] (Q15) * x[n-i] (Q15)
    // Usaremos uma multiplicação em 64 bits (long long) para garantir precisão
    // 16-bit * 16-bit * 16-bit -> Q45.
    // Para retornar a um valor Q15, precisamos de 30 deslocamentos: >>30.

    // No entanto, para o Blackfin, que é 32-bit/16-bit otimizado, vamos usar 
    // a multiplicação 16x16 -> 32 e depois 16x32 -> 32 ou 64.
    
    // Abordagem Simplificada (Comum em DSP de ponto fixo) - Resultado de 32 bits:
    // (e[n] * x[n-i]) -> Q30.
    // Multiplicar por MU_FIXED (Q15): (MU_FIXED * (e[n] * x[n-i]) >> 15) -> Q30.
    // Deslocar 15 bits adicionais para Q15: >>15.
    // Total de deslocamentos (e[n]*x[n-i])*MU: 15 + 15 = 30 bits.
    
    for( i = 0; i < ORDEM_FILTRO; i++ ) 
    {
        // 1. Cálculo da parte e[n] * x[n-i] (Resulta em Q30 no long)
        long term_grad = (long)e_n * (long)x_buffer[i]; 
/*
        // 2. Multiplicação por MU (MU_FIXED * Q30) -> Q45.
        // O valor term_grad já está em Q30 (long). MU_FIXED é Q15 (short).
        // (long)MU_FIXED * Q30 -> Q45. Usamos o tipo long long para acumular o Q45.
        long long update = (long long)MU_FIXED * term_grad;

        // 3. Normaliza de Q45 para Q15 (Desloca 30 bits)
        // O termo de atualização w_update (Q15)
        short w_update = (short) (update >> 30); 
        
        // 4. Atualiza o peso (w[i](n+1) = w[i](n) + w_update)
		w[i] += w_update;	*/
		long update = (long)MU_FIXED * (long)e_n; // Q30
        update = update >> 15; // De volta a Q15 (mu * e)
        update = (long)x_buffer[i] * update; // Q30
        update = update >> 15; // De volta a Q15 (o termo final)
        
        short w_update = (short) update; 

        // 4. Atualiza o peso
		w[i] += w_update;
	}
	
    // Imprimir os pesos finais (opcional, para debug)
    /*
    if (i % 1000 == 0) { // A cada 1000 amostras
        printf("w[0]=%d, w[1]=%d\n", w[0], w[1]);
    }
    */
    
    // Retorna o erro e[n] (sinal recuperado)
    return e_n;
}