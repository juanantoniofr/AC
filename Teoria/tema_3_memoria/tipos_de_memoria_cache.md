# Tipos de memoria caché

Según su **estructura interna y la forma de ubicar los bloques** de memoria principal, las memorias caché se clasifican en tres tipos:

## Caché de correspondencia directa (o mapeado directo):

Cada bloque de memoria tiene asociada una **única línea** exclusiva en la que puede ubicarse dentro de la caché. Para determinar la línea se utiliza la función módulo: `Dirección-de-bloque MOD Número-de-líneas`.

- _Ventajas:_ Tiene una **baja complejidad hardware** (requiere un único comparador), lo que permite una identificación del bloque muy rápida (bajo tiempo de acierto) y una menor sobrecarga de memoria al usar etiquetas pequeñas.
- _Inconvenientes:_ Presenta una **tasa de fallos alta**, ya que sufren la mayor cantidad de fallos por conflicto al no ofrecer opciones alternativas para ubicar un bloque.

## Caché asociativa por conjuntos (de k vías):

La caché se organiza en varios conjuntos, donde cada conjunto agrupa un número determinado de _k_ líneas (vías). Un bloque de memoria va a un conjunto específico calculado mediante `Dirección-de-bloque MOD Número-de-conjuntos`, pero una vez allí, **puede ubicarse libremente en cualquiera de las k vías** de ese conjunto.

- _Ventajas:_ Al aumentar la asociatividad (tener más vías donde elegir), **disminuyen los fallos por conflicto**.
- _Inconvenientes:_ **Aumenta el coste hardware** (se necesitan más comparadores, multiplexores de línea y etiquetas de mayor tamaño) y el **tiempo de acierto es mayor**.

## Caché totalmente asociativa (o completamente asociativa):

Los bloques de memoria principal pueden ubicarse en **absolutamente cualquier línea** libre de toda la memoria caché.

- _Ventajas:_ Consigue una **baja tasa de fallos**, eliminando por completo los fallos por conflicto (solo se darán fallos forzosos o por capacidad).
- _Inconvenientes:_ Tiene una **alta complejidad hardware**, ya que se necesita un comparador dedicado para cada una de las líneas, lo que hace que solo sea viable para cachés muy pequeñas. Además, su identificación es más lenta y requiere etiquetas de mayor longitud.

---

Por otro lado, si las clasificamos según el **tipo de información que contienen**, existen dos variantes:

## Cachés unificadas (o mixtas):

Almacenan **tanto datos como instrucciones** compartiendo el mismo espacio físico de la caché. Tienen la ventaja de equilibrar la carga de trabajo automáticamente, reduciendo fallos de capacidad si un tipo de información necesita más espacio que el otro.

## Cachés separadas:

Existe una caché dedicada en exclusiva a los **datos** y otra paralela y distinta para las **instrucciones**.

- _Ventajas:_ Aportan un **mayor rendimiento en procesadores segmentados**, ya que evitan bloqueos estructurales. Al tener vías separadas, la etapa de búsqueda de instrucciones (IF) y la etapa de acceso a memoria de datos (MEM) pueden acceder a la caché en el mismo ciclo sin competir por el recurso. También permite que el diseño de cada caché se optimice de forma independiente según su propósito.
- _Inconvenientes:_ Como el espacio está fijado de antemano para cada tipo, no se equilibra la carga automáticamente, lo que puede provocar que la tasa de fallos global sea algo mayor.
