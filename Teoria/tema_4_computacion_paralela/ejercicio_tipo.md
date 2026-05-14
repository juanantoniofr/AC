### Ejercicio: Análisis de Trazas y Optimización en RISC-V

Considere un procesador RISC-V de 5 etapas (IF, ID, EX, MEM, WB) que implementa las siguientes características:

- Camino de datos **optimizado para saltos** (la condición y la dirección de salto se resuelven de forma adelantada en la etapa ID).
- **Predicción de salto no tomado**.
- **Toda la lógica de anticipación de resultados (desvíos/bypass)** activa.

Se ejecuta el siguiente fragmento de código, correspondiente a un bucle que procesa un vector:

```assembly
Loop: lw   t0, 0(s1)
      addu t0, t0, s2
      sw   t0, 0(s1)
      addi s1, s1, -4
      bne  s1, zero, Loop
```

**Cuestiones para ponerte a prueba:**

1.  **Riesgos de datos y bloqueos:** Deduce la traza de ejecución de una iteración. A pesar de tener los desvíos activados, hay bloqueos inevitables. Identifica **cuántos ciclos de bloqueo de datos** se producen en total en una iteración y **entre qué par de instrucciones** ocurren.
2.  **Riesgos de control:** Sabiendo que el salto `bne` final **se toma** (el bucle itera), ¿cuántos **ciclos de bloqueo de control** se producen al ejecutarse el salto y qué le ocurre a la instrucción que se haya introducido en el cauce tras él?.

Traza de ejecución (cada columna representa un ciclo de reloj, y cada fila una instrucción):

| Ciclos             | C1  | C2  | C3     | C4          | C5                | C6        | C7         | C8        | C9  | C10 | C11 |
| :----------------- | :-- | :-- | :----- | :---------- | :---------------- | :-------- | :--------- | :-------- | :-- | :-- | :-- |
| lw to, 0(s1)       | IF  | ID  | EX     | MEM out(to) | WB                |           |            |           |     |     |     |
| addu t0, t0, s2    |     | IF  | **ID** | ID          | in(to) EX out(t0) | MEM       | WB         |           |     |     |     |
| sw t0, 0(s1)       |     |     | _if_   | IF          | ID                | in(t0) EX | MEM        | WB        |     |     |     |
| addi s1, s1, -4    |     |     |        |             | IF                | ID        | EX out(s1) | MEM       | WB  |     |     |
| bne s1, zero, Loop |     |     |        |             |                   | IF        | **ID**     | in(s1) ID | EX  | MEM | WB  |
| `otra instrucción` |     |     |        |             |                   |           | IF         | _flush_   |     |     |     |

Bloqueo RAW lw t0, 0(s1) y addu t0, t0, s2 -> 1 ciclos de penalización
Bloqueo RAW addi s1, s1, -4 y bne s1, zero, loop-> 1 ciclos de penalización

En total 2 ciclos de penalización de datos, más 1 ciclo de penalización por bloqueo de control (suponiendo que se toma el salto)

3.  **Planificación estática (Optimización):** Ejerciendo el papel del compilador, ¿cómo **reordenarías y modificarías** las instrucciones de este bucle para **eliminar por completo todos los ciclos de bloqueo de datos** sin alterar la lógica del programa original?.

- Podemos adelantar la instrucción addi para eliminar un bloqueo

| Ciclos             | C1  | C2  | C3  | C4          | C5                | C6        | C7  | C8      | C9  | C10 | C11 |
| :----------------- | :-- | :-- | :-- | :---------- | :---------------- | :-------- | :-- | :------ | :-- | :-- | :-- |
| lw to, 0(s1)       | IF  | ID  | EX  | MEM out(t0) | WB                |           |     |         |     |     |     |
| addi s1, s1, -4    |     | IF  | ID  | EX          | MEM               | WB        |     |         |     |     |     |
| addu t0, t0, s2    |     |     | IF  | ID          | in(t0) EX out(t0) | MEM       | WB  |         |     |     |     |
| sw t0, 4(s1)       |     |     |     | IF          | ID                | in(t0) EX | MEM | WB      |     |     |     |
| bne s1, zero, Loop |     |     |     |             |                   | IF        | ID  | EX      | MEM | WB  |     |
| `otra instrucción` |     |     |     |             |                   |           | IF  | _flush_ |     |     |     |

Con esta reordenación, hemos eliminado completamente los bloqueos de datos, ya que cada instrucción tiene sus operandos listos en el momento de su ejecución. Sin embargo, el bloqueo de control sigue presente si el salto se toma, pero no podemos eliminarlo sin cambiar la lógica del programa.
