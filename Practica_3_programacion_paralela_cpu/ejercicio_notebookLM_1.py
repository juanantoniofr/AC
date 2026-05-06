from mpi4py import MPI
import numpy as np

N = 100000

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# 1. Creación optimizada del array con NumPy
if rank == 0:
    # Genera el array directamente con NumPy (mucho más rápido)
    a = np.random.randint(0, 11, N, dtype='i')
else:
    a = None

# Pre-asignar buffer receptor asegurando el mismo tipo de dato
a_local = np.zeros(N // size, dtype='i')

# Scatter distribuye correctamente
comm.Scatter(sendbuf=a, recvbuf=a_local, root=0)

# 2. Uso de np.sum en lugar de sum nativo de Python
suma_local = np.sum(a_local)

# 3. Uso de allreduce para obtener la suma global en TODOS los procesos en 1 paso
suma_global = comm.allreduce(suma_local, op=MPI.SUM)

# Todos los procesos calculan la media global directamente
media_global = suma_global / N

# 4. Filtrado local optimizado con NumPy sin bucles for
contador = np.sum(a_local > media_global)

# Suma los conteos locales en el proceso 0
conteo_total = comm.reduce(contador, root=0, op=MPI.SUM)

if rank == 0:
    print("-" * 30)
    print(f"Soy el proceso {rank}")
    print(f"Suma global = {suma_global}")
    print(f"Media global = {media_global:.2f}")
    print(f"Suma total de contador (elementos > media) = {conteo_total}")
    print("-" * 30)