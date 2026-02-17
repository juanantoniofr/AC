#include <stdio.h>
#include <omp.h>

long num_steps = 100000000; // 100 millones de rectángulos
double step;

int main() {
    int i;
    double x, pi, sum = 0.0;
    double start_time, run_time;

    // Calculamos el ancho de cada rectángulo (La Base)
    step = 1.0 / (double) num_steps;

    start_time = omp_get_wtime();

    // ---------------------------------------------------------
    // ZONA DE CÓMPUTO INTENSIVO
    // Aquí es donde el procesador pasa el 99% del tiempo.
    // El bucle calcula la altura de cada rectángulo y las acumula.
    // ---------------------------------------------------------
    
    for (i = 0; i < num_steps; i++) {
        x = (i + 0.5) * step;           // Calculamos la posición central del rectángulo
        sum = sum + 4.0 / (1.0 + x*x);  // Sumamos la altura (f(x))
    }

    // ---------------------------------------------------------

    // Finalmente: Área Total = Suma de Alturas * Base
    pi = step * sum;
    
    run_time = omp_get_wtime() - start_time;

    printf("Pi calculado: %.15f\n", pi);
    printf("Tiempo      : %.6f segundos\n", run_time);
    
    return 0;
}