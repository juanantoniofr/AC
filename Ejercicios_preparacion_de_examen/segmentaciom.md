# Problema examen de segmentación

## P2 (2.5 puntos)

Suponga que el código que se muestra a continuación se ejecuta en un RISC-V con segmentación de cauce, con el camino de datos optimizado para saltos, predicción de salto no tomado
y toda la lógica de anticipación de resultados (desvíos) necesaria para evitar bloqueos.
Suponga que a partir de la posición 100 se encuentran los siguientes bytes: 10, 30, 4, 1, 10, 29, 11, 32, 7, 15, …

a) Realice la traza de ejecución indicando los bloqueos que se producen y los desvíos que se activan. Para cada desvío indique el registro de segmentación o unidad funcional
(registro de segmentación IF/ID, ID/EX, EX/MEM o MEM/WB, comparador de la etapa ID, sumador de la etapa ID, ALU, puerto de datos de la memoria o puerto de direcciones de la memoria)
que constituyen el origen y el destino del desvío.

| Instrucción            | 1   | 2   | 3           | 4            | 5                    | 6           | 7   | 8   | 9   | 10         | 11         | 12  | 13  | 14  | 15  | 16  |
| :--------------------- | :-- | :-- | :---------- | :----------- | :------------------- | :---------- | :-- | :-- | :-- | :--------- | :--------- | :-- | :-- | :-- | --- | --- |
| (1) addi t1,zero,0     | IF  | ID  | EX _o1(t1)_ | MEM _o2(t1)_ | WB                   |             |     |     |     |            |            |     |     |     |     |     |
| (2) lw t2,100(t1)      |     | IF  | ID          | _i1(t1)_ EX  | MEM                  | WB          |     |     |     |            |            |     |     |     |     |     |
| (3) addi t1,t1,4       |     |     | IF          | ID           | _i2(t1)_ EX _o3(t1)_ | MEM         | WB  |     |     |            |            |     |     |     |     |     |
| (4) lw t3,100(t1)      |     |     |             | IF           | ID                   | _i3(t1)_ EX | MEM | WB  |     |            |            |     |     |     |     |     |
| (5) beq t2,t3,e1       |     |     |             |              | IF                   | -           | -   | ID  | EX  | MEM        | WB         |     |     |     |     |     |
| (6) addi t1,t1,-4      |     |     |             |              |                      |             |     | IF  | ID  | EX _o(t1)_ | MEM        | WB  |     |     |     |     |
| (7) e1: beq t1,zero,e2 |     |     |             |              |                      |             |     |     | IF  | -          | _i(t1)_ ID | EX  | MEM | WB  |     |     |
| (8) addi t1,zero,zero  |     |     |             |              |                      |             |     |     |     | -          | IF         | -   | -   | -   | -   |     |
| (9) e2: addi t1,t1,1   |     |     |             |              |                      |             |     |     |     |            |            | IF  | ID  | EX  | MEM | WB  |

EX/MEM -> ALU
MEM/WB -> ALU
EX/MEM -> ALU
EX/MEM -> comparador de la etapa ID

b) Indique los pares de instrucciones que presentan **dependencias tipo WAR** en el código fuente, así como el registro involucrado. Limítese exclusivamente a las dependencias entre una
instrucción de la línea i y las instrucciones de las líneas i+1 e i+2, tal y como ocurre con los riesgos de tipo RAW. Para referirse a las instrucciones utilice el número de línea.

(2) lw t2,100(t1) (lee t1)
(3) addi t1,t1,4 (escribe en t1)

(4) lw t3,100(t1) (lee t1)
(6) addi t1,t1,-4 (escribe en t1)

(7) e1: beq t1,zero,e2 (lee t1)
(8) addi t1,zero,zero (escribe en t1)

(7) e1: beq t1,zero,e2 (lee t1)
(9) e2: addi t1,t1,1 (escribe en t1)

c) Indique los pares de instrucciones que presentan **dependencias tipo WAW** en el código fuente, así como el registro involucrado. Limítese exclusivamente a las dependencias entre una instrucción
de la línea i y las instrucciones de las líneas i+1 e i+2, tal y como ocurre con los riesgos de tipo RAW. Para referirse a las instrucciones utilice el número de línea.

1-3 (t1), 8-9(t1), 6-8(t1)

## P3 (2.5 puntos)

Manteniendo el mismo número de instrucciones, consigo un procesador con una frecuencia de 1 GHz más, y con una reducción del 20% de CPI. ¿Cuál es la aceleración mínima que se consigue?

### Solución

Para calcular la aceleración mínima que vas a conseguir, debemos apoyarnos en la **ecuación clásica del rendimiento de un procesador**. El tiempo de ejecución de la CPU se define mediante la
siguiente fórmula:

$t_{CPU} = \frac{N\_instrucciones \times CPI}{f_{reloj}}$

Vamos a definir matemáticamente los dos escenarios planteados:

- **Escenario original:** $t_1 = \frac{N \times CPI_1}{f_1}$
- **Escenario mejorado:** Mantenemos el mismo número de instrucciones ($N$), reducimos el CPI un 20% ($CPI_2 = 0,8 \times CPI_1$) y aumentamos la frecuencia en 1 GHz ($f_2 = f_1 + 1$).

Por tanto, $t_2 = \frac{N \times 0,8 \times CPI_1}{f_1 + 1}$

Para averiguar cuánto más rápido es el nuevo procesador, utilizamos el **factor de aceleración ($A$)**, que consiste en dividir el tiempo del escenario original entre el tiempo del escenario mejorado:

$A = \frac{t_1}{t_2} = \frac{\frac{N \times CPI_1}{f_1}}{\frac{N \times 0,8 \times CPI_1}{f_1 + 1}}$

Al resolver la fracción, la variable del número de instrucciones ($N$) y el $CPI_1$ se anulan por estar presentes tanto en el numerador como en el denominador, simplificando la ecuación enormemente:

$A = \frac{f_1 + 1}{0,8 \times f_1} = \frac{1}{0,8} \times \frac{f_1 + 1}{f_1} = \mathbf{1,25 \times \left(1 + \frac{1}{f_1}\right)}$

**El cálculo de la aceleración mínima:**
Al observar la ecuación resultante, vemos que la aceleración final sigue dependiendo de la frecuencia base ($f_1$) que tuviera tu procesador original. Como buscamos la **aceleración mínima**,
tenemos que pensar en el peor escenario posible matemático para nuestra mejora.

El factor $\left(1 + \frac{1}{f_1}\right)$ se hace cada vez más pequeño a medida que la frecuencia original ($f_1$) es más grande. Si calculamos el límite cuando $f_1$ tiende a infinito,
la porción $\frac{1}{f_1}$ tiende a 0, haciendo que el paréntesis completo valga 1.

Por lo tanto, la **aceleración mínima garantizada es exactamente 1,25x** (es decir, el procesador será como mínimo un 25% más rápido).

**El sustento teórico:**
Este resultado matemático tiene toda la lógica desde el punto de vista del hardware. Si partes de un procesador que ya tiene una frecuencia extremadamente alta (por ejemplo, 100 GHz),
añadir 1 GHz extra supone una mejora casi nula en ese apartado. Sin embargo, **la simple reducción del CPI en un 20% te garantiza por sí sola una mejora del 25% en el rendimiento**
($1 / 0,8 = 1,25$). Cualquier mejora adicional en la frecuencia, como ese gigahercio extra, se sumará a esa base para darte un factor de aceleración final que siempre será estrictamente
superior a 1,25.
