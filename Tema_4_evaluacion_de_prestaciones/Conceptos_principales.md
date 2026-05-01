# Evaluación de Prestaciones

## Factores clave de evaluación

- 1. Rendimiento
- 2. Coste
- 3. Consumo de potencia
- 4. Escalabilidad
- 5. Fiabilidad

## Métricas de rendimiento

- Hay dos métricas diferentes:
  1. **Productividad**
  2. **Tiempo de ejecución**

### Tiempo de ejecución

- Es importante desde el punto de vista del usuario.
- Es el **tiempo total** que un computador tarda en ejecutar un programa.

=> Entonces el rendimiento (**R**) es la inversa del tiempo de ejecución (**T**).

$$
R = \frac{1}{T}
$$

A partir del Rendimiento, **\*podemos comparar dos computadores** mediante el **factor de aceleración**, (n), que se define como:

$$
n = \frac{R_x}{R_y} = \frac{T_y}{T_x}
$$

#### Formas de medir el tiempo de ejecución

1. **Tiempo de reloj:** Tiempo total que tarda una tarea en ejecutarse, tiene en cuenta los tiempos de acceso a memoria, E/S (disco, red) y tiempo de CPU (incluido el asignado a otros procesos).

2. **Tiempo de CPU:** NO incluye los tiempos de acceso a memoria, E/S (disco, red) y tiempo de CPU (incluido el asignado a otros procesos).

   2.1 El **tiempo de CPU** se divide en tiempo de CPU **de usuario** (el empleado por el propio proceso) y tiempo de CPU **de sistema** (el empleado por el sistema para atender peticiones del proceso).

   $$
   TCPU = TCPU_{usuario} + TCPU_{sistema}
   $$

   2.2 Formula para calcular el tiempo de CPU

   $$
       t_{CPU} = n_{ciclos} \cdot t_{ciclos} = \frac{n_{ciclos}}{f_{reloj}}
   $$

   donde
   - n\_{ciclos} se define como: Número de ciclos de reloj que la CPU dedica al programa => $\frac{ciclos}{programa}$
   - t\_{ciclos} se define como: Periodo de reloj => $\frac{segundos}{ciclo}$
   - {f\_{reloj}} se define como: frecuencia de reloj.
   - **Ciclo** de reloj: es el intervalo de tiempo entre dos pulsos consecutivos del reloj del procesador.
   - La **frecuencia** es el número de ciclos de reloj que ocurren cada segundo. Se mide en hercios (Hz): 1Hz es igual a 1 ciclo por segundo.
   - Duración del ciclo = $\frac{1}{frecuencia}$

## Leyes y tendencias

- 1. Ley de Amdahl.
- 2. Ley de Moore.
- 3. Muro de la Potencia.
- 4. Paso a multiprocesadores.

_Notas:_

En determinados **sectores** puede ser **decisivos** otros factores como:

- 1. **Sistema escalables** => si el **rendimiento** aumenta proporcionalmente al aumento de **recursos**.
- 2. **Sitemas fiables** => si es capaz de funcionar de forma correcta y continua.
