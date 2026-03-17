# hola mundo con mpi4py (Programación Paralela con Python)
from mpi4py import MPI

# Establezco el comunicador global
comm = MPI.COMM_WORLD
# Qué número de proceso soy?
rank = comm.Get_rank()
# Cuantos procesos hay en mi comunicador
size = comm.Get_size()
# Obtengo el nombre del procesador
name = MPI.Get_processor_name()

print(f"Hola mundo, soy el proceso {rank} de {size} y mi nombre es {name}")