# Tipos de dependencias

## 1. Dependencia RAW (Read After Write - Lectura después de escritura)

También conocida como **dependencia real**. Se produce cuando una instrucción necesita **leer** un operando que está siendo **escrito** (calculado) por una instrucción anterior.

**Ejemplo en código ensamblador:**

```assembly
add  t1, t2, t3   # Escribe el resultado en t1
lw   t4, 100(t1)  # Lee t1 para usarlo como dirección base
```

- **¿Qué ocurre en el cauce?** La instrucción `lw` necesita leer el valor de `t1` en su etapa `ID`, pero la instrucción `add` no lo escribirá de forma definitiva hasta que llegue a su última etapa `WB`.
- **Riesgo:** Genera un riesgo real de datos. Si no se frena el cauce (con bloqueos) o se adelanta el dato (con desvíos), la segunda instrucción leerá un valor de `t1` obsoleto y erróneo.

## 2. Dependencia WAR (Write After Read - Escritura después de lectura)

También conocida como **antidependencia**. Se da cuando una instrucción **escribe** en un registro que está siendo **leído** por una instrucción anterior.

**Ejemplo en código ensamblador:**

```assembly
add  t4, t2, t3   # Lee el registro t2 para realizar la suma
subi t2, t1, 50   # Escribe un nuevo valor en el registro t2
```

- **¿Qué ocurre en el cauce?** La primera instrucción `add` lee el registro `t2` en su etapa `ID`. La segunda instrucción `subi` actualiza el valor de `t2`, pero no lo hace hasta que alcanza su etapa final `WB`.
- **Riesgo:** **En el cauce básico del RISC-V no hay riesgo**. Como las lecturas siempre se realizan pronto (etapa ID) y las escrituras se realizan al final (etapa WB), es físicamente imposible que la escritura se adelante y estropee el dato que la primera instrucción necesitaba leer.

## 3. Dependencia WAW (Write After Write - Escritura después de escritura)

También conocida como **dependencia de salida**. Se produce cuando dos instrucciones seguidas **escriben** en el mismo registro de destino.

**Ejemplo en código ensamblador:**

```assembly
or   t2, t4, t3   # Escribe su resultado en t2
subi t2, t1, 50   # También escribe su resultado en t2
```

- **¿Qué ocurre en el cauce?** Ambas instrucciones tienen como destino final actualizar el registro `t2`.
- **Riesgo:** **En el cauce básico del RISC-V tampoco hay riesgo**. Como existe una única etapa de escritura en los registros (`WB`) y las instrucciones fluyen en estricto orden secuencial, el resultado final del registro `t2` siempre será el de la última instrucción (`subi`). Las escrituras no pueden desordenarse.

## Resumen para el examen:

En la arquitectura segmentada RISC-V que se estudia en tu asignatura (con sus 5 etapas IF, ID, EX, MEM, WB), **únicamente las dependencias RAW son capaces de generar conflictos y bloqueos en el procesador**. Las dependencias WAR y WAW son inofensivas porque la estructura del cauce garantiza que las escrituras siempre se produzcan de forma ordenada y al final del ciclo de vida de la instrucción.
