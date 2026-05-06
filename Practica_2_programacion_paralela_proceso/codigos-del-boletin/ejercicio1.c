#include <stdio.h>
#include <omp.h>

int main() {
    // 1. Preguntamos al sistema cuántos procesadores lógicos tiene disponibles
    // Esto incluye núcleos físicos y virtuales (Hyper-Threading)
    int num_procs = omp_get_num_procs();

    // 2. Preguntamos cuántos hilos usaría OpenMP por defecto
    int max_threads = omp_get_max_threads();

    printf("--- INFORME DE HARDWARE ---\n");
    printf("Tu PC tiene %d procesadores logicos disponibles.\n", num_procs);
    printf("Por defecto, OpenMP creara equipos de %d hilos.\n", max_threads);
    
    printf("\n--- PRUEBA DE EJECUCION ---\n");
    #pragma omp parallel
    {
        int id = omp_get_thread_num();
		int total_threads = omp_get_num_threads();
        printf("Hola desde el hilo %d de %d\n", id, total_threads);
    }
    
    return 0;
}