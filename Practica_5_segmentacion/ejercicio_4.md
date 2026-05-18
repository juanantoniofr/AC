# Ejercicio 4.

## Enunciado

Repita los Ejercicios 1, 2 y 3 suponiendo un RISCV con todos los desvíos activos. Para cada desvío indique de qué registro de segmentación o unidad funcional se toma el dato y a qué registro de segmentación o unidad funcional se lleva.

- ¿Qué conclusiones se obtienen por el hecho de utilizar desvíos?
- ¿Cuántos bloqueos de cada tipo se han eliminado?

Finalmente, compruebe utilizando el simulador RISCV (con Adelantamientos activado) que los resultados obtenidos son correctos.

## Solución

### Código

```asm
la a1, x # x base address
addi a4, a1, 400 # x address loop end

bucle:
    lw a2, 0(a1) # x[i]
    addi a2, a2, 5 # x[i] + 5
    sw a2, 0(a1) # store back
    addi a1, a1, 4 # i++
    blt a1, a4, bucle # loop i<100

li a7 , 10 # Syscall exit
ecall
```

### Cronograma sin desvios ejercicio 1 - Primera iteración

|     | Ciclo                     | 1   | 2   | 3   | 4   | 5    | 6   | 7   | 8    | 9   | 10  | 11  | 12   | 13  | 14  | 15   | 16  | 17  | 18  | 19   | 20      |
| :-- | :------------------------ | :-- | :-- | :-- | :-- | :--- | :-- | :-- | :--- | :-- | :-- | :-- | :--- | :-- | :-- | :--- | :-- | :-- | :-- | :--- | :------ |
| 1   | `auipc a1, 0xfff0`        | IF  | ID  | EX  | MEM | _WB_ |     |     |      |     |     |     |      |     |     |      |     |     |     |      |         |
| 2   | `addi a1, a1, 0`          |     | IF  | -   | -   | _ID_ | EX  | MEM | _WB_ |     |     |     |      |     |     |      |     |     |     |      |         |
| 3   | `addi a4, x11, 400`       |     |     |     |     | IF   | -   | -   | _ID_ |     |     |     |      |     |     |      |     |     |     |      |         |
| 4   | `lw a2, 0(a1)`            |     |     |     |     |      |     |     | IF   | ID  | EX  | MEM | _WB_ |     |     |      |     |     |     |      |         |
| 5   | `addi a2, a2, 5`          |     |     |     |     |      |     |     |      | IF  | -   | -   | _ID_ | EX  | MEM | _WB_ |     |     |     |      |         |
| 6   | `sw a2, 0(a1)`            |     |     |     |     |      |     |     |      |     |     |     | _IF_ | -   | -   | _ID_ | EX  | MEM |     |      |         |
| 7   | `addi a1, a1, 4`          |     |     |     |     |      |     |     |      |     |     |     |      |     |     | _IF_ | ID  | EX  | MEM | _WB_ |         |
| 8   | `blt a1, a4, bucle`       |     |     |     |     |      |     |     |      |     |     |     |      |     |     |      | IF  | -   | -   | _ID_ | EX      |
| 9   | `addi a7, x0, 10`         |     |     |     |     |      |     |     |      |     |     |     |      |     |     |      |     |     |     | _IF_ | _flush_ |
| 10  | `lw a2, 0(a1)` (2ª iter.) |     |     |     |     |      |     |     |      |     |     |     |      |     |     |      |     |     |     |      | IF      |

### Repetimos ejercicio 1 con desvios activos - Primera iteración

¡Perfecto! Vamos a aplicar exactamente los **4 pasos estratégicos** que acabamos de comentar para resolver el código que me has pasado, manteniendo el texto del programa inalterado y utilizando la notación `_w()` $\rightarrow$ `_r()` para simular las flechas del simulador VisualRISCV32.

_(Nota: Como en el código que has proporcionado no hay ninguna etiqueta `bucle:` escrita en las instrucciones anteriores, he asumido lógicamente que el salto condicional de la línea 8 tiene como destino la instrucción `lw` de la línea 4, tal y como ocurría en los ejemplos de tus apuntes)_.

### Traza de Ejecución: Productor `_w()` $\rightarrow$ Consumidor `_r()`

