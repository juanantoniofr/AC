#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define N 10000000 // 10 Millones
int* A;

int main() {
    A = (int*)malloc(N * sizeof(int));
    for (int i = 0; i < N; i++) A[i] = 1; // Llenamos de 1s

    long long suma = 0;
    double start, end;

	omp_set_num_threads(4); // Establecemos el número de hilos

    // --- MODO 1: ATOMIC (Fuerza Bruta) ---
    start = omp_get_wtime();

    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        #pragma omp atomic
        suma += A[i];
    }

    end = omp_get_wtime();
    printf("Suma Atomic: %lld | Tiempo: %f seg\n", suma, end - start);

    // --- MODO 2: REDUCTION (Estrategia) ---
    suma = 0; // Reiniciamos
    start = omp_get_wtime();

    // TAREA: Completa la directiva con la cláusula reduction
    // #pragma omp parallel for ...
    for (int i = 0; i < N; i++) {
        suma += A[i];
    }

    end = omp_get_wtime();
    printf("Suma Reduction: %lld | Tiempo: %f seg\n", suma, end - start);

    free(A);
    return 0;
}