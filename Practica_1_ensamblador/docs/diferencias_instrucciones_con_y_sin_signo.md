## Ejemplo de diferencias entre `lhu` y `lh` en RISC‑V

**¿Qué diferencia hay entre está instrucción: lhu x5, 40(x6) y esta otra lh x5, 40(x6)?**

La diferencia entre **`lhu`** y **`lh`** está en **cómo se interpreta el dato cargado** desde memoria. Ambas son instrucciones **RISC‑V** que cargan **16 bits (halfword)**, pero **difieren en la extensión del signo**.

---

## 1. `lh x5, 40(x6)` — _Load Halfword (con signo)_

- Carga **16 bits** desde la dirección `x6 + 40`.
- El valor se interpreta como **con signo**.
- Se realiza **extensión de signo** hasta el tamaño del registro (32 o 64 bits).

### Ejemplo:

Si en memoria hay:

    0xFF80

(bit más significativo = 1 → número negativo)

Entonces en `x5` se carga:

    0xFFFFFF80   (en RV32)

---

## 2. `lhu x5, 40(x6)` — _Load Halfword Unsigned (sin signo)_

- Carga **16 bits** desde la dirección `x6 + 40`.
- El valor se interpreta como **sin signo**.
- Se realiza **extensión con ceros**.

### Ejemplo:

Si en memoria hay:

    0xFF80

Entonces en `x5` se carga:

    0x0000FF80   (en RV32)

---

## 3. Resumen rápido

| Instrucción | Tamaño cargado | Interpretación | Extensión |
| ----------- | -------------- | -------------- | --------- |
| `lh`        | 16 bits        | Con signo      | Signo     |
| `lhu`       | 16 bits        | Sin signo      | Ceros     |

---

## 4. Cuándo usar cada una

- Usa **`lh`** cuando el dato representa un **entero con signo** (ej. temperaturas, diferencias, valores negativos).
- Usa **`lhu`** cuando el dato es **sin signo** (ej. contadores, máscaras, valores binarios).

Si quieres, puedo mostrarte un **ejemplo paso a paso en memoria y registros** o compararlo con `lb / lbu` y `lw`.

## 5. ¿Qué ocurre si el bit más significativo del halfword es 0?

En ese caso **no hay ninguna diferencia práctica entre `lh` y `lhu`**

---

## Caso: el bit más significativo (MSB) es **0**

El MSB de un _halfword_ (16 bits) es el **bit 15**.  
Si ese bit vale `0`, el valor es **positivo** tanto si se interpreta **con signo** como **sin signo**.

### Ejemplo en memoria

Supongamos que en la dirección `x6 + 40` hay:

```text
0x1234
```

Representación binaria:

```text
0001 0010 0011 0100
^
MSB = 0
```

---

## Resultado de cada instrucción

### `lh x5, 40(x6)` (con signo)

- Se carga el halfword
- Se extiende el signo
- Como el MSB es `0`, la extensión **rellena con ceros**

Resultado en `x5`:

```text
0x00001234
```

### `lhu x5, 40(x6)` (sin signo)

- Se carga el halfword
- Se extiende con ceros

Resultado en `x5`:

```text
0x00001234
```

✅ **Resultado idéntico**

---

## Conclusión clara

- **Si el bit más significativo es 0 → `lh` y `lhu` cargan exactamente el mismo valor.**
- La diferencia solo aparece cuando el MSB es **1**.

### Regla mental rápida

> ❝Si el dato no puede ser negativo, `lh` y `lhu` se comportan igual mientras el MSB sea 0❞
