	# Llama a la función main (esta línea no es necesaria si RARS se configura para ejecutar primero el main
	j main


	# Segmento de código
	.text
	.data
A:
	.space	4096

	# Segmento de código
	.text
.globl main
main:
	# Crea el nuevo marco de pila de la función
	# Fin de la creación del nuevo marco de pila
# RISCV_intercambio_ej1p3.c:9:   for (i=0; i<N; i++)
	li	s1,0		
# RISCV_intercambio_ej1p3.c:9:   for (i=0; i<N; i++)
	j	.L2		
.L5:
# RISCV_intercambio_ej1p3.c:10: 	  for (j=0; j<N; j++)
	li	s2,0		
# RISCV_intercambio_ej1p3.c:10: 	  for (j=0; j<N; j++)
	j	.L3		
.L4:
# RISCV_intercambio_ej1p3.c:11: 		  A[i][j]= 1917;
	la	a4,A	
	slli	a5,s1,5	
	add	a5,a5,s2	
	slli	a5,a5,2	
	add	a5,a4,a5	
	li	a4,1917		
	sw	a4,0(a5)	
# RISCV_intercambio_ej1p3.c:10: 	  for (j=0; j<N; j++)
	addi	s2,s2,1	
.L3:
# RISCV_intercambio_ej1p3.c:10: 	  for (j=0; j<N; j++)
	li	a5,31		
	ble	s2,a5,.L4	
# RISCV_intercambio_ej1p3.c:9:   for (i=0; i<N; i++)
	addi	s1,s1,1	
.L2:
# RISCV_intercambio_ej1p3.c:9:   for (i=0; i<N; i++)
	li	a5,31		
	ble	s1,a5,.L5	
# RISCV_intercambio_ej1p3.c:13:       return(0);
	li	a5,0		
# RISCV_intercambio_ej1p3.c:14: }
	mv	a0,a5	
	# Restaura el marco de pila anterior
	# Fin de la restauración del marco de pila

    # --- Fin del programa (Syscall Exit) ---
    li a7, 10          # Código 10: Salir
    ecall
