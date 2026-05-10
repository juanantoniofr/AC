# Ejemplo de examen tipo test

## CUESTIóN 4 (10 preguntas, 1.5 puntos)

Indique que opción es la correcta en el margen izquierdo de cada pregunta. Sólo se puede seleccionar una opción. Cada respuesta incorrecta resta un tercio de una correcta. ́

---

### 1. Una CPU tiene una cache con 32 líneas que divide las direcciones en los siguientes campos: DESPLAZAMIENTO de 8 bits, INDICE de 4 bits y ETIQUETA de 20 bits. Indique que afirmación es la correcta:

- A. La cache es asociativa por conjuntos de 8 vías.
- B. La cache es asociativa por conjuntos de 4 vías.
- **C. La cache es asociativa por conjuntos de 2 vías.**
- D. La cache es de mapeado directo.

**Explicación**

La opción correcta para esta pregunta de examen es la **C. La cache es asociativa por conjuntos de 2 vías**.

Vamos a desglosar los errores conceptuales y a realizar el cálculo correcto:

- 1 El cálculo correcto (Por qué es la C)
  Para resolver este tipo de problemas, hay que recordar la relación entre el tamaño del índice, el número de conjuntos y el total de líneas:

- **El índice determina los conjuntos:** El campo ÍNDICE de la dirección se utiliza para seleccionar el conjunto en el que se ubicará el bloque. Si el índice tiene **4 bits**, significa que la caché está dividida en $2^4 =$ **16 conjuntos**.
- **Cálculo de las vías:** El grado de asociatividad (las vías) es simplemente el número de líneas que hay dentro de cada conjunto. Si el enunciado dice que la caché tiene un total de **32 líneas**, dividimos:
  $$
  32 \text{ líneas en total} / 16 \text{ conjuntos} = 2 \text{ líneas por conjunto (2 vías)}
  $$

**Por lo tanto, la afirmación correcta es que la caché es asociativa por conjuntos de 2 vías.**

_Notas_:

- **Sobre la opción D (Mapeado directo):** Las cachés de mapeado directo (o correspondencia directa) **sí tienen índice**, y lo utilizan para identificar directamente la única línea en la que puede ubicarse un bloque.
- El único tipo de caché en el que **el índice no existe** (y la dirección se compone únicamente de Etiqueta y Desplazamiento) es en la **caché completamente asociativa**.

- _Comprobación extra:_ Si esta caché de 32 líneas fuera realmente de mapeado directo, tendría 32 conjuntos (1 vía por conjunto). Para direccionar 32 conjuntos necesitarías obligatoriamente un índice de 5 bits ($2^5 = 32$), lo cual choca con los 4 bits del enunciado.

- Las direcciones de memoria se dividen (de izquierda a derecha) en:
  - **Etiqueta**: Esto identifica el bloque (que se almacena en una vía) dentro del conjunto.
  - **Índice**: Esto direcciona el conjunto.
  - **Desplazamiento**: _bits menos significativos_. Esto direcciona el byte o palabra dentro del bloque.

- Relación entre los conceptos de bloque y vía:
  - Un bloque se almacena en una vía, pero:
    - El bloque es el contenido
    - La vía es el contenedor

### Esquema de direccionamiento en cache

![alt text](esquema_direccionamiento_cache.png)

---

### 2. Se tiene una cache de mapeado directo con la siguiente division de direcciones: DESPLAZAMIENTO de 8 bits, ́́INDICE de 4 bits y ETIQUETA de 20 bits. Indique el numero y el tipo de fallos que se producen para la siguiente secuencia de referencias a direcciones de memoria: , 0xA104, 0xB102, 0xBC03, 0xA1FF. Suponga que la cache está inicialmente vacía.

- A. 4 fallos forzosos y 0 fallos por conflicto.
- B. 3 fallos forzosos y 0 fallos por conflicto.
- C. 3 fallos forzosos y 1 fallos por conflicto.
- D. 2 fallos forzosos y 1 fallo por conflicto.

- desplazamiento (8 bits) => el tamaño del bloque es 2<sup>8</sup> = 256 Bytes
- indice (4 bits) => el número de conjuntos es de 2<sup>4</sup> = 16
-

| etiqueta (20 bits) | indice (4 bists) | desplazamiento (8 bits) |

- 0xA101; desplazamiento (8 bits) -> 0x01 -> binario -> 0000 0001 -> selecciona la palabra dentro de bloque (vía)
  indice (4bits) -> 0x1 -> binario -> 0001 -> selecciona el conjunto
  etiqueta (20 bits) -> 0x0000A -> binario -> 0000 0000 0000 0000 1000 -> se compara en paralelo con las etiquetas de todas las vías

1 fallo forzoso

- 0xA104; desplazamiento (8 bits) -> 0x04 -> binario -> 0000 0100 -> selecciona la palabra dentro de bloque (vía)
  indice (4bits) -> 0x1 -> binario -> 0001 -> selecciona el conjunto
  etiqueta (20 bits) -> 0x0000A -> binario -> 0000 0000 0000 0000 1000 -> se compara en paralelo con las etiquetas de todas las vías

### 3. Un sistema de memoria virtual tiene las siguientes características: direcciones virtuales de V bits, direcciones físicas de F bits, tamaño de página de 2pt bytes y una TLB de mapeado directo con 2L líneas. Indique cuantos elementos tiene la tabla de paginas.

- A. 2
  F−P−L
  B. 2
  F−P
  C. 2
  V−P−L
  D. 2
  V−P
