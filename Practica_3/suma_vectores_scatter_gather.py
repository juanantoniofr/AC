from mpi4py import MPI
import random
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

numelementos = 1024  # 2^10 elementos

a = [1 for _ in range(numelementos)]
b = [1 for _ in range(numelementos)]

trozos_a = []
trozos_b = []
# Calcular tamaño base y resto
tamaño_trozo = numelementos // size
resto = numelementos % size

# El root divide el trabajo a partes iguales
if rank == 0:   
    trozo_divisible_a = a[:-resto]
    trozo_divisible_b = b[:-resto]
    for i in range(0,size):
        trozos_a.append(a[(i)*tamaño_trozo:tamaño_trozo*(i+1)])
        trozos_b.append(b[(i)*tamaño_trozo:tamaño_trozo*(i+1)])
        
    print(f"Soy el proceso {rank} y la longitud del vector a procesar en {len(trozos_a)}")

    
# scatter devuelve un trozo del tabajo total a cada proceso
trozo_local_a = comm.scatter(trozos_a,root=0)
trozo_local_b = comm.scatter(trozos_b,root=0)
print(f"Soy el proceso {rank} y la longitud del vector a procesar es {len(trozo_local_a)}")
# cada proceso realiza su suma
suma_local_a = sum(trozo_local_a)
suma_local_b = sum(trozo_local_b)      

# Todos los procesos envían con Gather sus resultados y el root los recibe en una lista ordenada
lista_sumas = comm.gather([suma_local_a,suma_local_b],root=0)
if rank == 0:
    print(f"Soy el proceso {rank} y la longitud de la lista de sumas es {len(lista_sumas)}")    
    suma_total_a = sum([suma[0] for suma in lista_sumas])
    suma_total_b = sum([suma[1] for suma in lista_sumas])
    resto_a = sum(a[-resto:]) if resto > 0 else 0
    resto_b = sum(b[-resto:]) if resto > 0 else 0
    suma_total_a += resto_a
    suma_total_b += resto_b
    print(f"Suma total de a: {suma_total_a}")
    print(f"Suma total de b: {suma_total_b}")
# Aplanar la lista
#c_flat = [item for sublist in lista_sumas for item in sublist]
#print(c_flat)


    