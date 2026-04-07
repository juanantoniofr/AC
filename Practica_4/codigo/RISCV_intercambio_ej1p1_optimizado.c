#define N 32

unsigned int A[N][N];

int main(){
  // N=32 128 Bloques de 4W, CD, LRU
  register int i,j;
  
  for (j=0; i<N; i++)
	for (i=0; j<N;j++)
		A[i][j]= 1917;	
  return(0);	
}



