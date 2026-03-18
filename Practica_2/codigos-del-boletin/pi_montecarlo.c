#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

long tiradas = 100000000; // 100 millones de dardos

int main() {
    double x, y;     // Coordenadas del dardo
    long aciertos = 0; // Contador de dardos dentro del círculo
    double pi;
    double start, end;

    // Semilla para los números aleatorios
    srand(time(NULL)); 

    printf("Lanzando %ld dardos...\n", tiradas);
    start = omp_get_wtime();

    // --- ZONA DE CÓMPUTO INTENSIVO ---
    for (long i = 0; i < tiradas; i++) {
        // Generamos coordenadas aleatorias entre 0 y 1
        // (Nota: rand() devuelve un entero, lo normalizamos)
        x = (double)rand() / RAND_MAX;
        y = (double)rand() / RAND_MAX;

        // Comprobamos si ha caído dentro del círculo
        // Ecuación: x^2 + y^2 <= radius^2 (radio = 1)
        if ((x * x + y * y) <= 1.0) {
            aciertos++;
        }
    }
    // ---------------------------------

    pi = 4.0 * ((double)aciertos / (double)tiradas);
    end = omp_get_wtime();

    printf("Pi estimado: %.10f\n", pi);
    printf("Tiempo     : %.6f segundos\n", end - start);

    return 0;
}