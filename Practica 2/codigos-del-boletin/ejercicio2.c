#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

#define N 50000000 // 50 Millones de iteraciones

int main() {
    double *A = (double*)malloc(N * sizeof(double));
    double start, end;
    // array con los hilos del equipo, desde 1 hasta 16
    int hilos[] = {1, 2, 4, 8, 16, 32};
    int num_pruebas = sizeof(hilos) / sizeof(hilos[0]);



    // CAMBIA ESTE VALOR para cada prueba (1, 2, 4, 8, 16...)
    //int num_hilos = 1; 
    for (int j = 0; j < num_pruebas; j++) {
        int num_hilos = hilos[j];
        omp_set_num_threads(num_hilos);

        printf("Iniciando calculo con %d hilos...\n", num_hilos);
        start = omp_get_wtime();
    
        // Bucle con alta carga computacional (sin dependencias)
        #pragma omp parallel for
        for (int i = 0; i < N; i++) {
            A[i] = sqrt(i * 4.0) + sin(i) * cos(i); 
        }

        end = omp_get_wtime();
        printf("Tiempo: %f segundos\n", end - start);
    
        
    }
    
    free(A);
    return 0;
}