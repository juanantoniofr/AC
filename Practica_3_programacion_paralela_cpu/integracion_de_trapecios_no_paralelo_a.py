# integracion_trapecios_no_paralelo.py
# INTEGRACION NUMERICA POR EL METODO DE LOS TRAPECIOS
# ENTRADA: NINGUNA.
# SALIDA:  ESTIMACION DE LA INTEGRAL DESDE a HASTA b DE f(x)
# USANDO EL METODO DE LOS TRAPECIOS CON n TRAPECIOS

from mpi4py import MPI


def f(x):
    return (1-x*x)**0.5

def calcula_integral_parcial(a,b,i_inicial,i_final,n):
    integral_parcial = 0
    for i in range(i_inicial,i_final):
        integral_parcial += f(a+i*(b-a)/n)
    
    return integral_parcial

a = -1.0
b = 1.0
n = 100000
h = (b-a)/n

inicial = (f(a) + f(b))/2.0

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if n % size != 0:
    print(f"Error: n {n} debe ser divisible por el número de procesos {size}")


# inicializamos los datos
# Si soy el proceso p, cuáles son los valores inicial y final de la suma que me corresponde
numiter = (n -1) // size


# computo paralelo
i_inicial = 1 + rank * numiter
i_final =  (rank + 1) * numiter

integral_parcial = calcula_integral_parcial(a,b,i_inicial,i_final,n)

# proceso cero como maestro
if rank == 0:
    integral = inicial + integral_parcial
    for fuente in range(1,size):
        integral += comm.recv(source=fuente)
    integral *= h

    print (f"ESTIMACION USANDO n={n} TRAPECIOS")
    print (f"DE LA INTEGRAL DESDE {a} HASTA {b} = {integral}")
    print (f"ESTIMACION DE PI: {2*integral}")
else:
    comm.send(integral_parcial,dest=0)

