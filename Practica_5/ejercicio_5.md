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

- a. Dibuje en papel el diagrama de ejecución para un RISCV sin ningún tipo de desvío. Dibuje solo la primera iteración y la última.

**primera iteración**

| CICLO                  | C1  | C2  | C3     | C4     | C5   | C6     | C7     | C8   | C9  | C10    | C11    | C12  | C13 | C14 | C15     | C16 | C17 | C18 | C19 | C20 | C21 | C22 | C23 | C24 | C25 | C26 | C27 | C28 | C29 |
| ---------------------- | --- | --- | ------ | ------ | ---- | ------ | ------ | ---- | --- | ------ | ------ | ---- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `la a1, cadena`        | IF  | ID  | EX     | MEM    | _WB_ |        |        |      |     |        |        |      |     |     |         |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| `cont:   lb a2, 0(a1)` |     | IF  | **ID** | **ID** | _ID_ | EX     | MEM    | _WB_ |     |        |        |      |     |     |         |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| `beqz a2, FIN`         |     |     | IF     | IF     | _IF_ | **ID** | **ID** | _ID_ | EX  | MEM    | WB     |      |     |     |         |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| `addi a2, a2, 32`      |     |     |        |        |      | IF     | IF     | _IF_ | ID  | EX     | MEM    | _WB_ |     |     |         |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| `sb a2 , 0(a1)`        |     |     |        |        |      |        |        |      | IF  | **ID** | **ID** | _ID_ | EX  | MEM | WB      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| `addi a1, a1, 1`       |     |     |        |        |      |        |        |      |     | IF     | IF     | _IF_ | ID  | EX  | MEM     | WB  |     |     |     |     |     |     |     |     |     |     |     |     |     |
| `j cont`               |     |     |        |        |      |        |        |      |     |        |        |      | IF  | ID  | EX      | MEM | WB  |     |     |     |     |     |     |     |     |     |     |     |     |
| `li a7 , 10`           |     |     |        |        |      |        |        |      |     |        |        |      |     | IF  | _flush_ |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| `cont:   lb a2, 0(a1)` |     |     |        |        |      |        |        |      |     |        |        |      |     |     | IF      | ID  | EX  |     |     |     |     |     |     |     |     |     |     |     |     |

**última iteración**

| CICLO                  | C1  | C2  | C3     | C4     | C5   | C6      | C7  | C8  | C9  | C10 | C11 | C13 | C14 | C15 | C16 | C17 | C18 | C19 | C20 | C21 | C22 | C23 | C24 | C25 | C26 | C27 | C28 | C29 |
| ---------------------- | --- | --- | ------ | ------ | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `cont:   lb a2, 0(a1)` | IF  | ID  | EX     | MEM    | _WB_ |         |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| `beqz a2, FIN`         |     | IF  | **ID** | **ID** | _ID_ | EX      | MEM | WB  |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| `addi a2, a2, 32`      |     |     | IF     | IF     | IF   | _flush_ |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| `li a7 , 10`           |     |     |        |        |      | IF      | ID  | EX  | MEM | WB  |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| `ecall`                |     |     |        |        |      |         | IF  | ID  | EX  | MEM | WB  |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|                        |     |     |        |        |      |         |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|                        |     |     |        |        |      |         |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|                        |     |     |        |        |      |         |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |

_NOTA_: La arquitectura base sobre la que se trabaja ya incorpora esta mejora, estableciendo de forma general que "la condición y destino del salto se calculan **en la fase ID**"

**- b ¿En cuántos ciclos se ejecuta este bucle?**

Para calcular el tiempo total en un procesador segmentado, no debemos mirar cuándo termina la etapa `WB` de una iteración, sino el **ritmo o intervalo de inicio** (cuántos ciclos pasan desde que el `lb` de una iteración entra en `IF` hasta que entra el `lb` de la siguiente).

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

- b. Repita el apartado (a) suponiendo que el RISCV tiene todos los desvíos posibles.
- c. Aplique la planificación de instrucciones para minimizar el número de bloqueos y repita el apartado (a) en un RISCV sin desvíos activos.
- d. Repita el apartado (c) suponiendo que el RISCV tiene todos los desvíos posibles.
