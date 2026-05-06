.data
    cadena: .asciiz "CADENAENMAYUSCULAS"
.text
        # ---- `load address` -- pseudoinstrucción - al final de la ejecución el registro a1 contiene la dirección de memoria donde empieza la `cadena`
        la a1, cadena
        # ---- `load byte` carga el primer byte de `cadena` y lo guarda en a2 -> Carga `C`
cont:   lb a2, 0(a1)
        # ---- Salta a la etiqueta FIN si el registro a2 vale cero. Esto ocurre cuando lee el carácter fin de cadena '\0'
        beqz a2, FIN
        addi a2, a2, 32 # ---- convierte mayúsculas a minúsculas de caracteres ascii desde la A-Z.
        # ---- Copia el byte menos significativo de a2 en la dirección de memoria cuyo valor está en a1 (más el desplazamiento 0).
        sb a2 , 0(a1)
        addi a1, a1, 1
        j cont
FIN:

    li a7 , 10 # Syscall exit
    ecall