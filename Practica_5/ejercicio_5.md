# Ejercicio 5.

Sea el siguiente fragmento de código, que convierte una cadena de caracteres en mayúscula a minúscula:

```assembly
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
```

## - a. Dibuje en papel el diagrama de ejecución para un RISCV sin ningún tipo de desvío. Dibuje solo la primera iteración y la última.

**primera iteración**

| CICLO                  | C1  | C2  | C3     | C4     | C5   | C6     | C7     | C8   | C9  | C10    | C11    | C12  | C13 | C14 | C15     | C16 | C17 |
| ---------------------- | --- | --- | ------ | ------ | ---- | ------ | ------ | ---- | --- | ------ | ------ | ---- | --- | --- | ------- | --- | --- |
| `la a1, cadena`        | IF  | ID  | EX     | MEM    | _WB_ |        |        |      |     |        |        |      |     |     |         |     |     |
| `cont:   lb a2, 0(a1)` |     | IF  | **ID** | **ID** | _ID_ | EX     | MEM    | _WB_ |     |        |        |      |     |     |         |     |     |
| `beqz a2, FIN`         |     |     | IF     | IF     | _IF_ | **ID** | **ID** | _ID_ | EX  | MEM    | WB     |      |     |     |         |     |     |
| `addi a2, a2, 32`      |     |     |        |        |      | IF     | IF     | _IF_ | ID  | EX     | MEM    | _WB_ |     |     |         |     |     |
| `sb a2 , 0(a1)`        |     |     |        |        |      |        |        |      | IF  | **ID** | **ID** | _ID_ | EX  | MEM | WB      |     |     |
| `addi a1, a1, 1`       |     |     |        |        |      |        |        |      |     | IF     | IF     | _IF_ | ID  | EX  | MEM     | WB  |     |
| `j cont`               |     |     |        |        |      |        |        |      |     |        |        |      | IF  | ID  | EX      | MEM | WB  |
| `li a7 , 10`           |     |     |        |        |      |        |        |      |     |        |        |      |     | IF  | _flush_ |     |     |
| `cont:   lb a2, 0(a1)` |     |     |        |        |      |        |        |      |     |        |        |      |     |     | IF      | ID  | EX  |

**última iteración**

| CICLO                  | C1  | C2  | C3     | C4     | C5   | C6      | C7  | C8  | C9  | C10 | C11 |
| ---------------------- | --- | --- | ------ | ------ | ---- | ------- | --- | --- | --- | --- | --- |
| `cont:   lb a2, 0(a1)` | IF  | ID  | EX     | MEM    | _WB_ |         |     |     |     |     |     |
| `beqz a2, FIN`         |     | IF  | **ID** | **ID** | _ID_ | EX      | MEM | WB  |     |     |     |
| `addi a2, a2, 32`      |     |     | IF     | IF     | IF   | _flush_ |     |     |     |     |     |
| `li a7 , 10`           |     |     |        |        |      | IF      | ID  | EX  | MEM | WB  |     |
| `ecall`                |     |     |        |        |      |         | IF  | ID  | EX  | MEM | WB  |
|                        |     |     |        |        |      |         |     |     |     |     |     |
|                        |     |     |        |        |      |         |     |     |     |     |     |
|                        |     |     |        |        |      |         |     |     |     |     |     |

_NOTA_: La arquitectura base sobre la que se trabaja ya incorpora esta mejora, estableciendo de forma general que "la condición y destino del salto se calculan **en la fase ID**"

**- b ¿En cuántos ciclos se ejecuta este bucle?**

Para calcular el tiempo total en un procesador segmentado, no debemos mirar cuándo termina la etapa `WB` de una iteración, sino el **ritmo o intervalo de inicio** (cuántos ciclos pasan desde que el `lb`
de una iteración entra en `IF` hasta que entra el `lb` de la siguiente).

Vamos a calcular el número exacto de ciclos paso a paso basándonos en las reglas de sin desvíos de tus tablas:

