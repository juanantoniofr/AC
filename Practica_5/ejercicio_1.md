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

### - Primera iteración

1.  **Los bloqueos no son "huecos" ni saltos en el tiempo:** Cuando una instrucción se bloquea porque le falta un dato, **se queda atascada repitiendo su fase actual** (por ejemplo, `ID`, `ID`, `ID`) y obliga a la instrucción que viene detrás a quedarse atascada esperando en su fase anterior (`IF`, `IF`, `IF`).
2.  **Lectura y escritura en el mismo ciclo (WB / ID):** En RISC-V, las escrituras en los registros se hacen en la _primera mitad_ del ciclo (fase WB) y las lecturas en la _segunda mitad_ (fase ID). Esto significa que si una instrucción escribe en el ciclo 5, la instrucción que lee **obtiene el dato válido en ese mismo ciclo 5** y no necesita esperar al ciclo 6.
3.  **Fases WB inexistentes:** Las instrucciones de almacenamiento (`sw`) y las de salto (`blt`) **no tienen fase WB**, ya que su función es escribir en la memoria o evaluar un salto, no guardar nada en un registro de la CPU.

---

#### Esta es la tabla correcta y su explicación

Para dibujar este diagrama "sin desvíos", debes aplicar rigurosamente las dependencias RAW introduciendo ciclos de bloqueo (stalls).

| Ciclo                     | 1   | 2   | 3      | 4      | 5    | 6      | 7      | 8    | 9   | 10     | 11     | 12   | 13      | 14  |
| :------------------------ | :-- | :-- | :----- | :----- | :--- | :----- | :----- | :--- | :-- | :----- | :----- | :--- | :------ | :-- |
| `lw a2, 0(a1)`            | IF  | ID  | EX     | MEM    | _WB_ |        |        |      |     |        |        |      |         |     |
| `addi a2, a2, 5`          |     | IF  | **ID** | **ID** | _ID_ | EX     | MEM    | _WB_ |     |        |        |      |         |     |
| `sw a2, 0(a1)`            |     |     | **IF** | **IF** | _IF_ | **ID** | **ID** | _ID_ | EX  | MEM    |        |      |         |     |
| `addi a1, a1, 4`          |     |     |        |        |      | **IF** | **IF** | _IF_ | ID  | EX     | MEM    | _WB_ |         |     |
| `blt a1, a4, bucle`       |     |     |        |        |      |        |        |      | IF  | **ID** | **ID** | _ID_ | EX      | MEM |
| `addi a7, x0, 10`         |     |     |        |        |      |        |        |      |     | **IF** | **IF** | _IF_ | _flush_ |     |
| `lw a2, 0(a1)` (2ª iter.) |     |     |        |        |      |        |        |      |     |        |        |      | IF      | ID  |

_Nota_: `li a7, 10` es una pseudoinstrucción, se traduce en RISC-V como `addi a7, x0, 10`

**Análisis paso a paso de lo que ocurre en el procesador:**

1.  **`lw a2, 0(a1)`:** Fluye de forma normal de 1 a 5. Escribe su resultado en `a2` en el ciclo 5.
2.  **`addi a2, a2, 5`:** Entra en `IF` en el ciclo 2. En el ciclo 3 entra en `ID` y descubre que necesita `a2`. Como no hay desvíos, tiene que bloquearse repitiendo la etapa `ID` en los ciclos 3, 4 y 5. En el ciclo 5 consigue leer correctamente el dato porque el `lw` lo está escribiendo. Avanza a `EX` en el ciclo 6. Escribe su nuevo `a2` en el ciclo 8.
3.  **`sw a2, 0(a1)`:** Entra en `IF` en el ciclo 3. Como el `addi` se atascó en `ID`, esta instrucción se queda "haciendo tapón" repitiendo `IF` durante los ciclos 3, 4 y 5. Pasa a `ID` en el ciclo 6, donde descubre que necesita el nuevo `a2` del `addi`. Por ello, se atasca en `ID` durante los ciclos 6, 7 y 8, logrando leer `a2` en el ciclo 8. Realiza su `EX` y `MEM` en 9 y 10. No tiene `WB`.
4.  **`addi a1, a1, 4`:** Como el `sw` estuvo ocupando la etapa `IF` hasta el ciclo 5, esta instrucción recién puede entrar al cauce en el ciclo 6. Una vez dentro, se queda atascada en `IF` (6, 7, 8) haciendo tapón detrás del `sw`. En el ciclo 9 entra a `ID`, y como no depende de nadie anterior (nadie estaba modificando `a1`), fluye normal hasta su `WB` en el ciclo 12.
5.  **`blt a1, a4, bucle`:** Entra en `IF` en el ciclo 9. Pasa a `ID` en el ciclo 10 y detecta que necesita el registro `a1` que está siendo modificado. Se bloquea en `ID` (10, 11 y 12) hasta que el `addi a1` llega a `WB` en el ciclo 12. Pasa a `EX` en el 13 y a `MEM` en el 14. No tiene `WB`.
6.  En la arquitectura RISC-V, **la condición y el destino del salto se calculan siempre en la etapa de decodificación (`ID`)**. Veamos qué ocurre exactamente:

