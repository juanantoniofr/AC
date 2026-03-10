from mpi4py import MPI

def prod_escalar_serie (a, b, primer_elemento, n):
    suma = 0.0
    for i in range(primer_elemento, primer_elemento+n):
        suma += a[i] * b[i]
    return suma

elementos = 2*2*2*2*3*3*5*7*11*13
n = elementos

# Inicializa los vectores
x = [i%5 for i in range(0,n)]
y = [i%5 for i in range(0,n)]

comm = MPI.COMM_WORLD
mi_rango = comm.Get_rank()
p = comm.Get_size()

#comm.barrier() # sincroniza a los procesos antes de la suma global
#start_time = MPI.Wtime()
# Cada proceso calcula una parte del producto escalar
n_local = n // p # división entera del número de elementos entre el número de procesos
inicio_vector_local = mi_rango * n_local
suma_local = prod_escalar_serie (x, y, inicio_vector_local, n_local)
print (f"MI RANGO = {mi_rango}, SUMA LOCAL = {suma_local}")

# Enviamos el resultado local al proceso 0 para la suma global
lista = comm.gather(suma_local, root=0)

# Suma las contribuciones calculadas por cada proceso
suma_total = 0.0
# Recorro la lista de resultados locales y los sumo
if mi_rango == 0:
    for suma_local in lista:
        suma_total += suma_local
    # Muestra el resultado por pantalla
    print (f"PRODUCTO ESCALAR USANDO p={p} TROZOS DE LOS VECTORES X e Y = {suma_total}")

#comm.barrier() # sincroniza a los procesos después de la suma global
end_time = MPI.Wtime()
#if mi_rango == 0:
#print (f"{mi_rango}: TIEMPO DE EJECUCIÓN {end_time - start_time}")
#print("---------------------------------------------")

# ¿por qué el tiempo de ejecución no disminuye al aumentar el número de procesos? Porque el tiempo de comunicación entre los procesos es mayor que el tiempo de cálculo local, especialmente para vectores pequeños. Además, la suma global en el proceso 0 también puede ser un cuello de botella.
# ¿dónde sincronizamos a los procesos? Antes de la suma global, para asegurarnos de que todos los procesos han terminado su cálculo local antes de que el proceso 0 comience a recibir las contribuciones.
# ¿Hay otro sitio donde podríamos sincronizar a los procesos? Podríamos sincronizar después de que cada proceso envíe su suma local, pero eso no es necesario en este caso porque el proceso 0 solo comenzará a recibir después de que todos los procesos hayan enviado sus sumas locales.