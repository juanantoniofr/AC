#define N 32

unsigned int A[N][N];

int main(){
  // register indica al compilador que use registros para contener los valores de las variables
  // N=32 128 Bloques de 4W, CD, LRU
  register int i,j;
  
  for (j=0; j<N; j++)
	  for (i=0; i<N;i++)
		  A[i][j]= 1917;	
  
  return(0);	
}



