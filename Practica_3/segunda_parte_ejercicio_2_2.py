from mpi4py import MPI
import numpy as np
import time
import sys

# Función auxiliar para validación (ejecución secuencial pura)
def matriz_mul_secuencial(A, B):
    return np.dot(A, B)

def main():
    # 1. Inicialización del entorno MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # Identificador del proceso actual
    size = comm.Get_size()  # Número total de procesos

    # Definimos el tamaño de la matriz (N x N)
    # N = 1000 es un buen balance para ver tiempos sin esperar demasiado
    N = 1000 

    # IMPORTANTE: Para este ejercicio básico, asumimos que N es divisible por size.
    # En un caso real, habría que usar Scatterv/Gatherv para trozos desiguales.
    if N % size != 0:
        if rank == 0:
            print(f"Error: N ({N}) debe ser divisible por el número de procesos ({size}).")
        sys.exit(0)

    # Calculamos cuántas filas manejará cada proceso (Chunk Size)
    filas_locales = N // size

    # -------------------------------------------------------------------------
    # PARTE 1: Inicialización de Datos (Solo en el proceso Maestro)
    # -------------------------------------------------------------------------
    if rank == 0:
        print(f"--- Iniciando multiplicación {N}x{N} con {size} procesos ---")
        # dtype='d' asegura double precision (float64)
        A = np.random.rand(N, N).astype('d')
        B = np.random.rand(N, N).astype('d')
        # Matriz vacía para recibir el resultado final
        C_final = np.empty((N, N), dtype='d')
        
        start_time = time.time()
    else:
        # Los esclavos no necesitan tener la Matriz A completa, solo su trozo.
        # Pero sí necesitan espacio para recibir la Matriz B completa.
        A = None
        B = np.empty((N, N), dtype='d') 
        C_final = None

    # -------------------------------------------------------------------------
    # PARTE 2: Distribución de Datos (Comunicación)
    # -------------------------------------------------------------------------
    
    # 2.1 Broadcast de B
    # Enviamos la matriz B completa desde root=0 a todos los procesos.
    # Es crucial que B esté pre-alocada en los esclavos antes de llamar a Bcast.
    comm.Bcast(B, root=0)

    # 2.2 Scatter de A
    # Preparamos el buffer local para recibir el trozo de filas de A.
    # Dimensiones: (filas_locales x N)
    A_local = np.empty((filas_locales, N), dtype='d')
    
    # Repartimos A. MPI toma A del root, lo divide en trozos iguales y
    # envía cada trozo al buffer A_local de cada proceso.
    comm.Scatter(A, A_local, root=0)

    # -------------------------------------------------------------------------
    # PARTE 3: Cómputo Paralelo
    # -------------------------------------------------------------------------
    
    # Sincronización opcional para asegurar que todos empiezan el cálculo a la vez
    comm.Barrier() 
    
    # Realizamos la multiplicación local.
    # (filas_locales x N) dot (N x N)Resulta en -> (filas_locales x N)
    # NumPy usa BLAS internamente, por lo que esto ya es muy rápido por núcleo.
    # t_inicio_calculo = time.time()
    C_local = np.dot(A_local, B)
    # t_fin_calculo = time.time()

    # (Opcional) Imprimir tiempo de cálculo por proceso para ver balanceo de carga
    # print(f"Proceso {rank} terminó cálculo en {t_fin_calculo - t_inicio_calculo:.4f}s")

   
    # -------------------------------------------------------------------------
    # PARTE 4: Recolección de Resultados (Comunicación) (RELLENAR ALUMNOS)
    # -------------------------------------------------------------------------
    # Objetivo: Normalizar la matriz resultado C para que todos sus valores 
    # estén entre 0 y 1.
    # Fórmula: C_norm = (C - Min_Global) / (Max_Global - Min_Global)
    
    # RETO:
    # 1. C_local solo tiene una parte de los datos.
    # 2. Tenéis que encontrar el Mínimo y Máximo de TODA la matriz C,
    #    sin reunir todavía la matriz en el maestro (sería ineficiente).
    # 3. Una vez tengáis Min_Global y Max_Global en TODOS los procesos,
    #    aplicad la fórmula a vuestro C_local.
    
    # PISTA: Buscad en la documentación de MPI las operaciones de reducción 
    # (Reduce, Allreduce) y los operadores (MPI.MIN, MPI.MAX).

    # --- ESCRIBIR CÓDIGO AQUÍ ---
    print(f"C_local: {C_local.shape}")
    
    min_local = np.min(C_local)
    max_local = np.max(C_local)
    
    lista_minimos = comm.gather(min_local, root=0)
    lista_maximos = comm.gather(max_local, root=0)
    # el proceso 0 calcula el minimo total
    if rank == 0:
        min_total = np.min(lista_minimos)
        max_total = np.max(lista_maximos)
        print(f"Mínimo total: {min_total:.4f}")
        print(f"Máximo total: {max_total:.4f}")
    
    comm.Gather(C_local,C_final,root=0)
    if rank == 0:
        C_norm = (C_final - min_total) / (max_total - min_total)
        print(f"C_norm: {C_norm.shape}")
        print(F"Máximo y mínimo de C_norm: {np.max(C_norm)} - {np.min(C_norm)}")
    # -------------------------------------------------------------------------
    # PARTE 5: Recolección (Modificado)
    # -------------------------------------------------------------------------
    # Ahora reunimos la matriz A
    # Reunimos los trozos C_local en C_final en el root.
    # MPI toma C_local de cada proceso y los pega en orden en C_final.
    comm.Gather(C_local, C_final, root=0)



    # -------------------------------------------------------------------------
    # PARTE 6: Validación y Resultados (Solo Maestro)
    # -------------------------------------------------------------------------
    if rank == 0:
        end_time = time.time()
        tiempo_total = end_time - start_time
        print(f"Tiempo Total Paralelo: {tiempo_total:.4f} segundos")

        # Validación: Solo si la matriz no es gigantesca (por tiempo)
        if N <= 1000:
            print("Validando resultado con cálculo secuencial...")
            start_seq = time.time()
             # 1. Cálculo secuencial base
            C_check = matriz_mul_secuencial(A, B)
           
            # 2. Normalizar el resultado secuencial. Descomentar cuando se haya resuelto problema.
            #min_check = np.min(C_check)
            # max_check = np.max(C_check)
            # C_check = (C_check - min_check) / (max_check - min_check)

            end_seq = time.time()
            print(f"Tiempo Secuencial (un solo núcleo): {end_seq - start_seq:.4f} segundos")

            # np.allclose es mejor que == por errores de redondeo en flotantes
            if np.allclose(C_final, C_check):
                print(">> ÉXITO: El resultado paralelo es correcto.")
                print(f">> Speedup aproximado: {(end_seq - start_seq)/tiempo_total:.2f}x")
            else:
                print(">> ERROR: Los resultados no coinciden.")
        else:
            print("Validación omitida por tamaño de matriz.")

if __name__ == "__main__":
    main()