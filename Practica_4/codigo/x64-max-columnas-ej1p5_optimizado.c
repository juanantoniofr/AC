// Calcula el m�ximo de cada columna de la matriz mat y lo almacena
// en el vector maximos.
#include <time.h>
#include <stdio.h>

#define N 10000
#define M 50000

int mat[N][M];
int maximos[M];

int main() {
    register int i, j, max;
    // La inicialización se realiza por filas (ya está optimizada).
    for (i=0; i<N; i++) {
        for (j=0; j<M; j++) {
            mat[i][j] = i*j%(i+j+1);
        }
    }

    clock_t inicio = clock();
    
    // -------INICIO DEL CÓDIGO QUE DEBE OPTIMIZARSE---------
    // Calcula el máximo de cada columna de la matriz mat y los almacena en 
    // el vector máximos.
    for (i=0; i<N; i++) {
        maximos[i] = mat[i][0];
        for (j=1; j<M; j++) {
            if (mat[i][j] > max) 
                maximos[i] = mat[i][j];
        }
        maximos[i] = max;
    }
    // -------FINAL DEL C�DIGO QUE DEBE OPTIMIZARSE---------
    

    // Calcula el tiempo transcurrido y lo muestra en pantalla
    clock_t fin = clock();
    double tiempo_segundos = (double)(fin - inicio) / CLOCKS_PER_SEC;    
    printf("Tiempo transcurrido: %f segundos\n", tiempo_segundos);    
}
