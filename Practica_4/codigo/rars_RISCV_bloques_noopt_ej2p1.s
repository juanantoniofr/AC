	# Llama a la función main (esta línea no es necesaria si RARS se configura para ejecutar primero el main
	j main


	# Segmento de código
	.text
	.data
A:
	.space	256
B:
	.space	256

	# Segmento de código
	.text
.globl main
main:
	# Crea el nuevo marco de pila de la función
	# Fin de la creación del nuevo marco de pila
# RISCV_bloques_noopt_ej2p1.c:10:     for (i=0; i<N; i++) {
	li	s1,0		
# RISCV_bloques_noopt_ej2p1.c:10:     for (i=0; i<N; i++) {
	j	.L2		
.L5:
# RISCV_bloques_noopt_ej2p1.c:11:         for (j=0; j<N; j++) {
	li	s2,0		
# RISCV_bloques_noopt_ej2p1.c:11:         for (j=0; j<N; j++) {
	j	.L3		
.L4:
# RISCV_bloques_noopt_ej2p1.c:12:                 B[j][i] = A[i][j];
	la	a4,A	
	slli	a5,s1,3	
	add	a5,a5,s2	
	slli	a5,a5,2	
	add	a5,a4,a5	
	lw	a4,0(a5)		
# RISCV_bloques_noopt_ej2p1.c:12:                 B[j][i] = A[i][j];
	la	a3,B	
	slli	a5,s2,3	
	add	a5,a5,s1	
	slli	a5,a5,2	
	add	a5,a3,a5	
	sw	a4,0(a5)	
# RISCV_bloques_noopt_ej2p1.c:11:         for (j=0; j<N; j++) {
	addi	s2,s2,1	
.L3:
# RISCV_bloques_noopt_ej2p1.c:11:         for (j=0; j<N; j++) {
	li	a5,7		
	ble	s2,a5,.L4	
# RISCV_bloques_noopt_ej2p1.c:10:     for (i=0; i<N; i++) {
	addi	s1,s1,1	
.L2:
# RISCV_bloques_noopt_ej2p1.c:10:     for (i=0; i<N; i++) {
	li	a5,7		
	ble	s1,a5,.L5	
# RISCV_bloques_noopt_ej2p1.c:16:     return 0;
	li	a5,0		
# RISCV_bloques_noopt_ej2p1.c:17: }
	mv	a0,a5	
	# Restaura el marco de pila anterior
	# Fin de la restauración del marco de pila

    # --- Fin del programa (Syscall Exit) ---
    li a7, 10          # Código 10: Salir
    ecall