- 6.1. Durante los ciclos 10 y 11, `blt` está en `ID` pero no puede evaluar el salto porque el registro `a1` aún no tiene el valor correcto. Mientras tanto, `li` espera pacientemente en `IF`.
- 6.2. En el **ciclo 12**, la instrucción anterior (`addi a1, a1, 4`) escribe el nuevo valor en la fase `WB`. En ese mismo ciclo 12, la instrucción `blt` logra leer el dato en su fase `ID`, evalúa la condición de inmediato y se da cuenta de que el salto **sí se toma**.
- 6.3. Al saber en ese preciso instante que la predicción ha fallado, el procesador descarta automáticamente la instrucción equivocada que estaba en `IF`.
- 6.4. Por lo tanto, **en el ciclo 13 se produce el flush**, insertando un hueco (`nop`) en lugar de dejar que `li a7, 10` pase a la fase `ID`.En ese mismo ciclo 13, el procesador empezará a cargar en la fase `IF` la instrucción correcta (`lw a2, 0(a1)` de la segunda iteración).

### - Última iteración

| Ciclo               | 1   | 2   | 3      | 4      | 5    | 6      | 7      | 8    | 9   | 10     | 11     | 12   | 13  | 14  | 15  | 16  | 17  |
| :------------------ | :-- | :-- | :----- | :----- | :--- | :----- | :----- | :--- | :-- | :----- | :----- | :--- | :-- | :-- | :-- | :-- | :-- |
| `lw a2, 0(a1)`      | IF  | ID  | EX     | MEM    | _WB_ |        |        |      |     |        |        |      |     |     |     |     |     |
| `addi a2, a2, 5`    |     | IF  | **ID** | **ID** | _ID_ | EX     | MEM    | _WB_ |     |        |        |      |     |     |     |     |     |
| `sw a2, 0(a1)`      |     |     | **IF** | **IF** | _IF_ | **ID** | **ID** | _ID_ | EX  | MEM    |        |      |     |     |     |     |     |
| `addi a1, a1, 4`    |     |     |        |        |      | **IF** | **IF** | _IF_ | ID  | EX     | MEM    | _WB_ |     |     |     |     |     |
| `blt a1, a4, bucle` |     |     |        |        |      |        |        |      | IF  | **ID** | **ID** | _ID_ | EX  | MEM |     |     |     |
| `addi a7, x0, 10`   |     |     |        |        |      |        |        |      |     | **IF** | **IF** | _IF_ | ID  | EX  | MEM | WB  |     |
| `ecall`             |     |     |        |        |      |        |        |      |     |        |        |      | IF  | ID  | EX  | MEM | WB  |

_Nota_: `li a7, 10` es una pseudoinstrucción, se traduce en RISC-V como `addi a7, x0, 10`

## Apartado b

Calcule el **CPI (Ciclos por Instrucción)** y el **BPI (Bloqueos por Instrucción)** usando las siguientes ecuaciones:

### CPI

CPI = n_instruciones_ejecutadas + latencia_inicial + n_bloqueos / n_instrucciones_ejecutadas

### BPI

BPI = n bloqueos / n instrucciones ejecutadas

```txt

- En la fórmula para calcular el CPI, la **"latencia inicial"** se refiere al **número de ciclos de reloj necesarios para llenar el cauce (pipeline) al principio de la ejecución** antes de que la primera instrucción logre completarse y salir del procesador.

- Para entenderlo conceptualmente, recuerda que en un procesador con segmentación, el rendimiento ideal es completar una instrucción en cada ciclo de reloj. Sin embargo, esto solo ocurre **una vez que el cauce está completamente lleno**. Cuando un bloque de código comienza a ejecutarse, la primera instrucción tiene que ir avanzando etapa por etapa, y las etapas posteriores a ella están vacías y no producen resultados hasta que esa primera instrucción llega al final.

- Matemáticamente, esta latencia inicial equivale a la **profundidad del pipeline menos uno ($n - 1$)**. Dado que el procesador RISC-V segmentado que se estudia en tu asignatura tiene 5 etapas (IF, ID, EX, MEM y WB), **la latencia inicial siempre es de 4 ciclos**.
```

