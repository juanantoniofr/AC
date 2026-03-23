#include <time.h>
#include <stdio.h>

#define N 22000
#define BSIZE 16

unsigned int A[N][N]; 
unsigned int B[N][N]; 

int main() {
    register int i, j, bi, bj;

    // La inicialización se realiza por filas (ya está optimizada).
    for (i=0; i<N; i++) {
        for (j=0; j<N; j++) {
            A[i][j] = i*j%(i+j+1);
        }
    }

    clock_t inicio = clock();
    
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

    // Calcula el tiempo transcurrido y lo muestra en pantalla. Se 
    // excluye el tiempo de inicialización de la matriz A.
    clock_t fin = clock();
    double tiempo_segundos = (double)(fin - inicio) / CLOCKS_PER_SEC;    
    printf("Tiempo transcurrido: %f segundos\n", tiempo_segundos);       
    return 0;
}
