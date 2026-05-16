# Computadores paralelos

## introducción

Los ejercicios matemáticos de esta parte giran en torno a la Ley de Amdahl, y en los exámenes se suelen combinar con preguntas teóricas sobre las arquitecturas para evaluar si comprendes dónde se va a ejecutar ese código.

Poniéndome de nuevo el "gorro de profesor", aquí tienes un ejercicio de examen completo que abarca los tipos de problemas que nos quedaban por ver (despejar la fracción secuencial y calcular el límite asintótico) junto con un apartado teórico clave.

---

## PROBLEMA DE EXAMEN: Rendimiento y Arquitecturas Paralelas

Un equipo de ingenieros de software está desarrollando una aplicación crítica y necesita ejecutarla en una nueva plataforma multiprocesador. Han analizado el código fuente original para determinar qué partes se pueden paralelizar y cuáles no.

**Apartado A (Cálculo de la fracción secuencial máxima):**
El equipo se ha marcado como objetivo obtener una **aceleración de 80** ejecutando el programa en un computador paralelo de **100 procesadores**.
Aplicando la Ley de Amdahl, calcule **cuál es la fracción máxima del programa que puede ser estrictamente secuencial** (es decir, que no se puede paralelizar) para lograr este ambicioso objetivo. _(Muestre sus cálculos y dé el resultado en porcentaje)._

**Apartado B (Límite máximo teórico):**
Suponga ahora que, tras reescribir parte del código, los ingenieros logran optimizar el programa hasta dejar la parte puramente secuencial en exactamente un **5%** ($1-f = 0.05$).
Si la empresa decidiera invertir un presupuesto infinito y les proporcionara un supercomputador con **infinitos procesadores**, ¿cuál sería la **aceleración máxima teórica** que alcanzaría el programa?. _(Justifique su respuesta teóricamente)._

Queremos calcular:

$\lim_{p \to \infty} \frac{1}{0.05 + \frac{0.95}{p}}$

Cuando $p \to \infty$: $\frac{95}{p} \to 0$

Entonces queda:$\frac{1}{0.05 + 0} = \frac{1}{0.05} = 20$

**Como mucho aceleraríamos el programa un factor de 20**

**Apartado C (Clasificación de la arquitectura):**
Finalmente, el equipo decide ejecutar la aplicación en un clúster formado por múltiples ordenadores independientes conectados a través de una red de interconexión. Cada ordenador (nodo) cuenta con su propia memoria privada y ejecuta su propio Sistema Operativo.
Responda brevemente a estas dos cuestiones:

1. ¿En qué categoría de la **Taxonomía de Flynn** se clasifica este clúster (SIMD o MIMD)?
2. Dado que no comparten el espacio de direcciones de memoria, ¿**qué modelo o paradigma de comunicación** deben utilizar explícitamente los ingenieros en su código para intercambiar datos entre los distintos procesadores?
