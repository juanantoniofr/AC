# Ejercicios

## 1.

El estudio de la ejecución de un programa secuencial revela que el 95 por ciento del tiempo de ejecución se invierte dentro de funciones que son paralelizables. ¿Cuál es la aceleración máxima que podríamos esperar al ejecutar una versión paralela de este programa en 10 procesadores?

## Solución

El sustento teórico detrás de la solución a este problema es la **Ley de Amdahl**. Esta ley de la arquitectura de computadores establece que **el rendimiento o la aceleración que se puede obtener al paralelizar un programa está estrictamente limitado por la fracción del tiempo de ejecución total que no se puede paralelizar** (es decir, la parte puramente secuencial).

La fórmula matemática de la Ley de Amdahl para el factor de aceleración es la siguiente:

$A_p = \frac{1}{(1-f) + \frac{f}{p}}$

Donde:

- **$A_p$**: Es el **factor de aceleración** (Speedup) que se consigue al utilizar un número determinado de procesadores.
- **$f$**: Es la **fracción del tiempo original que se ve afectada por la paralelización** (en tu caso, el porcentaje del código que es paralelizable).
- **$(1-f)$**: Representa la fracción de tiempo estrictamente secuencial que no puede beneficiarse de tener múltiples procesadores.
- **$p$**: Es el **número de procesadores**.

### Cálculos paso a paso

A partir de tu enunciado, extraemos las variables para aplicar la fórmula:

- Fracción paralelizable ($f$): 95% = **0.95**
- Fracción puramente secuencial ($1-f$): 1 - 0.95 = **0.05**
- Número de procesadores ($p$): **10**

Sustituimos estos valores exactos en la fórmula:

- 1.  $A_{10} = \frac{1}{0.05 + \frac{0.95}{10}}$
- 2.  Resolvemos la división de la parte paralelizada:
      $A_{10} = \frac{1}{0.05 + 0.095}$
- 3.  Sumamos el denominador (que representa el nuevo tiempo de ejecución relativo):
      $A_{10} = \frac{1}{0.145}$
- 4.  Calculamos el resultado final:
      **$A_{10} \approx 6.89$ (o $6.9x$)**

**Conclusión:**
La aceleración máxima que podemos esperar es de aproximadamente **6.9 veces** respecto a la ejecución en un solo procesador.

La principal lección teórica de este cálculo es comprender que, aunque dispongas de 10 procesadores y un 95% del código corra en paralelo de forma óptima, **nunca alcanzarás una aceleración lineal ideal de 10x**. Ese pequeño 5% del código que debe ejecutarse secuencialmente se convierte en un cuello de botella que limita severamente el rendimiento máximo alcanzable.

---

## 2.

Para un tamaño dado del problema, el 6 por ciento de las operaciones de un programa paralelo
están dentro de funciones de E/S que deben ejecutarse necesariamente en un solo procesador. ¿Cuál
es el número mínimo de procesadores necesarios para que el programa paralelo muestre una
aceleración de 10?

## Solución

- Sea N el número mínimo de procesadores
- Como el 6% es no paralelizable, suponemos que le 94% sí lo es.

Entonces:

$A_p = \frac{1}{(1-f) + \frac{f}{p}}$
$10 = \frac{1}{(1-f) + \frac{f}{p}}$
$10 = \frac{N}{(0,06 \dot N ) + 0,94}$
$0,6 \dot N + 9,4 = N$
$N = \frac{-9,4}{-0,4} = \frac{9,4}{0,4} = 23,5

**Al menos debe tener 24 procesadores**
