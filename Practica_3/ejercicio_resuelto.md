# Realización de la práctica de laboratorio 3

## Ejercicio 1.1

### Investigar si se puede lanzar un número de procesos que sea mayor que el número de núcleos del procesador utilizado y qué ocurre en ese caso.

Al ejecutar el comando `mpirun -np 9 python mpi_program.py` en un sistema con menos de 9 núcleos disponibles, se obtiene el siguiente error:

No hay suficientes ranuras disponibles en el sistema para satisfacer las 9 ranuras solicitadas por la aplicación: python3

Solicite menos ranuras para su aplicación o habilite más ranuras para su uso.

Una "ranura" es el término de Open MPI para una unidad asignable donde podemos iniciar un proceso. El número de ranuras disponibles se define por el entorno en el que se ejecutan los procesos de Open MPI:

- 1. Archivo de host, mediante cláusulas "slots=N" (N toma por defecto el número de núcleos del procesador si no se especifica).
- 2. Parámetro de línea de comandos --host, mediante el sufijo ":N" en el nombre de host (N toma por defecto 1 si no se especifica).
- 3. Gestor de recursos (p. ej., SLURM, PBS/Torque, LSF, etc.).
- 4. Si no se especifica ni un archivo de host, ni el parámetro de línea de comandos --host, ni un gestor de recursos, Open MPI toma por defecto el número de núcleos del procesador.

En todos los casos anteriores, si desea que Open MPI tome por defecto el número de subprocesos de hardware en lugar del número de núcleos del procesador, utilice la opción **--use-hwthread-cpus**.

Alternativamente, puede utilizar la opción **--oversubscribe** para ignorar el número de ranuras disponibles al decidir la cantidad de procesos que se van a ejecutar.

## Ejercicio 1.2

### ¿Qué ocurre al lanzar el programa saludos.py solo para un procesador?

Como el proceso 0 es el encargado de recibir los mensajes de los otros procesos, al ejecutar el programa con un solo proceso, **el proceso 0 no recibirá ningún mensaje** y no imprimirá nada. En este caso, el programa se ejecutará sin errores, pero no se mostrará ningún resultado en la salida.

### ¿por qué?

Por que el proceso 0 está diseñado para esperar mensajes de los procesos con rango 1 a p-1. Si solo se ejecuta un proceso, no hay otros procesos que envíen mensajes al proceso 0, por lo que este último no recibirá ningún mensaje y no imprimirá nada.

## Ejercicio 1.3

### ¿Qué ocurre al lanzar el programa saludos_en_anillo.py solo para un procesador?

Como send no es bloqueante si el tamaño del mensaje no excede los 4KB, el proceso 0 enviará su mensaje al siguiente proceso (que en este caso es él mismo) y luego intentará recibir un mensaje de su anterior (que también es él mismo). No se produce **deadlock**, el proceso enviará su mensaje y luego lo recibirá, imprimiendo el mensaje recibido.

## Ejercicio 1.4

### Estudie el funcionamiento del programa. Para ello, cambie inicialmente el número n de elementos de los vectores a un valor muy pequeño (por ejemplo 6). Ejecute el programa variando el número de procesos lanzados desde 1 hasta 3, y compruebe que los resultados son correctos. Finalmente, estudie el código de ambas versiones para entender cómo se realiza el cálculo.

- Los resultados son correctos para 1, 2 o 3 procesos y un vector de 6 elementos. Sin embargo, para n = 7, para todos los casos 2 y 3 el vector de dimensión 7 no se puede dividir entre el número de procesos, lo que provoca que no se procese el vector completo.
