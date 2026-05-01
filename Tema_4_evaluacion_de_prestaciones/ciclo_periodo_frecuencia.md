Estos tres conceptos son las unidades fundamentales para medir el paso del tiempo y el ritmo de trabajo en el interior de un procesador. Aquí tienes el significado de cada uno y cómo se relacionan:

- **Ciclo de reloj:** Es el evento, "pulso" o unidad de paso básica en la que se divide el funcionamiento del procesador. El tiempo total que la CPU dedica a ejecutar un programa se contabiliza sumando el **número de ciclos de reloj** que han hecho falta para completar todas sus instrucciones.
- **Periodo de reloj ($t_{ciclo}$):** Es la medida que indica **cuánto tiempo físico exacto dura un solo ciclo**. Se mide en segundos por ciclo, aunque en las máquinas modernas se suelen utilizar los nanosegundos ($ns$).
- **Frecuencia de reloj ($f_{reloj}$):** Es el **número total de ciclos que el procesador es capaz de ejecutar en un segundo**. Se expresa en Hercios (Hz, que equivale a ciclos/segundo). Por ejemplo, las fuentes muestran procesadores funcionando a frecuencias como 500 MHz (500 millones de ciclos por segundo) o 2.66 GHz.

**Su relación matemática:**
El periodo y la frecuencia son conceptos **inversamente proporcionales**. Esto se puede observar directamente en la ecuación fundamental para calcular el tiempo de CPU ($t_{CPU}$), donde el tiempo que aporta la CPU a un programa se puede obtener tanto multiplicando los ciclos por el tiempo que dura cada uno (el periodo), como dividiéndolos entre el ritmo al que ocurren (la frecuencia):

**$t_{CPU} = n_{ciclos} \cdot t_{ciclo} = \frac{n_{ciclos}}{f_{reloj}}$**.

_(Nota: de la ecuación anterior se puede deducir matemáticamente una regla de física básica : el Periodo siempre es la inversa matemática de la Frecuencia, es decir, $Periodo = \frac{1}{Frecuencia}$)._