#### Solución

- Número de instrucciones -> 504
- Latencia inicial -> 4
- Cada dependencia de datos genera 2 ciclos de bloqueo. Dentro del bucle tenemos:
  - 1. `lw` seguido de `addi`: Dependencia de `a2`. Genera **2 bloqueos**.
  - 2. `addi` seguido de `sw`: Dependencia de `a2`. Genera **2 bloqueos**.
  - 3. `addi a1` seguido de `blt`: Dependencia de `a1`. Genera **2 bloqueos**.
- **Riesgo de control:** Como vimos, si el salto se toma (iteraciones 1 a la 99), se descarta una instrucción (flush), lo que genera **1 bloqueo** de control. Si el salto no se toma (iteración 100), hay **0 bloqueos**.

**Cálculo de bloqueos sin desvíos:**

- Iteraciones 1-99: 6 bloqueos de datos + 1 de control = **7 bloqueos por iteración** ($7 \times 99 = 693$).
- Iteración 100: 6 bloqueos de datos + 0 de control = **6 bloqueos**.
- \_**Total de bloqueos en el bucle:** $693 + 6 = \mathbf{699}$ **bloqueos**.

**Con estos datos, los resultados correctos sin desvíos serían:**

- **CPI** = (504 + 4 + 699) / 504 = 1207 / 504 = **2,39**
- **BPI** = 699 / 504 = **1,38**

### Apartado c

Aplique la planificación de instrucciones para minimizar el número de bloqueos. ¿Cuántos bloqueos de datos pueden eliminarse en cada iteración?

#### Solución

Para reducir los bloqueos sin desvíos, debes recordar **la regla de oro**: como las escrituras se hacen en la etapa WB y las lecturas en la etapa ID, **necesitas insertar al menos dos instrucciones independientes entre la instrucción que calcula un dato y la instrucción que lo necesita** para que el bloqueo se reduzca a 0 ciclos.

Para aplicar verdaderamente la planificación, el compilador (o tú como programador) debe **reordenar** el código alejando al máximo las instrucciones dependientes. La pieza clave que tienes completamente libre en tu bucle es el incremento del puntero `addi a1, a1, 8`.

Si lo **adelantas**, ganas instrucciones "gratis" de separación para los datos, y evitas el temido bloqueo doble del salto. Para hacer esto sin alterar el programa, debes reajustar los _offsets_ de los almacenamientos en memoria (`sw`) porque el puntero `a1` ya estará apuntando al siguiente bloque:

```assembly
la a1, x # x base address
addi a4, a1, 200 # x address loop end

bucle:
    lw a2, 0(a1)       # 1. Carga x[i]
    lw a3, 4(a1)       # 2. Carga x[i+1]

    addi a1, a1, 8     # 3. ADELANTAMOS el incremento del índice (i+=2)

    addi a2, a2, 5     # 4. Hay 2 instrucciones de separación con lw a2 -> ¡0 bloqueos!
    addi a3, a3, 5     # 5. Hay 2 instrucciones de separación con lw a3 -> ¡0 bloqueos!

    sw a2, -8(a1)      # 6. Guardamos x[i] (Offset compensado). 1 instr. de separación -> 1 bloqueo
    sw a3, -4(a1)      # 7. Guardamos x[i+1]. El bloqueo anterior la retrasa justo a tiempo -> 0 bloqueos

    blt a1, a4, bucle  # 8. Hay 4 instrucciones de separación con addi a1 -> ¡0 bloqueos de datos!

li a7 , 10 # Syscall exit
ecall
```

### ¿Por qué esta es la solución correcta?

Con esta reordenación óptima:

- Las cargas (`lw`) tienen tiempo suficiente de ir a memoria gracias a que intercalamos la suma del puntero (`a1`).
- La instrucción de salto (`blt`) ya tiene el registro `a1` calculadísimo y listo para cuando necesita evaluarlo en su etapa ID, borrando 2 ciclos de penalización de un plumazo.
- **Has logrado reducir los bloqueos de datos de tu iteración desenrollada de 4 ciclos a tan solo 1 ciclo** (el que sufres inevitablemente entre `addi a2` y `sw a2`).