**1. El arranque inicial (`la a1, cadena`)**
Esta instrucción entra en el ciclo 1 y ocupa esa ranura de tiempo inicial.

- **Total temporal:** 1 ciclo.

**2. La primera iteración (1 iteración)**
El `lb` de la primera iteración entra en el ciclo 2. Como vimos en la tabla, sufre 2 ciclos de bloqueo esperando al registro `a1`. Esto retrasa en cadena todo el bloque. El salto final `j cont` se evalúa en el ciclo 14, lanzando la siguiente iteración en el ciclo 15.
Por tanto, la distancia real que "cuesta" esta primera iteración es del ciclo 2 al 14.

- **Total temporal:** 13 ciclos.

**3. Las iteraciones regulares (17 iteraciones)**
De la iteración 2 a la 18 (un total de 17 letras), el `lb` entra limpio porque ya no tiene que esperar a `la`. Si haces el recorrido exacto, cada iteración sufre 2 bloqueos de datos para `beqz`, 2 bloqueos de datos para `sb` y 1 bloqueo de control por el salto. Esto significa que el salto `j cont` evalúa la vuelta cada 11 ciclos. Es decir, una nueva iteración entra al procesador **cada 11 ciclos**.

- **Total temporal:** 17 iteraciones × 11 ciclos = 187 ciclos.

En un procesador ideal, si el bucle tiene 6 instrucciones, tardaría 6 ciclos en lanzar la siguiente iteración. Pero como estamos sin desvíos, hay que sumar los bloqueos matemáticamente:

- 6 ciclos ideales (uno por cada instrucción: lb, beqz, addi, sb, addi, j).
- +2 ciclos de bloqueo RAW porque beqz necesita el registro a2 que carga lb. (Tienen que esperar a que lb llegue a la etapa WB).
- +2 ciclos de bloqueo RAW porque sb necesita el registro a2 que calcula addi a2, a2, 32.
- +1 ciclo de bloqueo de control provocado por el salto incondicional j cont (que evalúa su destino en la etapa ID descartando la instrucción que entra detrás).

(_Nota_: El addi a1, a1, 1 no sufre bloqueos porque su dependencia es con la iteración anterior, y el dato se calculó muchos ciclos atrás).
**Suma total: 6 (ideales) + 2 (datos) + 2 (datos) + 1 (control) = 11 ciclos exactos entre una iteración y la siguiente.**

**4. La última iteración (1 iteración nula) y salida**
El `lb` del carácter nulo empieza en el ciclo 202. Aquí el salto `beqz` se toma. Se descarta la suma, salta a la etiqueta `FIN`, ejecuta el `li` y termina con la etapa `WB` de la instrucción `ecall`. Como bien dedujiste de la tabla del mensaje anterior, todo este proceso de vaciado final hasta terminar el programa dura exactamente **11 ciclos** (del 202 al 212).

- **Total temporal:** 11 ciclos.

### Cálculo Final Correcto

Si sumamos el tiempo real de solapamiento de cada fase:
Total = 1 (arranque) + 13 (iteración 1) + 187 (iteraciones 2-18) + 11 (salida) = **212 ciclos**.

**Conclusión:** El bucle completo y la finalización del programa se ejecutan en **212 ciclos**, un número bastante menor a 317, demostrando precisamente la gran ventaja de rendimiento que aporta solapar instrucciones en un procesador segmentado.

## - b. Repita el apartado (a) suponiendo que el RISCV tiene todos los desvíos posibles.

_NOTA:_
**¿En qué fase de la instrucción posterior se puede inyectar el dato?**

Aunque inyectar el dato en la etapa de Ejecución (**EX**) es lo más habitual (ya que allí se encuentra la ALU y la mayoría de las instrucciones necesitan los operandos para realizar cálculos o calcular direcciones de memoria), el destino del desvío depende estrictamente de **en qué etapa necesita físicamente el dato la instrucción que lo va a consumir**.

Las fuentes teóricas y los ejercicios de tu asignatura contemplan dos excepciones muy importantes en las que el hardware inyecta el dato en otras etapas:

