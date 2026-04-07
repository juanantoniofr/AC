# ejercicio_1_1.md

## Apartado a

Al tratarse de una caché **totalmente asociativa** de 8 líneas y bloques de 4 palabras (16 bytes - 32 bits), la descomposición de la dirección de 32 bits es la siguiente:

- **Desplazamiento:** 4 bits (para indexar los 16 bytes del bloque - 4 palabras). En hexadecimal, esto corresponde exactamente al **último dígito**.
- **Índice:** 0 bits (al ser totalmente asociativa, no hay conjuntos específicos).
- **Etiqueta:** 28 bits (el resto de la dirección). En hexadecimal, corresponde a los **primeros 7 dígitos**.

Patrón de acceso a memoria: al tener los bucles intercambiados y acceder por columnas (`A[i][j]`), estamos saltando de fila en fila. Como cada fila tiene 32 enteros de 4 bytes, el salto en memoria entre cada acceso es de 128 bytes (**`0x80`** en hexadecimal).

## Apartado b

Tabla para los primeros 9 accesos (`j=0`, e `i` desde `0` hasta `8`) bajo esta arquitectura:

| Dirección (hex) | Etiqueta (hex) | Desplazamiento (hex) | Fallo/Acierto   |
| :-------------- | :------------- | :------------------- | :-------------- |
| `0x10010000`    | `0x1001000`    | `0x0`                | Fallo (Forzoso) |
| `0x10010080`    | `0x1001008`    | `0x0`                | Fallo (Forzoso) |
| `0x10010100`    | `0x1001010`    | `0x0`                | Fallo (Forzoso) |
| `0x10010180`    | `0x1001018`    | `0x0`                | Fallo (Forzoso) |
| `0x10010200`    | `0x1001020`    | `0x0`                | Fallo (Forzoso) |
| `0x10010280`    | `0x1001028`    | `0x0`                | Fallo (Forzoso) |
| `0x10010300`    | `0x1001030`    | `0x0`                | Fallo (Forzoso) |
| `0x10010380`    | `0x1001038`    | `0x0`                | Fallo (Forzoso) |
| `0x10010400`    | `0x1001040`    | `0x0`                | Fallo (Forzoso) |

### Análisis de este escenario:

1.  **Etiquetas diferentes:** A diferencia del caso de mapeado directo donde gran parte de los bits se iban al índice, aquí vemos claramente cómo la etiqueta va cambiando en cada iteración porque la CPU tiene que guardar los 28 bits superiores completos para identificar el bloque.
2.  **El noveno acceso (El fallo forzoso):** Los primeros 8 accesos traen bloques nuevos a la caché, llenando exactamente las 8 líneas que tiene disponibles. Cuando llega el acceso número 9 (dirección `0x10010400`), la caché ya está llena, pero ese bloque **nunca estuvo en cache** entonces el fallo es forzoso.
    _nota_ para que el fallo sea **por capacidad** el bloque debe de haber estado al menos una vez en cache.
3.  **Expulsión LRU:** Para poder meter este 9º bloque en la caché, el hardware aplicará la política LRU (Least Recently Used) y expulsará el bloque que lleva más tiempo sin usarse, que en este caso es el de la Etiqueta `0x1001000` (el primero que cargamos).
4.  Una fila de la matriz ocupa exactamente **8 bloques** en la memoria caché.

El cálculo se deduce directamente de las características de tu código y de la arquitectura de la caché:

    - 1. **Tamaño de la fila:** La matriz está definida con una dimensión `N = 32`, por lo que cada fila contiene 32 elementos.
    - 2. **Tamaño del elemento:** Cada elemento es de tipo `unsigned int`, que en la arquitectura RISC-V equivale a 1 palabra (4 bytes).
    - 3. **Capacidad de un bloque:** Las características de tu sistema especifican que el tamaño del bloque es de 4 palabras (4W). Esto significa que en cada bloque caben exactamente 4 números enteros.
    - 4. **Cálculo final:** Dividiendo los 32 elementos que conforman una fila entre los 4 elementos que caben en cada bloque, obtenemos la cantidad exacta: 32 / 4 = 8 bloques.

Por tanto, cada vez que el procesador recorre una fila completa de la matriz, necesita traer a la caché 8 bloques distintos desde la memoria principal.

### ¿Cabe la matriz completa en caché?

Cálculos detallados paso a paso:

- 1. Cálculo del tamaño de la memoria caché

* **Líneas totales:** 8 líneas.
* **Tamaño del bloque:** 4 palabras por línea.
* **Tamaño de la palabra:** 4 bytes o 32 bits.

**Cálculos:**

- **Capacidad en palabras:** 8 lineas \* 4 palabras por línea = 32 palabras.
- **Capacidad en bytes:** 32 palabras \* 4 bytes por palabra = 128 Bytes.

* 2. Cálculo del tamaño de la matriz

- **Dimensiones de la matriz:** 32 filas por 32 columnas.
- **Tipo de dato:** `unsigned int`, equivalente a 1 palabra o 4 bytes.

**Cálculos:**

- **Total de elementos (palabras):** 32 \* 32 = 1024 palabras.
- **Tamaño total en bytes:** 1024 palabras \* 4 bytes/palabra = 4096 Bytes (o exactamente **4 KB**).

* 3. Conclusión
     La capacidad total de la memoria caché destinada a guardar los datos puros es de **128 Bytes**, mientras que la matriz completa ocupa **4096 Bytes**. Por lo tanto, la matriz es muchísimo más grande y **no cabe en la caché**.

De hecho, los 128 Bytes de capacidad de la caché coinciden exactamente con el tamaño de **una sola fila de la matriz** (32 elementos por 4 bytes = 128 Bytes).

## Apartado c

**¿De qué tipo son los fallos que aparecen en la tabla?**
En los primeros 9 accesos de la tabla se producen fallos **forzosos** ya que en todos los casos es la primera vez que se referencia el bloque de memoria.

**¿Cabe la matriz en la caché?**
**No**, tal y como calculamos anteriormente, la matriz completa ocupa 4096 bytes, mientras que tu caché solo tiene capacidad para albergar 128 bytes simultáneamente.

**¿Qué tipo de fallos se producirán cuando comience el procesamiento de la segunda columna?**
Seguirá habiendo fallos forzosos ya que siempre será la primera vez que se referencia el bloque.

**¿Cuál será la frecuencia de fallo?**
La frecuencia de fallos será del **100%**. El pésimo patrón de acceso por columnas salta de fila en fila superando continuamente la capacidad de la caché, provocando que absolutamente cada lectura resulte en un fallo y deba ir a la memoria principal.

**¿Cuál es el número total de accesos?**
El código realiza un total de **1024 accesos** a la memoria caché (resultado del bucle anidado de 32 \* 32 iteraciones para leer o escribir en la matriz).

A continuación tienes la tabla resumen con el comportamiento global de tu código, desglosando matemáticamente los 1024 fallos (256 forzosos, porque la matriz tiene 256 bloques en total y todos deben traerse por primera vez, y 768 por capacidad para el resto de iteraciones):

| Tipo de fallo                        | Frec. Fallos | Número de accesos |
| :----------------------------------- | :----------- | :---------------- |
| Forzosos (256) y por Capacidad (768) | 100%         | 1024              |