| Línea | Instrucción         |  1  |  2  |             3             |                    4                     |             5              |         6         |             7              |                    8                     |         9         |            10             |        11         |   12    | 13  |
| :---- | :------------------ | :-: | :-: | :-----------------------: | :--------------------------------------: | :------------------------: | :---------------: | :------------------------: | :--------------------------------------: | :---------------: | :-----------------------: | :---------------: | :-----: | :-: |
| 1     | `auipc a1, 0xfff0`  | IF  | ID  | EX<br>**\_w(a1)\_EX/MEM** |                   MEM                    |             WB             |                   |                            |                                          |                   |                           |                   |         |     |
| 2     | `addi a1, a1, 0`    |     | IF  |            ID             | EX<br>**_r(a1)_**<br>**\_w(a1)\_EX/MEM** | MEM<br>**\_w(a1)\_MEM/WB** |        WB         |                            |                                          |                   |                           |                   |         |     |
| 3     | `addi a4, a1, 400`  |     |     |            IF             |                    ID                    |     EX<br>**_r(a1)_**      |        MEM        |             WB             |                                          |                   |                           |                   |         |     |
| 4     | `lw a2, 0(a1)`      |     |     |                           |                    IF                    |             ID             | EX<br>**_r(a1)_** | MEM<br>**\_w(a2)\_MEM/WB** |                    WB                    |                   |                           |                   |         |     |
| 5     | `addi a2, a2, 5`    |     |     |                           |                                          |             IF             |        ID         |             ID             | EX<br>**_r(a2)_**<br>**\_w(a2)\_EX/MEM** |        MEM        |            WB             |                   |         |     |
| 6     | `sw a2, 0(a1)`      |     |     |                           |                                          |                            |        IF         |             IF             |                    ID                    | EX<br>**_r(a2)_** |            MEM            |        WB         |         |     |
| 7     | `addi a1, a1, 4`    |     |     |                           |                                          |                            |                   |                            |                    IF                    |        ID         | EX<br>**\_w(a1)\_EX/MEM** |        MEM        |   WB    |     |
| 8     | `blt a1, a4, bucle` |     |     |                           |                                          |                            |                   |                            |                                          |        IF         |            ID             | ID<br>**_r(a1)_** |   EX    | MEM |
| 9     | `addi a7, x0, 10`   |     |     |                           |                                          |                            |                   |                            |                                          |                   |            IF             |        IF         | _abort_ |     |
| 10    | `lw a2, 0(a1)`      |     |     |                           |                                          |                            |                   |                            |                                          |                   |                           |                   |   IF    | ID  |

---

### test a ver si me sale a mi solo

| Ciclo               | 1   | 2   | 3                  | 4                   | 5        | 6   | 7                   | 8                        | 9        | 10             | 11       | 12      | 13  | 14  |
| :------------------ | --- | --- | ------------------ | ------------------- | -------- | --- | ------------------- | ------------------------ | -------- | -------------- | -------- | ------- | --- | --- |
| `auipc a1, 0xfff0`  | IF  | ID  | EX w(a1) -> EX/MEM | MEM w(a1) -> MEM/WB | WB       |     |                     |                          |          |                |          |         |     |     |
| `addi a1, a1, 0`    |     | IF  | ID                 | r(a1) EX            | MEM      | WB  |                     |                          |          |                |          |         |     |     |
| `addi a4, a1, 400`  |     |     | IF                 | ID                  | r(a1) EX | MEM | WB                  |                          |          |                |          |         |     |     |
| `lw a2, 0(a1)`      |     |     |                    | IF                  | ID       | EX  | MEM w(a2) -> MEM/WB | WB                       |          |                |          |         |     |     |
| `addi a2, a2, 5`    |     |     |                    |                     | IF       | ID  | ID                  | r(a2) EX w(a2) -> EX/MEM | MEM      | WB             |          |         |     |     |
| `sw a2, 0(a1)`      |     |     |                    |                     |          |     | IF                  | ID                       | r(a2) EX | MEM            | WB       |         |     |     |
| `addi a1, a1, 4`    |     |     |                    |                     |          |     |                     | IF                       | ID       | EX w(a1) EX/ID | MEM      | WB      |     |     |
| `blt a1, a4, bucle` |     |     |                    |                     |          |     |                     |                          | IF       | **ID**         | r(a1) ID | _FLUSH_ |     |     |
| `addi a7, x0, 10`   |     |     |                    |                     |          |     |                     |                          |          | -              | IF       | -       |     |     |

### Análisis paso a paso (Aplicando la estrategia Productor $\rightarrow$ Consumidor):

