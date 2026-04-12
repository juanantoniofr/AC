# integracion_trapeciosparalelo.py
from mpi4py import MPI
from math import log

def f(x):
    return log(x)
    #return (1-x*x)**0.5

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

a = 1.0
b = 100000.0
n =  7927920
h = (b-a)/n
integral_parcial = 0

# Qué iteraciones tengo que calcular?
iteracion_inicial = 1 + (rank * (n - 1)) // size
iteracion_final = ( (rank + 1) * (n -1) ) // size

comm.barrier()
start_time = MPI.Wtime()
for i in range(iteracion_inicial,iteracion_final):
        integral_parcial += f(a+i*(b-a)/n)


if rank == 0:
    integral = (f(a) + f(b))/2.0
    calculo_esclavos = 0
    for fuente in range(1,size): 
        calculo_esclavos += comm.recv(source=fuente)
    integral = integral_parcial + calculo_esclavos
    integral *= h
    end_time = MPI.Wtime()
    print (f"ESTIMACION USANDO n={n} TRAPECIOS")
    print (f"DE LA INTEGRAL DESDE {a} HASTA {b} = {integral}")
    print (f"ESTIMACION DE PI: {2*integral:.2f}")
    print(f"Tiempo total: {(end_time - start_time):.2f}")    
else:
    comm.send(integral_parcial, 0)

