# Ejercicio 2.

Implemente en ensamblador el bucle desenrollado de la Sección 5.1, pero no aplique la planificación de instrucciones. Dibuje la traza de ejecución en un RISCV sin desvíos (dibuje solo la primera iteración).

## Código Sección 5.1

```assembly
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
```

## Solución

- El texto indica que le factor de desenrollado es x4.
- Cómo no hay planificación de instrucciones, no se reordenan las instrucciones, solo se replica el bloque completo.

Tal como indican los apuntes teóricos sobre el desenrollado de bucles, al procesar varios elementos en una sola iteración _"es necesario reajustar la actualización del contador del bucle [...] el incremento debe ser k en el bucle desenrollado"_.

Dado que en cada iteración de tu bucle vas a procesar 4 elementos de 4 bytes cada uno, debes dejar el puntero `a1` quieto durante toda la iteración (usando los _offsets_ 0, 4, 8 y 12 para alcanzar cada elemento) y **realizar un único incremento del puntero sumando 16 al final del bucle**.

Además, esto te ahorra ejecutar tres instrucciones `addi` innecesarias. El código correcto quedaría así:

```assembly
la a1, x # x base address
addi a4, a1, 400 # x address loop end

bucle:
    # --- Elemento 1 (x[i]) ---
    lw a2, 0(a1)
    addi a2, a2, 5
    sw a2, 0(a1)

    # --- Elemento 2 (x[i+1]) ---
    lw a2, 4(a1)
    addi a2, a2, 5
    sw a2, 4(a1)

    # --- Elemento 3 (x[i+2]) ---
    lw a2, 8(a1)
    addi a2, a2, 5
    sw a2, 8(a1)

    # --- Elemento 4 (x[i+3]) ---
    lw a2, 12(a1)
    addi a2, a2, 5
    sw a2, 12(a1)

    # --- Actualización del puntero y salto ---
    addi a1, a1, 16 # i += 4 (4 elementos x 4 bytes)
    blt a1, a4, bucle # loop i<100

li a7 , 10 # Syscall exit
ecall
```

### Traza de ejecución correcta (Primera iteración, sin desvíos)

Para que tengas la solución exacta, así es como debería quedar la tabla corrigiendo el código y eliminando los bloqueos inexistentes en las etapas ID de las instrucciones de carga:

| Ciclo               | 1   | 2   | 3   | 4   | 5      | 6   | 7   | 8      | 9   | 10  | 11  | 12     | 13  | 14  | 15     | 16  | 17  | 18  | 19     | 20  | 21  | 22     | 23  | 24  | 25  | 26     | 27  | 28  | 29     | 30  | 31  | 32  | 33     | 34  | 35  |
| :------------------ | :-- | :-- | :-- | :-- | :----- | :-- | :-- | :----- | :-- | :-- | :-- | :----- | :-- | :-- | :----- | :-- | :-- | :-- | :----- | :-- | :-- | :----- | :-- | :-- | :-- | :----- | :-- | :-- | :----- | :-- | :-- | :-- | :----- | :-- | :-- |
| `lw a2, 0(a1)`      | IF  | ID  | EX  | MEM | **WB** |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |
| `addi a2, a2, 5`    |     | IF  | ID  | ID  | **ID** | EX  | MEM | **WB** |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |
| `sw a2, 0(a1)`      |     |     | IF  | IF  | IF     | ID  | ID  | **ID** | EX  | MEM |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |
| `lw a2, 4(a1)`      |     |     |     |     |        | IF  | IF  | IF     | ID  | EX  | MEM | **WB** |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |
| `addi a2, a2, 5`    |     |     |     |     |        |     |     |        | IF  | ID  | ID  | **ID** | EX  | MEM | **WB** |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |
| `sw a2, 4(a1)`      |     |     |     |     |        |     |     |        |     | IF  | IF  | IF     | ID  | ID  | **ID** | EX  | MEM |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |
| `lw a2, 8(a1)`      |     |     |     |     |        |     |     |        |     |     |     |        | IF  | IF  | IF     | ID  | EX  | MEM | **WB** |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |
| `addi a2, a2, 5`    |     |     |     |     |        |     |     |        |     |     |     |        |     |     |        | IF  | ID  | ID  | **ID** | EX  | MEM | **WB** |     |     |     |        |     |     |        |     |     |     |        |     |     |
| `sw a2, 8(a1)`      |     |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     | IF  | IF  | IF     | ID  | ID  | **ID** | EX  | MEM |     |        |     |     |        |     |     |     |        |     |     |
| `lw a2, 12(a1)`     |     |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        | IF  | IF  | IF     | ID  | EX  | MEM | **WB** |     |     |        |     |     |     |        |     |     |
| `addi a2, a2, 5`    |     |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |        | IF  | ID  | ID  | **ID** | EX  | MEM | **WB** |     |     |     |        |     |     |
| `sw a2, 12(a1)`     |     |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     | IF  | IF  | IF     | ID  | ID  | **ID** | EX  | MEM |     |        |     |     |
| `addi a1, a1, 16`   |     |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        | IF  | IF  | IF     | ID  | EX  | MEM | **WB** |     |     |
| `blt a1, a4, bucle` |     |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |        |     |     |     |        |     |     |        | IF  | ID  | ID  | **ID** | EX  | MEM |

**Nota clave de esta traza:** Las instrucciones de carga `lw` de las réplicas posteriores no sufren bloqueos por dependencias de datos en `ID`, solo sufren bloqueos estructurales "haciendo tapón" en la etapa de búsqueda (`IF`) mientras esperan a que el `sw` anterior desocupe la etapa de decodificación.
