from mpi4py import MPI 
# Establezco el comunicador global 
comm = MPI.COMM_WORLD 
# Determino el rango de este proceso 
mi_rango = comm.Get_rank() 
# Determino el numero de procesos 
p = comm.Get_size() 
if mi_rango != 0: 
    # Si no soy el proceso 0, creo el mensaje 
    mensaje = f"Saludos desde el proceso {mi_rango}" 
    # y se lo envío al proceso 0 
    comm.send (mensaje, dest=0) 
else: 
    # si soy el proceso 0, itero por todos los números de procesos (fuente) 
    print(f"Proceso {mi_rango}: Recibiendo mensajes de los otros procesos...")
    for fuente in range(1,p): 
        # Para cada fuente, recibo un mensaje desde él
        mensaje = comm.recv (source=fuente)
        # y lo imprimo 
        print (f"Mensaje recibido de {fuente}: {mensaje}")