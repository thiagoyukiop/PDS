

short proc_alg( short *coef, short *entr, int N )
{
    int i;
    int soma = 0;
    short sai_func;
    
   
    for( i=0; i<N; i++ ) 
    {
		soma += coef[i] * entr[i];	
	}
	
	// Desloca o vetor de amostras 
	for( i=N-1; i>0; i-- ) 
    {
		entr[i] = entr[i-1];	
	}
	
	
	sai_func = soma>>15;	// Ok funcionando
//	sai_func = (short) soma;

    return (sai_func);
}



		
