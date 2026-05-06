# Ejercicio 1.3: Optimización de código

## Aparatado a: accesos a memoria

Al recorrer la matriz por filas, incremento en 4 bytes (1 palabra) la direcciones a las que accedo, como en cada linea caben 4 palabras, después de un fallo, las otras tres direcciones de memoria tienen la misma etiqueta y están en cache.

| Dirección (hex) | Etiqueta (hex) | Desplazamiento (hex) | Fallo/Acierto   |
| :-------------- | :------------- | :------------------- | :-------------- |
| `0x10010000`    | `0x1001000`    | `0x0`                | Fallo (Forzoso) |
| `0x10010004`    | `0x1001000`    | `0x4`                | Acierto         |
| `0x10010008`    | `0x1001000`    | `0x8`                | Acierto         |
| `0x1001000C`    | `0x1001000`    | `0xC`                | Acierto         |
| `0x10010010`    | `0x1001010`    | `0x0`                | Fallo (Forzoso) |
| `0x10010014`    | `0x1001010`    | `0x4`                | Acierto         |
| `0x10010018`    | `0x1001010`    | `0x8`                | Acierto         |
| `0x1001001C`    | `0x1001010`    | `0xC`                | Acierto         |
| `0x10010020`    | `0x1001020`    | `0x0`                | Fallo (Forzoso) |

## Apartado b:

### ¿Cuál es la nueva tasa de fallo?

- Al recorrer la primera fila (32 accesos), tendremos 8 fallos forzosos (25%) y 24 de aciertos (75% ).
- El proceso se va a repetir para cada fila (32) y no tendremos ningún fallo por capacidad ya que los bloques se ubican en cache por primera vez.

Entonces:

- Fallos forzosos = 8 /\* 32 = 256
- Aciertos = 24 /\* 32 = 768

### ¿por qué mejora?

Por que al direccionar una posición de memoria nos traemos un bloque de 4 palabras que son las 3 siguientes posiciones a leer, al tenerlas ya en cache, esos 3 siguientes accesos a memoria son aciertos en cache.

### ¿qué tipo de fallo se elimina?

Se eliminan fallos forzosos.

### ¿qué tipo de localidad se está aprovechando?

La localidad espacial, ya que leemos "pronto" direcciones de memoria contiguas.
