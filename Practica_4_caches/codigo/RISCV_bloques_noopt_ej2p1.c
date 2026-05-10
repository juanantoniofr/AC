#define N 8

unsigned int A[N][N]; 
unsigned int B[N][N]; 

int main() {
    register int i, j;
    
    // Almacena en B la traspuesta de A
    for (i=0; i<N; i++) {
        for (j=0; j<N; j++) {
                B[j][i] = A[i][j];	
        }
    }
    
    return 0;
}
