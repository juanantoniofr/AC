.data

cadena: .asciiz "CADENAENMAYUSCULAS"

.text
	la 	a1,  cadena 
cont: 	lb 	a2, 0(a1)
	beqz	a2, FIN
	addi	a2, a2, 32
	sb     a2 , 0(a1)
	addi	a1, a1, 1
	j	cont
FIN:
    li a7 , 10  # Syscall exit 
    ecall
