#include <stdio.h>
#include <omp.h>

int main() {

    // NOTA IMPORTANTE:

    // Si el código no compila, es posible que sea necesario añadir un argumento
    // de compilación adicional para OpenMP.

    // -openmp:llvm 

    // En Visual Studio, esto se puede configurar en las propiedades del proyecto:
    // 1. Haz clic derecho en el proyecto en el Explorador de Soluciones y selecciona "Propiedades".
    // 2. Ve a "C/C++" -> "Linea de Comandos"
    // 3. En "Argumentos adicionales", añade: -openmp:llvm

    // Un vector pequeño para probar
    int vector[10] = { 12, 5, 89, 4, 99, 23, 101, 0, 75, 42 };
    int maximo = vector[0]; // Inicializamos con un valor bajo

	omp_set_num_threads(8); // Establecemos el número de hilos a usar

    // TAREA: Busca el valor máximo en paralelo.

    // #pragma omp parallel for ...
    for (int i = 0; i < 10; i++) {
        if (vector[i] > maximo) {
			printf("Hilo %d encontro un nuevo maximo: %d\n", omp_get_thread_num(), vector[i]);
            maximo = vector[i];
        }
    }

    printf("El valor maximo encontrado es: %d\n", maximo);
    printf("El valor esperado es: 101\n");

    return 0;
}