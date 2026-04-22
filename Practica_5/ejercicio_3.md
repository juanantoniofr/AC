# Ejercicio 3.

- 3.1 Aplique la planificación de instrucciones al código del Ejercicio 2 para eliminar el mayor número de bloqueos posible.Dibuje la traza de ejecución en un RISCV sin desvíos,
  indicando los bloqueos que se producen (dibuje solo la primera iteración y la última).
- 3.2 Calcule el CPI, el BPI y la aceleración conseguida respecto al código original.
- 3.3 ¿Qué bloqueos no han podido ser eliminados?
- 3.4¿Por qué?
- 3.5 Finalmente, compruebe utilizando el simulador RISCV que los resultados obtenidos son correctos.

## Código ejercicio 2

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

## Aplicamos planificación de instrucciones

Lamentablemente, tu propuesta **no es correcta**. Contiene errores tanto a nivel de lógica de programación como a nivel del concepto de "planificación de instrucciones" (instruction scheduling) que se exige en la asignatura.

Has cometido dos errores principales:

1.  **Error lógico en memoria (igual que te ocurrió en el Ejercicio 2):** Al hacer `addi a1, a1, 4` en medio de cada bloque y luego usar los desplazamientos estáticos (`8(a1)`, `12(a1)`), estás sumando el avance dos veces. Terminarías guardando los datos en posiciones incorrectas de la memoria, corrompiendo el vector `x`.
2.  **No hay verdadera planificación:** Sigues teniendo la instrucción que consume un dato (`addi a2, a2, 5`) pegada inmediatamente después de la instrucción que lo carga (`lw a2, 0(a1)`). Como estamos asumiendo un procesador **sin desvíos**, esto te seguirá provocando **2 ciclos de bloqueo por cada elemento**, es decir, no has eliminado los bloqueos.

### La clave de la Planificación de Instrucciones (Ejercicio 3)

Para planificar correctamente un bucle desenrollado y eliminar los bloqueos, debes hacer tres cosas:

1.  **Usar un registro temporal diferente** para cada elemento del vector (ej. `t1, t2, t3, t4`).
2.  **Agrupar las instrucciones por tipo:** Ponemos todas las cargas juntas (`lw`), luego toda la aritmética (`addi`), y luego todos los almacenamientos (`sw`).
3.  **Adelantar el incremento del puntero (`a1`):** Lo sumamos todo de golpe (`+16`) lo antes posible para separar su cálculo de la instrucción de salto (`blt`), y compensamos los _offsets_ en los `sw`.

### Solución

```assembly
la a1, x # x base address
addi a4, a1, 400 # x address loop end

bucle:
    # 1. CARGAS: Cargamos los 4 elementos en registros distintos
    lw t1, 0(a1)
    lw t2, 4(a1)
    lw t3, 8(a1)
    lw t4, 12(a1)

    # 2. PUNTERO: Adelantamos el incremento total del índice (i += 4 elementos)
    # Hacerlo aquí nos da instrucciones "gratis" de separación para los datos
    addi a1, a1, 16

    # 3. ARITMÉTICA: Sumamos 5 a cada registro
    # Entre 'lw t1' y 'addi t1' ahora hay 4 instrucciones en medio -> ¡0 bloqueos!
    addi t1, t1, 5
    addi t2, t2, 5
    addi t3, t3, 5
    addi t4, t4, 5

    # 4. ALMACENAMIENTO: Guardamos usando offsets negativos para compensar el '+16'
    # Entre 'addi t1' y 'sw t1' hay 3 instrucciones en medio -> ¡0 bloqueos!
    sw t1, -16(a1)
    sw t2, -12(a1)
    sw t3, -8(a1)
    sw t4, -4(a1)

    # 5. CONTROL: Salto condicional
    # Entre la actualización de 'a1' y este 'blt' hay 8 instrucciones -> ¡0 bloqueos de datos!
    blt a1, a4, bucle # loop i<100

li a7 , 10 # Syscall exit
ecall
```

## Traza sin desvíos, primera iteración

| Ciclo             | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  | 11  | 12  | 13  | 14  | 15  | 16  | 17  | 18  |
| :---------------- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| `lw t1, 0(a1)`    | IF  | ID  | EX  | MEM | WB  |     |     |     |     |     |     |     |     |     |     |     |     |     |
| `lw t2, 4(a1)`    |     | IF  | ID  | EX  | MEM | WB  |     |     |     |     |     |     |     |     |     |     |     |     |
| `lw t3, 8(a1)`    |     |     | IF  | ID  | EX  | MEM | WB  |     |     |     |     |     |     |     |     |     |     |     |
| `lw t4, 12(a1)`   |     |     |     | IF  | ID  | EX  | MEM | WB  |     |     |     |     |     |     |     |     |     |     |
| `addi t1, a1, 16` |     |     |     |     | IF  | ID  | EX  | MEM | WB  |     |     |     |     |     |     |     |     |     |
| `addi t2, t1, 5`  |     |     |     |     |     | IF  | ID  | EX  | MEM | WB  |     |     |     |     |     |     |     |     |
| `addi t3, t2, 5`  |     |     |     |     |     |     | IF  | ID  | EX  | MEM | WB  |     |     |     |     |     |     |     |
| `addi t4, t3, 5`  |     |     |     |     |     |     |     | IF  | ID  | EX  | MEM | WB  |     |     |     |     |     |     |
| `sw t1, -16(a1)`  |     |     |     |     |     |     |     |     | IF  | ID  | EX  | MEM |     |     |     |     |     |     |
| `sw t2, -12(a1)`  |     |     |     |     |     |     |     |     |     | IF  | ID  | EX  | MEM |     |     |     |     |     |
| `sw t3, -8(a1)`   |     |     |     |     |     |     |     |     |     |     | IF  | ID  | EX  | MEM |     |     |     |     |
| `sw t4, -4(a1)`   |     |     |     |     |     |     |     |     |     |     |     | IF  | ID  | EX  | MEM |     |     |     |
| `blt a1, a4`      |     |     |     |     |     |     |     |     |     |     |     |     | IF  | ID  | EX  |     |     |     |
|                   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|                   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|                   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|                   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
