# integracion_trapecios_no_paralelo.py
# INTEGRACION NUMERICA POR EL METODO DE LOS TRAPECIOS
# ENTRADA: NINGUNA.
# SALIDA:  ESTIMACION DE LA INTEGRAL DESDE a HASTA b DE f(x)
# USANDO EL METODO DE LOS TRAPECIOS CON n TRAPECIOS

from mpi4py import MPI
from math import log

def f(x):
    return log(x)
    
def calcula_integral_parcial(a,b,i_inicial,i_final,n):
    integral_parcial = 0
    for i in range(i_inicial,i_final):
        integral_parcial += f(a+i*(b-a)/n)
    
    return integral_parcial

a = 1.0
b = 100000.0
n = 2*2*2*2*3*3*5*7*11*11*13
h = (b-a)/n

inicial = (f(a) + f(b))/2.0

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if n % size != 0:
    print(f"Error: n {n} debe ser divisible por el número de procesos {size}")


# Computo paralelo
numiter = (n -1) // size
i_inicial = 1 + rank * numiter
i_final =  (rank + 1) * numiter

comm.barrier()
if rank == 0:
    start_time = MPI.Wtime()

integral_parcial = calcula_integral_parcial(a,b,i_inicial,i_final,n)

# proceso cero como maestro
if rank == 0:
    integral = inicial + integral_parcial
    for fuente in range(1,size):
        integral += comm.recv(source=fuente)
    integral *= h
    end_time = MPI.Wtime()
    print (f"ESTIMACION USANDO n={n} TRAPECIOS")
    print (f"DE LA INTEGRAL DESDE {a} HASTA {b} = {integral}")
    print (f"tiempo de ejecución:  {end_time - start_time}")
else:
    comm.send(integral_parcial,dest=0)
