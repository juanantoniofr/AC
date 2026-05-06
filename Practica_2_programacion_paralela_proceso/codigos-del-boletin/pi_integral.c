#include <stdio.h>
#include <omp.h>

long num_steps = 100000000; // 100 millones de rectángulos
double step;

int main() {
    int i;
    double x, pi, sum = 0.0;
    double start_time, run_time, ref;

    // Calculamos el ancho de cada rectángulo (La Base)
    step = 1.0 / (double) num_steps;

    start_time = omp_get_wtime();

    // ---------------------------------------------------------
    // ZONA DE CÓMPUTO INTENSIVO
    // Aquí es donde el procesador pasa el 99% del tiempo.
    // El bucle calcula la altura de cada rectángulo y las acumula.
    // ---------------------------------------------------------

    // setear número de nucleos
    omp_set_num_threads(8);

    int num_hilos[] = {1, 2, 4, 8 , 10, 12, 16, 20, 32}; 
    int num_pruebas = sizeof(num_hilos) / sizeof(num_hilos[0]);

    for (int j = 0; j < num_pruebas; j++) {
        omp_set_num_threads(num_hilos[j]);
        sum = 0.0;
        start_time = omp_get_wtime();

        #pragma omp parallel for reduction(+:sum) private(x)
        for (i = 0; i < num_steps; i++) {
            x = (i + 0.5) * step;           // Calculamos la posición central del rectángulo
            sum += 4.0 / (1.0 + x*x);  // Sumamos la altura (f(x))
        }

        // ---------------------------------------------------------

        // Finalmente: Área Total = Suma de Alturas * Base
        pi = step * sum;
        
        run_time = omp_get_wtime() - start_time;
        // aceleración
        if (j == 0) {
            ref = run_time;
        }
        double aceleration = ref / run_time;    
 
        printf("Pi calculado: %.15f\n", pi);
        printf("Tiempo      : %.6f segundos\n", run_time);
        printf("Número de hilos: %d\n", num_hilos[j]);
        printf("Aceleración : %.2f veces más rápido\n", aceleration);
        printf("\n");
    }
    
    return 0;
}