# Ejercicio_2_1.md

## Ejercicio 1.

Suponiendo un sistema con las siguientes características:

- Caché totalmente asociativa de 8 líneas, con bloques de 4 palabras de 32 bits. Se trata de la misma caché que en el Ejercicio 1.1.
- La matriz A se encuentra en la dirección 0x10010000 de memoria.
- La matriz B se encuentra en la dirección 0x10010100 de memoria.

Las direcciones de memoria de ambas matrices no son realmente necesarias para realizar este ejercicio, pero se proporcionan por si el alumno las necesitara.

### A. Traza de las 8 primeras iteraciones del bucle interno

El bucle interno recorre la matriz A y B para realizar esta asignación

- B[j][0] = A[0][j];

Cómo j va de 0 a 7, tenemos:

| Instrucción          | Bloque B | Bloque A |
| -------------------- | -------- | -------- |
| 1. B[0][0] = A[0][0] | B0       | A0     |
| 2. B[1][0] = A[0][1] | B2       | A0     |
| 3. B[2][0] = A[0][2] | B4       | A0     |
| 4. B[3][0] = A[0][3] | B6       | A0     |
| 5. B[4][0] = A[0][4] | B8       | A1     |
| 6. B[5][0] = A[0][5] | B10      | A1     |
| 7. B[6][0] = A[0][6] | B12      | A1     |
| 8. B[7][0] = A[0][7] | B14      | A1     |

| Instrucción | Líneas de caché | Bloque |
| ----------- | --------------- | ------ |
| 1 - 7       | 0               | A0 - B12 |
| 1 - 8       | 1               | B0 - B14 |
| 2           | 3               | B2  |
| 3           | 4               | B4  |
| 4           | 5               | B6  |
| 5           | 6               | A1  |
| 5           | 7               | B8  |
| 6           | 0               | B10 |

- **Fallos**: 10 de tipo forzoso

### B. Traza de las 8 siguientes iteraciones

Instrucciones desde B[8][0] = A[0][8] hasta B[16][0] = A[0][16]

| Instrucción | Líneas de caché | Bloque |
| ----------- | --------------- | ------ |
| 1 - 7 - 13  | 0               | A0 - B12 - B8 |
| 1 - 8 - 14  | 1               | B0 - B14 - B10 |
| 2 - 9 - 15  | 3               | B2 - A2 - B12 |
| 3 - 9 - 16  | 4               | B4 - B0 - B14 |
| 4 - 10      | 5               | B6 - B2  |
| 5 - 11      | 6               | A1 - B4  |
| 5 - 12      | 7               | B8 - B6  |
| 6 - 13      | 0               | B10 - A3  |

32 lecturas:
- **Fallos**: 
    - Forzosos: 4 de bloques A + 8 de bloques B
    - Capacidad: 8 
    - Aciertos: 12 de bloques A 

### C. ¿Cuántos fallos se producirán al ejecutar el programa completo? ¿Cuál será la frecuencia de fallos?

N = 8 => vector A y B tiene 8 * 8 = 64 posiciones, como cada bloque (A o B) contiene 4 posiciones => 16 Bloques A y B.

- Los bloques B son desplazados de la cache en cada iteración, cada bloque genera un fallo forzoso (16) y 3 por capacidad (3 * 16 = 48)
- Los bloques A no son desplazados generan fallos forzosos 16 y 3 aciertos (3 * 16 = 48)

- 128 accesos a memoria, de los cuales 48 son aciertos => Hit rate = (48 * 100) / 128 = 37,5%