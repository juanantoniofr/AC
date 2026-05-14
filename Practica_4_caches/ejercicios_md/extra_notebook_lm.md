Aquí tienes un ejercicio de desarrollo con nivel de examen oficial, diseñado específicamente basándome en el **Ejercicio 2.1 y 2.2 de la Práctica 4**.

Tómate tu tiempo para coger papel y bolígrafo, resolverlo paso a paso, y cuando me escribas tu respuesta, **te lo corregiré aplicando los criterios de evaluación de la cátedra**.

---

### PROBLEMA DE EXAMEN: Optimización de Caché (Procesamiento por bloques)

Un procesador RISC-V con direcciones físicas de 32 bits ejecuta un programa que realiza la trasposición de una matriz (copia las filas de la matriz `A` en las columnas de la matriz `B`). Ambas matrices son de tamaño 8x8 y sus elementos son enteros de 32 bits (4 bytes).

El computador posee una **memoria caché de datos totalmente asociativa de 8 líneas**, con un tamaño de **bloque de 16 bytes** (4 palabras). La política de reemplazo es LRU. La caché se encuentra inicialmente vacía.

Se sabe que en memoria principal:

- La matriz `A` comienza en la dirección `0x10010000`.
- La matriz `B` comienza en la dirección `0x10010100`.
- _Nota: Dado el tamaño del bloque (4 enteros), cada fila de las matrices ocupa exactamente 2 bloques de memoria. Por ejemplo, la primera fila de A ocupa los bloques A0 y A1; la segunda fila ocupa A2 y A3, etc._

El código original (sin optimizar) escrito por un programador novato es el siguiente:

```c
// Código original (Sin optimizar)
register int i, j;
for (i = 0; i < 8; ++i) {
    for (j = 0; j < 8; ++j) {
        B[j][i] = A[i][j];
    }
}
```

**SE PIDE:**

**Apartado A (Esquema de direcciones):**
Indique en cuántos campos descompone la memoria caché las direcciones físicas emitidas por el procesador. Especifique el nombre de cada campo y su tamaño en bits.

**Apartado B (Análisis de la traza sin optimizar):**
Rellene la traza de los primeros 8 accesos a memoria (es decir, correspondientes a las iteraciones `j=0, j=1, j=2, j=3` manteniendo `i=0`). Especifique el bloque de memoria accedido de cada matriz (A0, B0, B2, etc.) y si se produce Acierto o Fallo en caché.
_(Recuerde que una lectura de `A` y escritura en `B` son dos accesos independientes)._

**Apartado C (El problema de capacidad):**
Sin necesidad de seguir haciendo la traza completa, razone teóricamente qué le ocurrirá a la memoria caché cuando este bucle intente procesar la **segunda fila de A** (`i=1`). ¿Se producirán fallos de capacidad? Justifique su respuesta basándose en el tamaño de la caché (8 líneas) y el patrón de acceso a la matriz `B`.

| Linea de Caché | Estado Cache 1 iteración | Estado 2 iteración                   |
| :------------- | :----------------------- | :----------------------------------- |
| 0              | A0 _a7_                  | A0 _a7_ -> BO _a18_ -> **B12** _a30_ |
| 1              | B0 _a2_ -> B12 _a14_     | B12 _a14_ -> **A3** _a31_            |
| 2              | B2 _a4_ -> B14 _a16_     | B14 _a16_ -> **B10** _a28_           |
| 3              | B4 _a6_                  | B4 _a6_ -> **A2** _a23_              |
| 4              | B6 _a8_                  | B6 _a8_ -> B2 _a20_ -> **B14** _a32_ |
| 5              | A1 _a15_                 | A1 _a15_ -> **B8** _a26_             |
| 6              | B8 _a10_                 | B8 _a10_ -> **B4** _a22_             |
| 7              | B10 _a12_                | B10 _a12_ -> **B6** _a24_            |

Se producen 8 fallos por capacidad, ya que los bloques 'B' se expulsan mutuamente de la cache.

**Apartado D (Optimización - Procesamiento por bloques):**
Para solucionar el desastre del apartado anterior, ejerza el papel de un programador experto y reescriba en lenguaje C el código anterior aplicando la **Técnica de Procesamiento por Bloques (Blocking)**.
Escriba el código utilizando un tamaño de bloque de **4x4 elementos** (es decir, variables `BSIZE = 4`) de forma que los sub-bloques de A y B quepan simultáneamente en nuestra pequeña caché de 8 líneas.

```c
// Código optimizado
register int i, j, bi, bj;

// Bucles externos: Se mueven de bloque en bloque (de 4 en 4)
for (bi = 0; bi < 8; bi += 4) {
    for (bj = 0; bj < 8; bj += 4) {

        // Bucles internos: Procesan los 4x4 elementos del bloque actual
        for (i = bi; i < bi + 4; ++i) {
            for (j = bj; j < bj + 4; ++j) {
                B[j][i] = A[i][j];
            }
        }

    }
}
```

Los dos bucles exteriores dividen las matriz 8X8 en cuatro matrices de 4X4.