**1. Inyección en la etapa ID (Para los saltos condicionales)**
Como vimos anteriormente, en el camino de datos optimizado del RISC-V, el sumador y el comparador para evaluar las instrucciones de salto (como `beq` o `bge`) se adelantan a la etapa de decodificación (**ID**) para reducir la penalización a 1 solo ciclo.
Si un salto depende de un dato que se acaba de calcular, el hardware necesita enviar el desvío **directamente a la etapa ID** (al comparador), no a EX.

**2. Inyección en la etapa MEM (Para guardar datos con `sw` o `sb`)**
Las instrucciones de almacenamiento en memoria (`sw`) necesitan dos cosas:

- Un registro base para calcular la dirección (esto se suma en la etapa **EX**).
- El dato que se va a guardar en la memoria (esto solo se usa físicamente cuando la instrucción llega a la etapa **MEM**).

Si una instrucción calcula o carga un dato (por ejemplo un `lw` seguido de un `sw` que guarda ese mismo dato), el dato se puede inyectar mediante un desvío especial
**directamente a la entrada de la memoria de datos en la etapa MEM**, saltándose por completo la etapa EX.

**En resumen:**
La red de anticipación (desvíos) crea "atajos" inteligentes para entregar el dato justo a tiempo en el lugar exacto donde se usa. Por tanto, podemos inyectar datos en:

- **EX** (a la entrada de la ALU para operaciones aritméticas o cálculo de direcciones).
- **ID** (al comparador para evaluar saltos optimizados).
- **MEM** (al puerto de escritura de la memoria de datos para instrucciones _store_).

---

**primera iteración**

| CICLO                | C1  | C2  | C3           | C4          | C5     | C6     | C7  | C8           | C9          | C10 | C11     | C12 | C13 |
| :------------------- | :-- | :-- | :----------- | :---------- | :----- | :----- | :-- | :----------- | :---------- | :-- | :------ | :-- | :-- |
| `la a1, cadena`      | IF  | ID  | EX `out(a1)` | MEM         | WB     |        |     |              |             |     |         |     |     |
| `cont: lb a2, 0(a1)` |     | IF  | ID           | EX `in(a1)` | MEM    | WB     |     |              |             |     |         |     |     |
| `beqz a2, FIN`       |     |     | IF           | ID          | **ID** | **ID** | EX  | MEM          | WB          |     |         |     |     |
| `addi a2, a2, 32`    |     |     |              | IF          | IF     | **IF** | ID  | EX `out(a2)` | MEM         | WB  |         |     |     |
| `sb a2, 0(a1)`       |     |     |              |             |        |        | IF  | ID           | EX `in(a2)` | MEM | WB      |     |     |
| `addi a1, a1, 1`     |     |     |              |             |        |        |     | IF           | ID          | EX  | MEM     | WB  |     |
| `j cont`             |     |     |              |             |        |        |     |              | IF          | ID  | EX      | MEM | WB  |
| `li a7, 10`          |     |     |              |             |        |        |     |              |             | IF  | _flush_ |     |     |
| `cont: lb a2, 0(a1)` |     |     |              |             |        |        |     |              |             |     | IF      | ID  | EX  |

### Explicación:

**1. Dependencia de `la` a `lb` (¡0 bloqueos!):**
La instrucción `la` (que es una pseudoinstrucción) se comporta internamente como una operación aritmética que calcula una dirección. Por tanto, el registro `a1`
está listo a la salida de la etapa **EX** (Ciclo 3). Como `lb` necesita ese registro en su propia etapa **EX** (Ciclo 4) para sumarle el _offset_ de 0, el desvío
entra perfecto a tiempo. **`lb` no sufre ningún ciclo de bloqueo.**

**2. Dependencia de `lb` a `beqz` (El bloqueo de carga a salto cuesta 2 ciclos):**
Aquí es donde ocurre el atasco real. La instrucción `lb` no saca el carácter de la memoria hasta que finaliza su etapa **MEM** (al final del Ciclo 5). La instrucción de salto `beqz`,
por el hardware optimizado que manejamos, evalúa su condición en la etapa **ID**.

