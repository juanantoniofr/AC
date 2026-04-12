# hola mundo con mpi4py (Programación Paralela con Python)
import os
from mpi4py import MPI
import time

# Establezco el comunicador global
comm = MPI.COMM_WORLD
# Qué número de proceso soy?
rank = comm.Get_rank()
# Cuantos procesos hay en mi comunicador
size = comm.Get_size()
# Obtengo el nombre del procesador
name = MPI.Get_processor_name()

# Lanzamos más procesos que el número de procesadores disponibles
num_procesadores = os.cpu_count()
start_time = MPI.Wtime()
# trabajo tonto
s = sum(i*i for i in range(50_000_000))
end_time = MPI.Wtime()
print(f"Tiempo de ejecución del proceso {rank}: {end_time - start_time} segundos")