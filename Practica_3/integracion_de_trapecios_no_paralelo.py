# integracion_trapecios_no_paralelo.py
# INTEGRACION NUMERICA POR EL METODO DE LOS TRAPECIOS
# ENTRADA: NINGUNA.
# SALIDA:  ESTIMACION DE LA INTEGRAL DESDE a HASTA b DE f(x)
# USANDO EL METODO DE LOS TRAPECIOS CON n TRAPECIOS

from mpi4py import MPI
import numpy as np

def f(x):
    return (1-x*x)**0.5

def calcula_integral_parcial(a,b,vector):
    n = len(vector)
    for i in vector:
        integral_parcial += f(a+i*(b-a)/n)
    
    return np.array([integral_parcial])

a = -1.0
b = 1.0
n = 100000
h = (b-a)/n

integral = (f(a) + f(b))/2.0

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if n % size != 0:
    printf(f"Error: n {n} debe ser divisible por el número de procesos {size}")

# Cuantas filas por porceso
filas = n // size

# inicializamos los datos
vector = np.arange(1,n+1)
integral_local = np.empty(1)
integrales_parciales = np.empty(filas)

# distribuimos
comm.Scatter(vector, integrales_parciales, root=0)

# Computo paralelo
integral_local = calcula_integral_parcial(a,b,vector)

# Recibimos los datos

comm.Gather(integral_local, integrales_parciales, root=0)

#integral *= h
print(integrales_parciales)
#print (f"ESTIMACION USANDO n={n} TRAPECIOS")
#print (f"DE LA INTEGRAL DESDE {a} HASTA {b} = {integral}")
#print (f"ESTIMACION DE PI: {2*integral}")