# Realización de la práctica de laboratorio 3

## 1. instalación de mpi4py

- Para instalar mpi4py, se puede usar el siguiente comando:

```bash
pip install mpi4py
```

Con esto solo se instalará la biblioteca de Python, pero es necesario tener instalado un entorno de ejecución de MPI, como OpenMPI o MPICH, para poder usar mpi4py.

- Para instalar OpenMPI, se puede usar el siguiente comando en sistemas basados en Debian/Ubuntu:

```bash
sudo apt-get install libopenmpi-dev openmpi-bin
```

## 2. ejecución de mpi4py

- Para ejecutar el programa con mpi4py, se debe utilizar el comando `mpirun` seguido del número de procesos y el nombre del archivo Python. Por ejemplo:

```bash
mpirun -np 4 python mpi_program.py
```

- Si quiero excluir los núcleos de bajo consumo, puedo usar la opción `--bind-to` para especificar los núcleos que quiero usar. Por ejemplo, si quiero usar solo los núcleos de alto rendimiento, puedo ejecutar:

```bash
mpirun --bind-to core -np 4  python mpi_program.py
```