- En el Ciclo 4, `beqz` está en ID, pero el dato no existe. -> _Bloqueo._
- En el Ciclo 5, `beqz` sigue en ID. `lb` está leyendo la memoria, el dato aún no está en el registro de segmentación. -> _Bloqueo._
- En el Ciclo 6, `lb` pasa a WB y el dato ya está guardado en el registro _MEM/WB_. Es en este momento el dato ya está disponible, por lo tanto **no se produce el desvío directo**.
- ¡La instrucción sufre **2 ciclos de bloqueo**!

**3. El tapón estructural en cascada (`addi a2`):**
Como `beqz` se ha quedado atascado en ID durante los ciclos 4, 5 y 6, hace de "tapón" físico en las tuberías. Esto obliga a la instrucción que viene detrás (`addi a2, a2, 32`) a quedarse repitiendo
la etapa **IF** en esos mismos ciclos. **Es importante** poner los **IF** repetidos para demostrar dónde está la instrucción.

**4. No hay desvío para `addi a2, a2, 32`:**
`addi` no entra a su fase **ID** para leer registros hasta el **Ciclo 7**. En ese momento, la instrucción `lb` ya ha finalizado completamente (terminó en el Ciclo 6), por lo que el dato ya está escrito
de forma segura en el banco de registros. ¡`addi` lo lee con normalidad y no necesita usar la red de desvíos!.

**5. (`sb` y `j cont`):**

- Se produce el desvío entre `addi a2` y `sb a2`. El dato se calcula en el **EX** del ciclo 8 y viaja por la red de anticipación para entrar al **EX** del `sb` en el ciclo 9.
- El salto final `j cont` se evalúa en **ID** en el ciclo 10 y hace un descarte (_flush_) de la instrucción `li` en el ciclo 11, enlazando con la segunda iteración de forma perfecta.

**última iteración**

| CICLO                  | C1  | C2  | C3     | C4     | C5   | C6      | C7  | C8  | C9  | C10 | C11 |
| ---------------------- | --- | --- | ------ | ------ | ---- | ------- | --- | --- | --- | --- | --- |
| `cont:   lb a2, 0(a1)` | IF  | ID  | EX     | MEM    | _WB_ |         |     |     |     |     |     |
| `beqz a2, FIN`         |     | IF  | **ID** | **ID** | _ID_ | EX      | MEM | WB  |     |     |     |
| `addi a2, a2, 32`      |     |     | IF     | IF     | _IF_ | _flush_ |     |     |     |     |     |
| `li a7 , 10`           |     |     |        |        |      | IF      | ID  | EX  | MEM | WB  |     |
| `ecall`                |     |     |        |        |      |         | IF  | ID  | EX  | MEM | WB  |

### Explicación

Tal y como indica la teoría de la asignatura sobre los riesgos de control: "El simulador sigue la estrategia de apostar por salto no tomado, si el salto
se toma, es necesario ejecutar de nuevo la etapa IF con el destino de salto ya calculado".
Como el procesador había introducido de forma especulativa la instrucción `addi a2, a2, 32` en el cauce suponiendo que no saltaría, al resolverse el salto
en el Ciclo 5 se ve obligado a descartarla (flush) en el Ciclo 6 para limpiar el error, introduciendo en su lugar la instrucción correcta (`li a7, 10`).

**- b ¿En cuántos ciclos se ejecuta este bucle?**

