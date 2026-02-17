#include <stdio.h>
#include <omp.h>

#define N 1000000 // 1 Millón de elementos

int main() {
    int contador = 0;

	omp_set_num_threads(4); // Establece el número de hilos

    // TAREA: Paraleliza este bucle.
    // Estamos escribiendo todos en 'contador' a la vez.
    // ¿Qué crees que pasará?

    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        if (i % 2 == 0) {
            contador++; // ZONA DE CONFLICTO
        }
    }

    printf("Numeros pares encontrados: %d\n", contador);
    printf("Deberian ser: %d\n", N / 2);

    if (contador != N / 2) printf("ERROR! Se han perdido actualizaciones.\n");
    return 0;
}