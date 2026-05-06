# Clarificación de conceptos

## Riesgos de datos en la segmentación de cauce

Los riesgos de datos ocurren cuando la segmentación de cauce altera el orden estricto de lectura y escritura de los operandos, pudiendo generar resultados incorrectos. A continuación, te explico los tres tipos de dependencias (RAW, WAR y WAW) junto con sus ejemplos y secuencias tabulares.

Es muy importante destacar de antemano un concepto clave de las fuentes: **en el camino de datos segmentado básico de 5 etapas de RISC-V, el único riesgo de datos real que se produce es el RAW**. Los riesgos WAR y WAW son teóricos en esta arquitectura básica y no producen fallos gracias al diseño del hardware, aunque sí pueden ser un problema en procesadores más complejos con ejecución fuera de orden.

### 1. Riesgo RAW (Lectura después de escritura o dependencia real)

Se produce cuando una instrucción necesita **leer un operando que está siendo modificado por una instrucción anterior**. El riesgo ocurre si, debido a la segmentación, la instrucción que lee intenta tomar el valor antes de que la primera instrucción lo haya actualizado, leyendo un dato obsoleto.

**Ejemplo en ensamblador:**

```assembly
sub t2, t1, t3   # Escribe el resultado en t2
and t12, t2, t5  # Necesita leer el valor de t2
```

**Secuenciación tabular:**
| Ciclo | 1 | 2 | 3 | 4 | 5 | 6 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `sub t2, t1, t3` | IF | ID | EX | MEM | **WB (Escribe t2)** | |
| `and t12, t2, t5`| | IF | **ID (Lee t2)** | EX | MEM | WB |

**Explicación:** Como se observa en la tabla, la instrucción `and` intenta extraer el valor de `t2` en su etapa de decodificación (ID) durante el ciclo 3. Sin embargo, la instrucción `sub` no guardará el nuevo valor en `t2` hasta su etapa de escritura (WB) en el ciclo 5. Si no existiera hardware adicional (como los desvíos/anticipación), se produciría un riesgo y la CPU tendría que insertar bloqueos.

---

### 2. Riesgo WAR (Escritura después de lectura o antidependencia)

Ocurre cuando una instrucción necesita **escribir en un operando que está siendo leído por una instrucción anterior**. El riesgo sucedería si la segunda instrucción se adelanta y sobrescribe el registro antes de que la primera instrucción haya tenido tiempo de leer el valor original.

**Ejemplo en ensamblador:**

```assembly
add t4, t2, t3   # Necesita leer el valor de t2
or  t2, t4, t3   # Escribe un nuevo valor en t2
```

**Secuenciación tabular:**
| Ciclo | 1 | 2 | 3 | 4 | 5 | 6 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `add t4, t2, t3` | IF | **ID (Lee t2)** | EX | MEM | WB | |
| `or t2, t4, t3` | | IF | ID | EX | MEM | **WB (Escribe t2)** |

**Explicación:** En la arquitectura RISC-V estudiada, **este riesgo NO se produce**. Como las lecturas de registros se realizan estrictamente en la etapa 2 (ID) y las escrituras se realizan obligatoriamente en la etapa 5 (WB), es físicamente imposible que la instrucción `or` modifique el registro `t2` en el ciclo 6 antes de que la instrucción `add` lo haya leído en el ciclo 2.

---

### 3. Riesgo WAW (Escritura después de escritura o dependencia de salida)

Se da cuando **dos instrucciones distintas escriben en el mismo operando**. El riesgo ocurriría si, por culpa del solapamiento, la segunda instrucción finalizara su escritura antes que la primera instrucción, dejando en el registro un valor final incorrecto (el antiguo en lugar del nuevo).

**Ejemplo en ensamblador:**

```assembly
add t2, t3, t4   # Escribe un valor en t2
subi t2, t1, 50  # Sobrescribe un nuevo valor en t2
```

**Secuenciación tabular:**
| Ciclo | 1 | 2 | 3 | 4 | 5 | 6 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `add t2, t3, t4` | IF | ID | EX | MEM | **WB (1ª Escritura)** | |
| `subi t2, t1, 50`| | IF | ID | EX | MEM | **WB (2ª Escritura)** |

**Explicación:** Al igual que ocurre con las antidependencias, **este riesgo NO genera conflictos en el cauce básico de RISC-V**. Como el hardware solo permite escribir en los registros durante una única etapa al final del recorrido (la etapa WB), las escrituras siempre se completan en el mismo orden secuencial estricto en el que entraron las instrucciones. La instrucción `subi` siempre escribirá su valor definitivo un ciclo después de que `add` haya escrito el suyo.

## Interpretación de la instrucción `beq` con un desplazamiento inmediato

La instrucción

```asm
beq t1, t3, 16
```

se interpreta así en **RISC‑V**:

---

### Significado

> **“Si el contenido de `t1` es igual al de `t3`, salta a la dirección `PC + 16`.”**

- `beq` = _Branch if Equal_ (salto condicional si son iguales).
- `t1` y `t3` son registros temporales (alias de `x6` y `x28`).
- `16` es un **desplazamiento inmediato relativo al PC**, expresado en **bytes**.

---

### Detalle importante: el `16`

- El salto **no va a la dirección absoluta 16**.
- Va a:
  $$
  PC_{\text{actual}} + 16
  $$
- En RISC‑V, las instrucciones miden **4 bytes**, así que:
  - `16 bytes = 4 instrucciones más adelante`.

Si el PC actual apunta a la instrucción `beq`, el destino será la **quinta instrucción contando desde esa**.

---

### Ejemplo ilustrativo

```asm
0x1000: addi t1, x0, 3
0x1004: addi t3, x0, 3
0x1008: beq  t1, t3, 16   # si t1 == t3 → PC = 0x1008 + 16 = 0x1018
0x100C: addi x5, x0, 0   # se salta
0x1010: addi x5, x0, 1   # se salta
0x1014: addi x5, x0, 2   # se salta
0x1018: addi x5, x0, 3   # se ejecuta
```

Como `t1 == t3`, el salto **sí se toma** y se ejecuta la instrucción en `0x1018`.

---

### Forma habitual en ensamblador

En la práctica, normalmente no se escribe el número directamente, sino una **etiqueta**, y el ensamblador calcula el desplazamiento:

```asm
beq t1, t3, destino
```

Esto es más legible y evita errores.

---

## Resumen rápido

- ✅ Es un **salto condicional**
- ✅ El `16` es un **offset en bytes relativo al PC**
- ✅ Equivale a saltar **4 instrucciones hacia delante**
- ❌ No es una dirección absoluta
