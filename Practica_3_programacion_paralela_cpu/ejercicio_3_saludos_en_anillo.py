# Saludos en anillo
from mpi4py import MPI

# Establezco el comunicador global
comm = MPI.COMM_WORLD
# Qué número de proceso soy?
rank = comm.Get_rank()
# Cuantos procesos hay en mi comunicador
size = comm.Get_size()
# cual es el proceso siguiente en el anillo?
siguiente = (rank + 1) % size
# cual es el proceso anterior en el anillo?
anterior = (rank - 1) % size

# cada proceso envía un mensaje a su siguiente y recibe un mensaje de su anterior
mensaje = f"Saludos desde el proceso {rank}"

# A. Se produce un deadlock porque todos los procesos están esperando a recibir un mensaje antes de enviar el suyo. 
# mensaje_recibido = comm.recv(source=anterior)
# comm.send(mensaje, dest=siguiente)

# B. intercambio de send y recv para evitar el deadlock
comm.send(mensaje, dest=siguiente)
mensaje_recibido = comm.recv(source=anterior)

# C. Qué pasa si se ejecuta un solo proceso? En ese caso, causará un deadlock.

print(f"Proceso {rank}: {mensaje_recibido}")