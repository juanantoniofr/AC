# Evaluación de Prestaciones

## Tabla de contenidos

- [Factores clave de evaluación](#factores-clave-de-evaluación)
- [Métricas de rendimiento](#métricas-de-rendimiento)
  - [Productividad](#productividad)
  - [Tiempo de ejecución](#tiempo-de-ejecución)
  - [Otras métricas de rendimiento](#otras-métricas-de-rendimiento)
  - [Ley de Amdahl](#ley-de-amdahl)
- [Coste](#coste)
- [Consumo de potencia](#consumo-de-potencia)
- [Benchmarks](#benchmarks)
- [Leyes y tendencias](#leyes-y-tendencias)

## Factores clave de evaluación

- 1. Rendimiento (En determinados sectores puede llegar a ser decisiva la escalabilidad y la fiabilidad a la hora de evaluar un sistema).
  - CPI.
  - Frecuencia de reloj.
  - Complejidad de las instrucciones.
- 2. Coste
- 3. Consumo de potencia

## Métricas de rendimiento

- Hay dos métricas diferentes:
  1. **Productividad**
  2. **Tiempo de ejecución**

### Productividad

La **productividad** se define como el **número de tareas que un computador realiza por unidad de tiempo**. Es una de las dos métricas fundamentales para evaluar el rendimiento de un sistema, siendo la otra el tiempo de ejecución (o tiempo de respuesta).

Sobre este concepto, el material aportado destaca dos aspectos clave:

- **Ámbito de aplicación:** Es una métrica especialmente adecuada para medir el rendimiento en los **centros de proceso de datos**, donde lo que prima es el volumen global de trabajo que el sistema es capaz de sacar adelante, más que el tiempo que tarda en finalizar un programa individual.
- **Su papel protagonista en el diseño actual de procesadores:** Históricamente, el rendimiento se mejoraba logrando que las instrucciones se ejecutaran más rápido (reduciendo el tiempo de respuesta gracias al aumento de la frecuencia de reloj). Sin embargo, al alcanzarse los límites físicos de disipación de calor ("el muro de la potencia"), la industria tuvo que cambiar de estrategia y empezar a fabricar procesadores multinúcleo. Con este nuevo paradigma arquitectónico, **la mejora del rendimiento de los computadores ya no se basa en el tiempo de respuesta, sino en aumentar la productividad**.

### Tiempo de ejecución

- Es importante desde el punto de vista del usuario.
- Definición: Es el **tiempo total** que un computador tarda en ejecutar un programa.

=> Entonces el rendimiento (**R**) es la inversa del tiempo de ejecución (**T**).

$$
R = \frac{1}{T}
$$

A partir del Rendimiento, **podemos comparar dos computadores** mediante el **factor de aceleración**, (n), que se define como:

$$
n = \frac{R_x}{R_y} = \frac{T_y}{T_x}
$$

#### Formas de medir el tiempo de ejecución

1. **Tiempo de reloj:** Tiempo total que tarda una tarea en ejecutarse, tiene en cuenta los tiempos de acceso a memoria, E/S (disco, red) y tiempo de CPU (incluido el asignado a otros procesos).

2. **Tiempo de CPU:** No incluye los tiempos de acceso a memoria, E/S (disco, red) y tiempo de CPU (incluido el asignado a otros procesos).

   2.1 El **tiempo de CPU** se divide en tiempo de CPU **de usuario** (el empleado por el propio proceso) y tiempo de CPU **de sistema** (el empleado por el sistema para atender peticiones del proceso).

   $$
   TCPU = TCPU_{usuario} + TCPU_{sistema}
   $$

   2.2 Formula para calcular el tiempo de CPU

   $$
       t_{CPU} = n_{ciclos} \cdot t_{ciclos} = \frac{n_{ciclos}}{f_{reloj}}
   $$

   donde
   - **n\_{ciclos}** => Número de ciclos de reloj que la CPU dedica al programa => $\frac{ciclos}{programa}$
   - **t\_{ciclos}** => (**Periodo de reloj**) => Se define como el tiempo que dura un ciclo de reloj => $\frac{segundos}{ciclo}$, se suele medir en nanosegundos (ns).
   - **f\_{reloj}** => (**frecuencia de reloj**) => Se define como el número de ciclos que la CPU puede ejecutar en un segundo => $\frac{ciclos}{segundo}$, se suele medir en hercios (Hz).
   - **Ciclo** de reloj => es el intervalo de **tiempo entre dos pulsos consecutivos del reloj del procesador**.

**CPI** => (**Cycles Per Instruction**) => Es el número **medio** de ciclos de reloj que se necesitan para ejecutar una instrucción.

**Redefinición de la fórmula del tiempo de CPU a partir de CPI:**

_Ecuación clásica de medición del Rendimiento de un computador_

$$
t_{CPU} = n_{instrucciones} \cdot CPI \cdot t_{ciclo} = \frac{n_{instrucciones} \cdot CPI}{f_{reloj}}
$$

### Otras métricas de rendimiento

| Métrica                                                            | Descripción                                                                                                                                                                                       |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **MIPS** (Millones de Instrucciones por Segundo)                   | Es el número de millones de instrucciones que un computador puede ejecutar en un segundo. Se calcula como: $MIPS = \frac{n_{instrucciones}}{t_{CPU} \cdot 10^6}$                                  |
| **MFLOPS** (Millones de Operaciones de Punto Flotante por Segundo) | Es el número de millones de operaciones de punto flotante que un computador puede ejecutar en un segundo. Se calcula como: $MFLOPS = \frac{n_{operaciones\_punto\_flotante}}{t_{CPU} \cdot 10^6}$ |

### Ley de Amdahl:

**¿puedo mejorar el rendimiento de un programa de forma indefinida?**

- No, la **ley de Amdahl** establece que el rendimiento máximo que se puede obtener al mejorar una parte de un sistema está limitado por la proporción de tiempo que esa parte representa en el sistema total. En otras palabras, si una parte del programa no se puede mejorar, el rendimiento total estará limitado por esa parte.

- Factor de mejora máxima (n) que se puede obtener al mejorar una parte del sistema:

$$
a_{s} = \frac{R_{mejorado}}{R_{original}} = \frac{T_{original}}{T_{mejorado}} = \frac{1}{(1 - F) + \frac{F}{S}}
$$

Donde:

- **a_s** => Factor de mejora del sistema.
- **R_mejorado** => Rendimiento del sistema mejorado.
- **R_original** => Rendimiento del sistema original.
- **T_original** => Tiempo de ejecución del sistema original.
- **T_mejorado** => Tiempo de ejecución del sistema mejorado.
- **F** => Proporción del tiempo de ejecución que se puede mejorar.
- **1 - F** => Proporción del tiempo de ejecución que no se puede mejorar.
- **S** => Factor de mejora de la parte mejorada.

$$
T_{mejorado} = (1 - F) \cdot T_{original} + \frac{F \cdot T_{original}}{S}
$$

## Coste

Los factores a tener en cuenta en el coste de fabricación de los circuitos integrados son:

Dado el proceso de fabricación (tecnología de fabricación) consiste en crear circuitos integrados a partir de obleas de silicio, por lo tanto:

- El coste de fabricación está directamente relacionado con el área que ocupa, ya qué a mayor area:
  - Menor rendimiento (menos chips por oblea).
  - Mayor es el coste de los defectos.

**Conclusión**: El **coste de fabricación** de un circuito integrado está directamente relacionado con la **complejidad de su diseño**.

## Consumo de potencia

- El consumo de potencia viene determinado principalmente por la **potencia dinámica** (aquella que se consume en las transiciones de los niveles lógicos - de 0 a 1 y de 1 a 0 -).

- La formula para obtener la potencia dinámica **de un transistor** es:
  $$
  P_{dinámica} = C_{l} \cdot V^2 \cdot f
  $$

Donde:

- **C_l** => Capacitancia de carga o carga capacitiva (capacidad de almacenar carga eléctrica), depende de la tecnología y el número de transistores conectados a la salida.
- **V** => Voltaje de alimentación o voltaje aplicado.
- **f** => Frecuencia de trabajo o de conmutación => es la frecuencia de las transiciones de 0 a 1.

- La formula para obtener la potencia dinámica **de un circuito síncrono integrado** viene dada por la suma de la potencia dinámica de cada uno de los transistores que lo componen, por lo tanto:

  $$
  \sum_{i=1}^{n} P_{dinámica\_i} = \sum_{i=1}^{n} C_{L}{^i} \cdot V^2 \cdot f_{s}{^i}
  $$

- Teniendo en cuenta que:

  $$
  f_{s}{^i} = a^{i} \cdot f
  $$

  Donde **a<sup>i</sup>** => Es el factor de actividad del transistor i, que representa **la probabilidad** de que el transistor i cambie de estado (de 0 a 1 o de 1 a 0) en un ciclo de reloj.

- Tenemos
  $$
  \sum_{i=1}^{n} P_{dinámica\_i} = \sum_{i=1}^{n} C_{L}{^i} \cdot V^2 \cdot a^{i} \cdot f = V^2 \cdot f \cdot \sum_{i=1}^{n} C_{L}{^i} \cdot a^{i}
  $$

## Benchmarks

- Son programas de referencia que se utilizan para medir el rendimiento de un sistema.
- Tenemos bencmarks que miden el rendimiento de un sistema en general (ej: SPEC) y otros que miden el rendimiento de un sistema en una tarea específica (ej: Linpack).
- Otros miden el consumo de potencia (ej: SPECpower).

Las fuentes destacan específicamente el uso del benchmark **SPECpower** para evaluar el **consumo de potencia en servidores**, así como para analizar la **relación entre el rendimiento y la energía consumida**.

Este benchmark utiliza aplicaciones de negocio implementadas en Java que hacen un uso intensivo del procesador, de las memorias caché, del sistema de memoria y de la red de interconexión del multiprocesador.

Para llevar a cabo esta evaluación, SPECpower se basa en las siguientes métricas:

- **Rendimiento:** Se mide en operaciones de servidor Java por segundo, una métrica denominada **`ssj_ops`** (del inglés, _server side Java operations / second_).
- **Eficiencia:** Como medida principal de eficiencia, se evalúa el rendimiento por unidad de potencia consumida, expresado en **`ssj_ops/watt`**.
- **Índice global:** Para obtener una calificación general del sistema, se calcula un índice (`ssj_ops/w global`) que resulta de dividir la suma total de las operaciones ejecutadas entre la suma total de la potencia consumida.

Estos resultados se obtienen sometiendo al computador a **diferentes niveles de carga de trabajo** (desde el 100% de carga hasta un estado de inactividad activa). Gracias a esto, **es posible comparar de forma objetiva distintos procesadores** para determinar cuál de ellos ofrece la **mayor eficiencia (mejor rendimiento por vatio consumido)** y el menor consumo general de energía.

## Leyes y tendencias

- 1. Ley de Amdahl.
- 2. Ley de Moore.
- 3. Muro de la Potencia.
- 4. Paso a multiprocesadores.

_Notas:_

En determinados **sectores** puede ser **decisivos** otros factores como:

- 1. **Sistema escalables** => si el **rendimiento** aumenta proporcionalmente al aumento de **recursos**.
- 2. **Sitemas fiables** => si es capaz de funcionar de forma correcta y continua.
