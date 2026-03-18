#include <stdio.h>
#include <omp.h>

int main() {
    int ultimo = -1;

    // TAREA: Ejecuta este bucle paralelo.
    // Queremos que, al acabar, la variable 'ultimo' conserve 
    // el valor de la última iteración (i = 9).

    #pragma omp parallel for lastprivate(ultimo)
    for (int i = 0; i <= 10; i++) {
        ultimo = i;
        // Simulamos trabajo...
        printf("Hilo %d trabajando en iteracion %d, ultimo = %d\n", omp_get_thread_num(), i, ultimo);
    }

    printf("Valor final de 'ultimo': %d\n", ultimo);

    return 0;
}