A continuación, te detallo cómo habríamos deducido cada cruce aplicando nuestra estrategia:

**1. Dependencia de `a1` (Línea 1 $\rightarrow$ Línea 2)**

- **Consumidor (L2):** Necesita `a1` al inicio de su EX (ciclo 4).
- **Productor (L1):** Calcula `a1` al final de su EX (ciclo 3).
- **Cruce:** Llega a tiempo. Se traza la diagonal `_w(a1)_EX/MEM` en ciclo 3 $\rightarrow$ `_r(a1)_` en ciclo 4.

**2. Dependencia de `a1` (Línea 2 $\rightarrow$ Línea 3)**

- **Consumidor (L3):** Necesita `a1` al inicio de su EX (ciclo 5).
- **Productor (L2):** Calcula el nuevo `a1` al final de su EX (ciclo 4).
- **Cruce:** Llega a tiempo. Desvío `_w(a1)_EX/MEM` en ciclo 4 $\rightarrow$ `_r(a1)_` en ciclo 5.

**3. Dependencia de `a1` (Línea 2 $\rightarrow$ Línea 4)**

- _Ojo aquí:_ La L4 necesita `a1` como dirección base. ¿Quién fue el último en escribir `a1`? Fue la L2 (la L3 escribió en `a4`).
- **Consumidor (L4):** Necesita `a1` al inicio de su EX (ciclo 6).
- **Productor (L2):** Terminó de calcularlo en el ciclo 4, pero en el ciclo 5 el dato sigue viajando por la etapa MEM.
- **Cruce:** Se desvía desde la salida de MEM de L2. Desvío `_w(a1)_MEM/WB` en ciclo 5 $\rightarrow$ `_r(a1)_` en ciclo 6.

**4. Dependencia de `a2` (Línea 4 $\rightarrow$ Línea 5) - _Load-Use Stall_**

- **Consumidor (L5):** Necesita sumar `a2` al inicio de su EX (debería ser ciclo 7).
- **Productor (L4):** Al ser un `lw`, el dato `a2` no sale de la memoria hasta terminar su etapa MEM (final del ciclo 7).
- **Cruce:** ¡Imposible, no se puede viajar atrás en el tiempo! **Se fuerza 1 bloqueo (ID en ciclo 7)**. L5 retrasa su EX al ciclo 8. Ahora sí encaja: Desvío `_w(a2)_MEM/WB` de L4 en ciclo 7 $\rightarrow$ `_r(a2)_` de L5 en ciclo 8. _(Este bloqueo arrastra la etapa IF de la L6)_.

**5. Dependencia de `a2` (Línea 5 $\rightarrow$ Línea 6)**

- **Consumidor (L6):** L6 necesita `a2` en su etapa EX (ciclo 9) para guardarlo. _(Nota: el otro registro, `a1`, lo leyó del banco sin problemas en su etapa ID, ya que L2 terminó en el ciclo 6)_.
- **Productor (L5):** Sumó `a2` y lo tiene listo al final de su EX (ciclo 8).
- **Cruce:** Llega a tiempo. Desvío `_w(a2)_EX/MEM` en ciclo 8 $\rightarrow$ `_r(a2)_` en ciclo 9.

**6. Dependencia de `a1` (Línea 7 $\rightarrow$ Línea 8) - _ALU-Branch Stall_**

- **Consumidor (L8):** Es un salto condicional, evalúa en su etapa ID (debería ser ciclo 10). Necesita `a1` y `a4`. (`a4` se calculó muy atrás en L3, lo lee directamente del banco).
- **Productor (L7):** Calcula el incremento de `a1` al final de su etapa EX (ciclo 10).
- **Cruce:** ¡Imposible, ocurren a la vez! **Se fuerza 1 bloqueo (ID en L8)**. L8 espera en ID hasta el ciclo 11. La L7 saca el dato adelantado al terminar EX en el ciclo 10: Desvío `_w(a1)_EX/MEM` en ciclo 10 $\rightarrow$ entrada al comparador en ID `_r(a1)_` en ciclo 11.

_(Finalmente, en el ciclo 11 el salto de la línea 8 se resuelve como "Tomado", por lo que la instrucción de la línea 9 que había entrado preventivamente en la etapa IF se aborta y en el ciclo 12 se empieza a buscar la instrucción correcta del bucle)._

![alt text](simulacion_primera_iteracion_con_devios.png)
