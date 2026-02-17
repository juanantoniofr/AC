#include <stdio.h>
#include <omp.h>

#define N 10

int main() {

    int A[N];
    int temp;

    omp_set_num_threads(4); //  Establecemos el número de hilos

    // TAREA: Paraleliza este bucle.
    // El printf actúa como "freno", dando tiempo a que 
    // los hilos se pisen el valor de 'temp' unos a otros.
    
    for (int i = 0; i < N; i++) {
        temp = i;
        printf("Hilo %d trabajando en iteracion %d\n", omp_get_thread_num(), i);
        A[i] = temp;
    }

    // INSPECCIÓN VISUAL
    // Tu trabajo es mirar esta lista. 
    // Si el código funcionase bien, A[i] debería ser igual a i.

    printf("\n--- RESULTADOS FINAL ---\n");
    for (int i = 0; i < N; i++) {
        printf("Posicion %02d contiene: %02d\n", i, A[i]);
    }

    return 0;
}