# Ejercicio_2_1.md

## Ejercicio 1.

Suponiendo un sistema con las siguientes características:

- Caché totalmente asociativa de 8 líneas, con bloques de 4 palabras de 32 bits. Se trata de la misma caché que en el Ejercicio 1.1.
- La matriz A se encuentra en la dirección 0x10010000 de memoria.
- La matriz B se encuentra en la dirección 0x10010100 de memoria.

Las direcciones de memoria de ambas matrices no son realmente necesarias para realizar este ejercicio, pero se proporcionan por si el alumno las necesitara.

### Traza de las 8 primeras iteraciones del bucle interno

El bucle interno recorre la matriz A y B para realizar esta asignación

- B[j][0] = A[0][j];

Cómo j va de 0 a 7, tenemos:

| Instrucción          | Bloque B | Bloque A |
| -------------------- | -------- | -------- |
| 1. B[0][0] = A[0][0] | B[0]     | A[0]     |
| 2. B[1][0] = A[0][1] | B[1]     | A[0]     |
| 3. B[2][0] = A[0][2] | B[2]     | A[0]     |
| 4. B[3][0] = A[0][3] | B[3]     | A[0]     |
| 5. B[4][0] = A[0][4] | B[4]     | A[1]     |
| 6. B[5][0] = A[0][5] | B[5]     | A[1]     |
| 7. B[6][0] = A[0][6] | B[6]     | A[1]     |
| 8. B[7][0] = A[0][7] | B[7]     | A[1]     |

| Instrucción | Líneas de caché | Bloque |
| ----------- | --------------- | ------ |
| 1           | 0               | A[0] X |
| 1           | 1               | B[0] X |
| 2           | 3               | B[1] X |
| 3           | 4               | B[2]   |
| 4           | 5               | B[3]   |
| 5           | 6               | A[1]   |
| 5           | 7               | B[4]   |
| 6           | 0               | B[5]   |
| 7           | 1               | B[6]   |
| 8           | 2               | B[7]   |
