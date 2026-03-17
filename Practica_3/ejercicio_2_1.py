from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = 10_000_000


# ---------- Apartado A ----------
# ---------- Preparación de Datos ----------
if rank == 0:
    # Generamos los datos fuera del cronómetro (simulando carga de disco/input) 
    vector = np.random.rand(N)
    vector_size = vector.size
    cuadrados = np.square(vector)  
    bloques = np.array_split(vector, size)
    bloques_cuadrados = np.array_split(cuadrados, size)
    
else:
    vector = None
    bloques = None # Inicializamos variable para el bloque secuencial
    bloques_cuadrados = None

# Sincronizamos todos los procesos antes de empezar a medir
comm.Barrier()


# ==========================================
# INICIO MEDICIÓN PARALELA
# ==========================================
t_inicio_par = MPI.Wtime()

# 1. Distribuir
bloque_local = comm.scatter(bloques, root=0)
bloques_cuadrados_local = comm.scatter(bloques_cuadrados, root=0)


# ---------- Apartado B ----------
# 2. Computar Localmente
suma_local = np.sum(bloque_local)
max_local = np.max(bloque_local)
min_local = np.min(bloque_local)
suma_local_cuadrados = np.sum(bloques_cuadrados_local)



# ---------- Apartado C ----------
# 3. Reducir (Comunicación global)
suma_total = comm.reduce(suma_local, op=MPI.SUM, root=0)
max_total = comm.reduce(max_local, op=MPI.MAX, root=0)
min_total = comm.reduce(min_local, op=MPI.MIN, root=0)
suma_total_cuadrados = comm.reduce(suma_local_cuadrados, op=MPI.SUM, root=0)

# -------- Disviación típica -----
if rank == 0:
    media_aritmetica_cuadrado = (suma_local / vector_size )**2
    std = ((suma_local_cuadrados / vector.size) - media_aritmetica_cuadrado)**0.5

# ---------- Apartado D ----------
# 4. Cálculo Final en Root
if rank == 0:
    media = suma_total / N

t_fin_par = MPI.Wtime()

# ==========================================
# FIN MEDICIÓN PARALELA
# ==========================================


if rank == 0:
    tiempo_paralelo = t_fin_par - t_inicio_par
    
    print("-" * 30)
    print(f"Resultados (N={N}):")
    print(f"Media: {media:.4f}")
    print(f"Máx:   {max_total:.4f} | Mín: {min_total:.4f}")
    print(f"Std: {std:.4f}")
    print("-" * 30)

    # ==========================================
    # MEDICIÓN SECUENCIAL (SOLO EN ROOT)
    # ==========================================
    t_inicio_sec = MPI.Wtime()
    
    # NumPy está altamente optimizado en C, es un rival difícil
    s_sec = np.sum(vector)
    max_sec = np.max(vector)
    min_sec = np.min(vector)
    desv_sec = np.std(vector) # Calcula media internamente
    
    t_fin_sec = MPI.Wtime()
    tiempo_secuencial = t_fin_sec - t_inicio_sec

    # ==========================================
    # COMPARATIVA Y SPEEDUP
    # ==========================================
    speedup = tiempo_secuencial / tiempo_paralelo

    print(f"Tiempo Paralelo ({size} procs): {tiempo_paralelo:.6f} seg")
    print(f"Tiempo Secuencial:          {tiempo_secuencial:.6f} seg")
    print("-" * 30)
    print(f"Speedup: {speedup:.2f}x")
    
    if speedup > 1:
        print(">> El cálculo paralelo fue más rápido.")
    else:
        print(">> El cálculo secuencial fue más rápido (Overhead de comunicación).")

