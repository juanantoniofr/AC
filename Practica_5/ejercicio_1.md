# Ejercicio 1

Dado el siguiente código en RISC-V.

```asm
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

## Apartado a.

Dibuje el diagrama de ejecución RISC-V **sin desvíos**.

- Primera iteración

1.  **Los bloqueos no son "huecos" ni saltos en el tiempo:** Cuando una instrucción se bloquea porque le falta un dato, **se queda atascada repitiendo su fase actual** (por ejemplo, `ID`, `ID`, `ID`) y obliga a la instrucción que viene detrás a quedarse atascada esperando en su fase anterior (`IF`, `IF`, `IF`).
2.  **Lectura y escritura en el mismo ciclo (WB / ID):** En RISC-V, las escrituras en los registros se hacen en la _primera mitad_ del ciclo (fase WB) y las lecturas en la _segunda mitad_ (fase ID). Esto significa que si una instrucción escribe en el ciclo 5, la instrucción que lee **obtiene el dato válido en ese mismo ciclo 5** y no necesita esperar al ciclo 6.
3.  **Fases WB inexistentes:** Las instrucciones de almacenamiento (`sw`) y las de salto (`blt`) **no tienen fase WB**, ya que su función es escribir en la memoria o evaluar un salto, no guardar nada en un registro de la CPU.

---

### Esta es la tabla correcta y su explicación

Para dibujar este diagrama "sin desvíos", debes aplicar rigurosamente las dependencias RAW introduciendo ciclos de bloqueo (stalls).

| Ciclo               | 1   | 2   | 3   | 4   | 5      | 6   | 7   | 8      | 9   | 10  | 11  | 12     | 13  | 14  |
| :------------------ | :-- | :-- | :-- | :-- | :----- | :-- | :-- | :----- | :-- | :-- | :-- | :----- | :-- | :-- |
| `lw a2, 0(a1)`      | IF  | ID  | EX  | MEM | **WB** |     |     |        |     |     |     |        |     |     |
| `addi a2, a2, 5`    |     | IF  | ID  | ID  | **ID** | EX  | MEM | **WB** |     |     |     |        |     |     |
| `sw a2, 0(a1)`      |     |     | IF  | IF  | IF     | ID  | ID  | **ID** | EX  | MEM |     |        |     |     |
| `addi a1, a1, 4`    |     |     |     |     |        | IF  | IF  | IF     | ID  | EX  | MEM | **WB** |     |     |
| `blt a1, a4, bucle` |     |     |     |     |        |     |     |        | IF  | ID  | ID  | **ID** | EX  | MEM |

**Análisis paso a paso de lo que ocurre en el procesador:**

1.  **`lw a2, 0(a1)`:** Fluye de forma normal de 1 a 5. Escribe su resultado en `a2` en el ciclo 5.
2.  **`addi a2, a2, 5`:** Entra en `IF` en el ciclo 2. En el ciclo 3 entra en `ID` y descubre que necesita `a2`. Como no hay desvíos, tiene que bloquearse repitiendo la etapa `ID` en los ciclos 3, 4 y 5. En el ciclo 5 consigue leer correctamente el dato porque el `lw` lo está escribiendo. Avanza a `EX` en el ciclo 6. Escribe su nuevo `a2` en el ciclo 8.
3.  **`sw a2, 0(a1)`:** Entra en `IF` en el ciclo 3. Como el `addi` se atascó en `ID`, esta instrucción se queda "haciendo tapón" repitiendo `IF` durante los ciclos 3, 4 y 5. Pasa a `ID` en el ciclo 6, donde descubre que necesita el nuevo `a2` del `addi`. Por ello, se atasca en `ID` durante los ciclos 6, 7 y 8, logrando leer `a2` en el ciclo 8. Realiza su `EX` y `MEM` en 9 y 10. No tiene `WB`.
4.  **`addi a1, a1, 4`:** Como el `sw` estuvo ocupando la etapa `IF` hasta el ciclo 5, esta instrucción recién puede entrar al cauce en el ciclo 6. Una vez dentro, se queda atascada en `IF` (6, 7, 8) haciendo tapón detrás del `sw`. En el ciclo 9 entra a `ID`, y como no depende de nadie anterior (nadie estaba modificando `a1`), fluye normal hasta su `WB` en el ciclo 12.
5.  **`blt a1, a4, bucle`:** Entra en `IF` en el ciclo 9. Pasa a `ID` en el ciclo 10 y detecta que necesita el registro `a1` que está siendo modificado. Se bloquea en `ID` (10, 11 y 12) hasta que el `addi a1` llega a `WB` en el ciclo 12. Pasa a `EX` en el 13 y a `MEM` en el 14. No tiene `WB`.
