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
    double atomic_duration = end - start;
    printf("Suma Atomic: %lld | Tiempo: %f seg\n", suma, atomic_duration);

    // --- MODO 2: REDUCTION (Estrategia) ---
    suma = 0; // Reiniciamos
    start = omp_get_wtime();

    // TAREA: Completa la directiva con la cláusula reduction
    #pragma omp parallel for reduction(+:suma)
    for (int i = 0; i < N; i++) {
        suma += A[i];
    }

    end = omp_get_wtime();
    double reduction_duration = end - start;
    printf("Suma Reduction: %lld | Tiempo: %f seg\n", suma, reduction_duration);

    // mejora del rendimiento
    printf("Mejora de rendimiento: %f veces más rápido\n", atomic_duration / reduction_duration);
    free(A);
    return 0;
}