.data 

x:   .word 4

.text

la a1, x # x base address
addi a4, a1, 400 # x address loop end

bucle:
    lw a2, 0(a1) # x[i]
    addi a2, a2, 5 # x[i] + 5
    sw a2, 0(a1) # store back
    addi a1, a1, 4 # i++
    blt a1, a4, bucle # loop i<100

li a7 , 10 # Syscall exit
ecall