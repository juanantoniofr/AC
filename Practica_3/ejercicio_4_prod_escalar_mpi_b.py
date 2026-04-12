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

comm.barrier() # sincroniza a los procesos antes de la suma global
start_time = MPI.Wtime()

# Cada proceso calcula una parte del producto escalar
n_local = n // p # división entera del número de elementos entre el número de procesos
inicio_vector_local = mi_rango * n_local
suma_local = prod_escalar_serie (x, y, inicio_vector_local, n_local)



if mi_rango == 0:
    # Suma las contribuciones calculadas por cada proceso
    suma_total = suma_local
    for fuente in range(1,p):
        suma_local = comm.recv (source=fuente)
        suma_total += suma_local
    # Muestra el resultado por pantalla
    print (f"PRODUCTO ESCALAR USANDO p={p} TROZOS DE LOS VECTORES X e Y = {suma_total}")

else:
    comm.send (suma_local, dest=0)

comm.barrier() # sincroniza a los procesos después de la suma global
end_time = MPI.Wtime()
if mi_rango == 0:
    print (f"{mi_rango}: TIEMPO DE EJECUCIÓN {end_time - start_time}")
    print(f"-" * 20)

