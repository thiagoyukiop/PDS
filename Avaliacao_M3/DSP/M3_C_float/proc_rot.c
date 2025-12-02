/*
 * Arquivo: proc_rot.c
 * Propósito: Implementa o Algoritmo LMS (Least Mean Squares) para Cancelamento de Ruído.
 * Usa aritmética de Ponto Flutuante (float) para alta precisão.
 */

#define ORDEM_FILTRO   5       // Ordem do filtro (M)
#define MU_FLOAT       0.005f  // Coeficiente de aprendizado (mu) em float

// Variáveis Estáticas: Mantêm o estado do filtro entre chamadas
static float x_buffer[ORDEM_FILTRO] = {0.0f}; // Buffer de amostras de referência
static float w[ORDEM_FILTRO] = {0.0f};      // Vetor de pesos do filtro (coeficientes)

/*
 * Função principal do processamento LMS
 * @param s_n: Sinal Contaminado (Entrada Primária)
 * @param x_n: Sinal de Referência (Entrada do Filtro)
 * @return O Sinal de Erro (e[n]) - Sinal Recuperado
 */
 
float proc_alg( float s_n, float x_n )
{
    float y_n = 0.0f; // Saída do filtro (y[n])
    float e_n;        // Sinal de Erro/Recuperado (e[n])
    int i;
    
    // --- 1. Desloca e Atualiza o Buffer de Entrada (x_buffer) ---
    // Insere o novo x_n na posição 0
    for( i = ORDEM_FILTRO - 1; i > 0; i-- ) 
    {
		x_buffer[i] = x_buffer[i-1];	
	}
	x_buffer[0] = x_n;
    
    
    // --- 2. Saída do Filtro Adaptativo (y[n]) ---
    // y[n] = sum( w[i] * x[n-i] )
    for( i = 0; i < ORDEM_FILTRO; i++ ) 
    {
		// Multiplicação float * float
		y_n += w[i] * x_buffer[i];	
	}
	
    
    // --- 3. Sinal de Erro (e[n]) ---
    // Calcula o erro: e[n] = s[n] - y[n]
	e_n = s_n - y_n;
	
	
    // --- 4. Atualização dos Pesos ---
    // Regra LMS: w[i](n+1) = w[i](n) + MU * e[n] * x[n-i]
    for( i = 0; i < ORDEM_FILTRO; i++ ) 
    {
        float w_update = MU_FLOAT * e_n * x_buffer[i]; 
        
		w[i] += w_update;	
	}
    return e_n;
}