**1. Primera iteración**
Miramos los ciclos que ocurren entre las fases IF de la instrucción `lb:

- Primer IF: ciclo 2
- Segundo IF: ciclo 11
- Total = 11 - 2 = 9 ciclos.
  **2. Iteraciones intermedias**
  Tenemos 17 iteraciones intermedias.
- Como son 6 instrucciones, si no hubiese bloqueo serían 6 ciclos ideales.
- Tenemos 2 ciclos de bloqueo de datos.
- 1 ciclo de bloqueo de control.
- Total = 17 \* 9 = 153
  **3. Última iteración**
  11 ciclos
  **4. Instrucciones previas al bucle**
  1 ciclo
  **5. Total**
  9 + 153 + 11 + 1 = 174 ciclos

## - c. Aplique la planificación de instrucciones para minimizar el número de bloqueos y repita el apartado (a) en un RISCV sin desvíos activos.

**Código original sin planificación**

```assembly
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
```

**Planificación**

- Adelantamos `addi a1, a1, 1` para evitar el bloqueo en el registro a2 entre `lb` y `beqz`.

```assembly
.data
    cadena: .asciiz "CADENAENMAYUSCULAS"
.text
        la a1, cadena
cont:   lb a2, 0(a1)
        addi a1, a1, 1
        beqz a2, FIN
        addi a2, a2, 32
        sb a2 , 0(a1)

        j cont
FIN:

    li a7 , 10 # Syscall exit
    ecall
```

**Repetimos apartado `a` sin desvíos**

**primera iteración**

| CICLO                  | C1  | C2  | C3     | C4     | C5   | C6  | C7     | C8   | C9     | C10    | C11  | C12 | C13 | C14 | C15     |
| ---------------------- | --- | --- | ------ | ------ | ---- | --- | ------ | ---- | ------ | ------ | ---- | --- | --- | --- | ------- |
| `la a1, cadena`        | IF  | ID  | EX     | MEM    | _WB_ |     |        |      |        |        |      |     |     |     |         |
| `cont: lb a2, 0(a1)`   |     | IF  | **ID** | **ID** | _ID_ | EX  | MEM    | _WB_ |        |        |      |     |     |     |         |
| `addi a1, a1, 1`       |     |     | IF     | IF     | _IF_ | ID  | EX     | MEM  | _WB_   |        |      |     |     |     |         |
| `beqz a2, FIN`         |     |     |        |        |      | IF  | **ID** | _ID_ | EX     | MEM    | WB   |     |     |     |         |
| `addi a2, a2, 32`      |     |     |        |        |      |     | IF     | IF   | ID     | EX     | MEM  | WB  |     |     |         |
| `sb a2 , -1(a1)`       |     |     |        |        |      |     |        | IF   | **ID** | **ID** | _ID_ | EX  | MEM | WB  |         |
| `j cont`               |     |     |        |        |      |     |        |      | IF     | IF     | IF   | ID  | EX  | MEM | WB      |
| `li a7 , 10`           |     |     |        |        |      |     |        |      |        |        |      |     |     | IF  | _flush_ |
| `cont:   lb a2, 0(a1)` |     |     |        |        |      |     |        |      |        |        |      |     |     | IF  | ID      |

**última iteración**

| CICLO                | C1  | C2  | C3  | C4     | C5   | C6      | C7  | C8  | C9  | C10 | C11 |
| -------------------- | --- | --- | --- | ------ | ---- | ------- | --- | --- | --- | --- | --- |
| `cont: lb a2, 0(a1)` | IF  | ID  | EX  | MEM    | _WB_ |         |     |     |     |     |     |
| `addi a1, a1, 1`     |     | IF  | ID  | EX     | MEM  | WB      |     |     |     |     |     |
| `beqz a2, FIN`       |     |     | IF  | **ID** | _ID_ | EX      | MEM | WB  |     |     |     |
| `addi a2, a2, 32`    |     |     |     | IF     | IF   | _flush_ |     |     |     |     |     |
| `li a7 , 10`         |     |     |     |        |      | IF      | ID  | EX  | MEM | WB  |     |
| `ecall`              |     |     |     |        |      |         | IF  | ID  | EX  | MEM | WB  |
|                      |     |     |     |        |      |         |     |     |     |     |     |
|                      |     |     |     |        |      |         |     |     |     |     |     |
|                      |     |     |     |        |      |         |     |     |     |     |     |

## - d. Repita el apartado (c) suponiendo que el RISCV tiene todos los desvíos posibles.
