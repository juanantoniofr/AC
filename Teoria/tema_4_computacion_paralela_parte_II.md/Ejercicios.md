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

## 4.

Suponga que tiene una aplicación corriendo sobre un multiprocesador NUMA con 32 procesadores, con una frecuencia de reloj de 3.3 GHz, para el cual una referencia a una zona de memoria no local (que reside en un procesador remoto y por tanto incluye comunicación entre distintos procesadores) tarda 200 ns en completarse.

Para simplificar, suponga que para esta aplicación todas las referencias a una zona local de memoria provocan un acierto en la jerarquía local de memoria (aunque esta suposición es ligeramente optimista).

Si el CPI base para cada procesador (suponiendo que todas las referencias a memoria aciertan en caché) es de 0.5, calcular cuánto más rápido es el multiprocesador en caso de que no haya comunicación (todas las instrucciones provocan referencias a zonas de memoria local) frente al caso en que un 0.2% de las instrucciones provocan una referencia a una zona de memoria no local (en la que hay comunicación).

## Solución

Vamos a resolver el **Ejercicio 4** paso a paso.

### El enunciado nos da los siguientes datos:

- **Frecuencia del procesador ($f$):** $3,3$ GHz.
- **Latencia de comunicación remota (acceso a memoria NUMA):** $200$ ns.
- **CPI base (asumiendo 100% de aciertos locales):** $0,5$ ciclos/instrucción.
- **Tasa de accesos remotos (comunicación):** $0,2\%$ de las instrucciones (es decir, $0,002$ accesos/instrucción).

El objetivo es calcular cuánto más rápido es el caso ideal (sin comunicación) frente al caso real (con un 0,2% de comunicación).

### Paso 1: Calcular la penalización de comunicación en ciclos de reloj

La latencia de acceder a la memoria remota nos la dan en nanosegundos (200 ns), pero para poder sumarla al CPI, necesitamos convertir ese tiempo a **ciclos de reloj**.

1. Calculamos el tiempo de un ciclo de reloj ($T_c$):
   $T_c = \frac{1}{f} = \frac{1}{3,3 \text{ GHz}} = \frac{1}{3,3 \times 10^9 \text{ Hz}} \approx 0,303 \text{ ns/ciclo}$

2. Calculamos cuántos ciclos caben en esos 200 ns de latencia:
   $\text{Penalización en ciclos} = \frac{\text{Latencia remota}}{T_c} = 200 \text{ ns} \times 3,3 \text{ GHz} = \mathbf{660 \text{ ciclos}}$

Esto significa que cada vez que una instrucción necesita un dato de otro procesador, la CPU se queda bloqueada durante 660 ciclos esperando el dato.

### Paso 2: Calcular el CPI de ambos escenarios

Ahora usamos el concepto de CPI efectivo: $CPI_{efectivo} = CPI_{base} + (\text{Tasa de fallos} \times \text{Penalización en ciclos})$.

- **Escenario 1 (Ideal, SIN comunicación):**
  Como el 100% de las referencias son locales y aciertan, no hay penalizaciones.
  $CPI_{ideal} = \mathbf{0,5}$

- **Escenario 2 (Real, CON comunicación):**
  Aquí, el 0,2% de las instrucciones pagan la tremenda penalización de 660 ciclos.
  $CPI_{real} = 0,5 + (0,002 \times 660) = 0,5 + 1,32 = \mathbf{1,82}$

### Paso 3: Calcular la aceleración usando la Ecuación Fundamental del Rendimiento

La ecuación fundamental nos dice que el Tiempo de CPU es:
$T_{CPU} = N\_instrucciones \times CPI \times T_c$

Para saber cuánto más rápido es el Escenario 1 respecto al 2, calculamos el **factor de aceleración ($A$)** dividiendo el tiempo del escenario lento entre el tiempo del escenario rápido:

$A = \frac{T_{real}}{T_{ideal}} = \frac{N \times CPI_{real} \times T_c}{N \times CPI_{ideal} \times T_c}$

Como el programa es el mismo, el número de instrucciones ($N$) y el tiempo de ciclo ($T_c$) se anulan en la división, simplificando la fórmula a:

$A = \frac{CPI_{real}}{CPI_{ideal}} = \frac{1,82}{0,5} = \mathbf{3,64}$

**Conclusión:** El multiprocesador es **3,64 veces más rápido** en el caso ideal sin comunicación que en el caso con comunicación.

---

### Sustento Teórico (El problema de la arquitectura NUMA)

Este ejercicio ilustra brillantemente la gran desventaja teórica de los sistemas MIMD de memoria distribuida o NUMA (Non-Uniform Memory Access): **la altísima sobrecarga de la comunicación**.

Aunque tu aplicación esté paralelizada de forma casi perfecta, el simple hecho de que un minúsculo **0,2%** de las instrucciones necesite viajar por la red de interconexión para buscar un dato en la memoria de otro procesador, destruye el rendimiento. Fíjate que el CPI salta de 0,5 a 1,82; es decir, **la CPU pasa más del doble de su tiempo atascada esperando datos de la red** que realizando cálculos útiles.

Por eso en computación paralela NUMA y clústeres es fundamental optimizar la "localidad de los datos" para que cada procesador trabaje en la medida de lo posible con su memoria local.
