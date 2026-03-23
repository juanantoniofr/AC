#define N 8
#define BSIZE 4

unsigned int A[N][N]= {
    { 31,73,31,37,10,49,47,53 },
    { 14,21,49,58,98,26,67,25 },
    { 16,76,5,16,91,37,62,16 },
    { 6,45,52,5,21,50,42,72 },
    { 75,70,8,43,57,10,24,90 },
    { 15,74,49,95,96,24,69,32 },
    { 91,99,6,19,27,1,3,10 },
    { 23,67,42,75,27,35,27,70 }
}; 
unsigned int B[N][N]; 

int main() {
    register int i, j, bi, bj;
    
    // Almacena en B la traspuesta de A
    for (bi = 0; bi < N; bi += BSIZE) {
        // Bloque deliminado por las filas [bi, bi+BSIZE)
        for (bj = 0; bj < N; bj += BSIZE) {
            // Bloque deliminado por las columnas [bj,jb+BSIZE)
            
            // Procesamos un pequeño bloque de BSIZE x BSIZE
            for (i = bi; i < bi + BSIZE; i++) {
                for (j = bj; j < bj + BSIZE; j++) {
                    B[j][i] = A[i][j];
                }
            }
        }
    }
    
    return 0;
}
