## Código en c

```c
int x = 4;
int res = 0;

int main () {
    if ( x <= 2) {
        res = 20;
    }
    else {
        res = 10;
    }
}
```

## Código ensamblador

```asm

.data

# Reserva 4 bytes de memoria, guarda el valor 4, y llámalo x
x:
    .word 4

# Define una etiqueta llamada res, pero sin reservar memoria
res:
    .space 0


.text

.globl main

main:
    #--- inicio (gestión de pila) ---
    addi sp, sp -16
    sw s0, 12(sp)
    addi s0, sp, 16

    #---Condición: if(x <= 2)--
    la a5,x # Cargar dirección de x
    lw a4,0(a5) # Cargar valor de x
    li a5,2 # Cargar constante 2
    bgt a4,a5,.L2 # Si (x > 2) ir a ELSE (.L2)

    #---Cuerpo del IF: res = 20--
    la a5,res
    li a4,20
    sw a4,0(a5) # Guardar 20 en res
    j .L3 # Saltar al final

.L2:
    #---Cuerpo del ELSE: res = 10--
    la a5,
    res li a4,10
    sw a4,0(a5) # Guardar 10 en res

.L3:
    #---Salida--
    li a5,0
    mv a0,a5
    lw s0,12(sp)
    addi sp,sp,16

    li a7, 10 # Syscall Exit
    ecall

```
