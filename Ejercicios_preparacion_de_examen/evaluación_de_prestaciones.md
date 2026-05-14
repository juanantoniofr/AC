# Ejercicios sobre evaluación de prestaciones

## Cuestión 1

### Enunciado

Suponga que se quiere mejorar el rendimiento de un computador aumentando la frecuencia de reloj pero manteniendo el consumo de potencia. Para ello, es posible reducir
el voltaje un 20%. Para que el computador funcione con la nueva frecuencia de reloj, han sido necesarios cambios en su diseño interno que han supuesto un aumento del CPI del
5%. ¿En qué porcentaje se reducirá el tiempo de ejecución del nuevo diseño?

### Solución

- Queremos mejorar el **rendimiento** aumentando la **frecuencia de reloj** pero manteniendo el **consumo de potencia**.
- Reducimos el voltaje (V) en un 20%.
- Frecuencia de reloj aumenta en x%.
- Cambio de diseño provoca aumento del CPI en un 5%.
- **¿cuanto de reducirá el tiempo de ejecución?**

Tenemos:

#### 1. Usamos la fórmula del consumo de potencia dinámica: $P = C_{L} \cdot V^2 \cdot f$.

Como el enunciado dice "manteniendo el consumo de potencia", igualamos la potencia original ($P1$) a la nueva ($P2$). Como no nos dicen nada de la capacitancia ($C_{L}$), suponemos que $C1 = C2$.
Por tanto, nos queda:
$V_1^2 \cdot f_1 = V_2^2 \cdot f_2$

#### 2. El cálculo de la nueva frecuencia

El enunciado dice que el voltaje se reduce un 20%, por lo que $V_2 = 0.8 \cdot V_1$. Sustituimos esto en la ecuación:
$V_1^2 \cdot f_1 = (0.8 \cdot V_1)^2 \cdot f_2$
$V_1^2 \cdot f_1 = 0.64 \cdot V_1^2 \cdot f_2$

Esto nos dice que el término del voltaje al cuadrado se ha reducido al 64%. Para hallar la nueva frecuencia ($f_2$), tenemos que despejarla:
$f_2 = \frac{1}{0.64} \cdot f_1 = 1.56 \cdot f_1$
_(Esto significa que la frecuencia ha aumentado un 56%)_.

#### 3. El cálculo final del tiempo de ejecución

La pregunta no nos pide el voltaje ni la frecuencia, sino **en qué porcentaje se reducirá el tiempo de ejecución**. Para ello, usamos la ecuación fundamental del rendimiento: $t = \frac{n \cdot CPI}{f}$.

Sabemos dos cosas sobre el nuevo diseño:

- La nueva frecuencia es un 56% mayor: $f_2 = 1.56 \cdot f_1$.
- El CPI ha aumentado un 5%: $CPI_2 = 1.05 \cdot CPI_1$.

Sustituyendo estos valores en la fórmula del tiempo (suponiendo que el número de instrucciones $n$ no cambia):
$t_2 = \frac{n \cdot (1.05 \cdot CPI_1)}{1.56 \cdot f_1}$

Si agrupamos los números, obtenemos la relación entre el tiempo nuevo y el antiguo:
$t_2 = \frac{1.05}{1.56} \cdot (\frac{n \cdot CPI_1}{f_1}) = 0.67 \cdot t_1$

**Conclusión:**
El nuevo tiempo de ejecución ($t_2$) es el 67% del tiempo original ($t_1$). Por lo tanto, el tiempo de ejecución **se ha reducido exactamente en un 33%** ($100\% - 67\% = 33\%$), que es la opción **b**.

## Cuestión 2

### Enunciado

Suponga que se quiere mejorar el rendimiento de una CPU unificando la tarea que realizan dos instrucciones en una única instrucción. La unificación ha provocado un aumento del periodo de reloj del 10%.

- ¿Qué porcentaje de instrucciones dedicadas a esta tarea tienen que ejecutarse en un programa de la CPU original para que compense la unificación? Suponga que el CPI medio del programa se mantiene.

### Solución

Para resolver este problema, debemos plantear una inecuación donde el tiempo de ejecución del nuevo procesador ($t_2$) sea estrictamente menor que el tiempo del procesador original ($t_1$), garantizando así que la modificación compensa.

El desarrollo matemático paso a paso es el siguiente:

#### 1. Tiempo de ejecución original:\*\*

El tiempo de la CPU original se define por la ecuación fundamental:
$t_1 = n \cdot CPI \cdot T_1$
_(Donde $n$ es el número total de instrucciones, y $T_1$ el periodo de reloj original)._

#### 2. Tiempo de ejecución del nuevo diseño:

Llamemos **$p$** al porcentaje de instrucciones de nuestro programa que están dedicadas a esa tarea unificable.

- Las instrucciones dedicadas a la tarea en el diseño original son $p \cdot n$. Como ahora dos instrucciones se unifican en una sola, en el nuevo diseño pasarán a ser la mitad: $\frac{p \cdot n}{2}$.
- Las instrucciones que no pertenecen a esa tarea se quedan exactamente igual: $(1-p) \cdot n$.
- El enunciado indica que el periodo de reloj aumenta un 10%, por lo que el nuevo periodo es **$1.1 \cdot T_1$**.
- El CPI medio se mantiene igual.

Sustituyendo esto en la fórmula, el nuevo tiempo de ejecución es:
$t_2 = \left( \frac{p \cdot n}{2} + (1-p) \cdot n \right) \cdot CPI \cdot 1.1 \cdot T_1$

#### 3. Planteamiento y resolución de la inecuación:\*\*

Queremos que el nuevo diseño sea más rápido, es decir, $t_2 < t_1$. Sustituimos ambas fórmulas:
$\left( \frac{p \cdot n}{2} + (1-p) \cdot n \right) \cdot CPI \cdot 1.1 \cdot T_1 < n \cdot CPI \cdot T_1$

Como $n$, $CPI$ y $T_1$ están multiplicando en ambos lados, podemos dividirlos y eliminarlos de la ecuación para simplificar:
$\left( \frac{p}{2} + (1-p) \right) \cdot 1.1 < 1$

Agrupamos las $p$ dentro del paréntesis ($\frac{p}{2} - p = -\frac{p}{2}$):
$\left( 1 - \frac{p}{2} \right) \cdot 1.1 < 1$

Despejamos el paréntesis pasando el $1.1$ dividiendo:
$1 - \frac{p}{2} < \frac{1}{1.1}$
$1 - \frac{p}{2} < 0.91$

Pasamos $\frac{p}{2}$ a la derecha y el $0.91$ restando a la izquierda:
$1 - 0.91 < \frac{p}{2}$
$0.09 < \frac{p}{2}$

Multiplicamos por 2 para despejar la $p$:
**$p > 0.18$**

Por lo tanto, la proporción de estas instrucciones en el programa original tiene que ser **mayor de un 18%** para que el aumento del periodo de reloj compense la reducción del número de instrucciones.
