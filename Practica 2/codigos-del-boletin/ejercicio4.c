#include <stdio.h>
#include <omp.h>

int main() {
    int valor = 10;
    int suma = 0;

    omp_set_num_threads(4); 

    // TAREA: Queremos que cada hilo sume su propio 'valor' (que debería ser 10)
    // a la variable global 'suma'.
    
    // NOTA: Usamos 'atomic' solo para evitar conflictos al escribir en 'suma',
    // céntrate en lo que pasa con la variable 'valor'.
    
    #pragma omp parallel private(valor)
    {
        // ¿Cuánto vale 'valor' aquí dentro?
        #pragma omp atomic
        suma += valor; 
        
        printf("Hilo %d suma su valor: %d\n", omp_get_thread_num(), valor);
    }
    
    printf("Suma final: %d (Deberia ser 40)\n", suma);
    return 0;
}