# Notas

## Muy importante

- Excluir los núcleos de bajo consumo de energía.

```python
mpirun --bind-to core -np X python3 nombre_archivo.py
```

- Función para medir el tiempo

```python
MPI.Wtime()
```

## funciones usadas en las prácticas

- `np.dot(A,B)`: Producto de matrices.
- `np.array(x) @ np.array(y)`: Producto escalar de dos vectores.
- import time: Para medir el tiempo de ejecución de un programa.
- `time.time()`: Devuelve el tiempo actual en segundos desde el epoch (1 de enero de 1970). Se puede usar para medir el tiempo de ejecución de un programa restando el tiempo inicial al tiempo final.

## estrutura de un programa MPI

```pythonfrom mpi4py import MPI
import numpy as np
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# inicialización de datos solo en el proceso 0 (maestro)
if rank == 0:
    # inicialización de datos
    pass
else:
    # Si procede: inicialización de datos para los procesos trabajadores
    pass

# comunicación de datos a los procesos trabajadores
# Envío y recepción simple de data es la variable que contiene los datos a enviar a los procesos trabajadores
comm.send(data, dest=0)
comm.recv(data, source=0)

# Si queremos enviar todos los datos a los procesos trabajadores, por lo que el proceso 0 (maestro) es el encargado de enviar los datos a los procesos trabajadores
dato_local = comm.bcast(data, root=0)
comm.Bcast(data, root=0)

# Si necesitamos dividir los datos en partes iguales para cada proceso trabajador, por lo que el proceso 0 (maestro) es el encargado de dividir los datos y enviarlos a cada proceso trabajador
dato_local = comm.scatter(data, root=0)
comm.Scatter(dato, dato_local, root=0)

# Operación inversa a scatter, cada proceso trabajador realiza su parte del trabajo con los datos recibidos y devuelve una lista ordenada de resultados al proceso 0 (maestro) para que este los combine y devuelva el resultado final

lista_resultados = comm.gather(data, root=0)
comm.Gather(data, lista_resultados, root=0)

# Podemos realizar una operación de reducción para combinar los resultados de todos los procesos trabajadores en un solo resultado final, por lo que el proceso 0 (maestro) es el encargado de realizar la operación de reducción y devolver el resultado final

resultado_final = comm.reduce(data, op=MPI.SUM, root=0)
comm.Reduce(data, resultado_final, op=MPI.SUM, root=0)

# realizamos una operación de reducción colectiva para combinar los resultados de todos los procesos trabajadores en un solo resultado final, por lo que todos los procesos participan en la operación de reducción colectiva y el resultado final se devuelve a todos los procesos

resultado_final = comm.Allreduce(data, op=MPI.SUM)
comm.Allreduce(data, resultado_final, op=MPI.SUM)

# Sincronización de procesos
comm.Barrier()
# Medida de tiempo de ejecución
start_time = MPI.Wtime()



```

## Ejercicio 1.1

### - Investigar si se puede lanzar un número de procesos que sea mayor que el número de núcleos del procesador utilizado y qué ocurre en ese caso.

Se disparan los tiempos de ejecución, ya que el tenemos que añadir el coste de manejar la entrada y salida de los procesos en cada núcleo ya que no hay para todos.

## Ejercicio 1.2

- En este ejercicio se realiza una comunicación simple, todos los procesos envía un mensaje al proceso 0, y este los recibe y los imprime en pantalla.

```python
...
if rank != 0:
 comm.send(mensaje,0)
...
if rank == 0:
    for fuente in range(1,comm.Get_size()):
        mensaje_recibido = comm.recv(fuente)
        print(mensaje_recibido)
```

### ¿Qué ocurre al ejecutar el programa sólo para un procesador? ¿Por qué?

No es una ejecución paralela, y además.

El único proceso tendrá rank = 0, el número de procesos es 1, por lo que:

- Ningún proceso tiene rank != 0 => ningún proceso envía mensaje.
- El rango entre 1 y 1 está vacío y el programa termina. No se ejecuta la operación de recibir mensaje.
