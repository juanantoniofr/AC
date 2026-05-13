# Políticas de reemplazo

Las **políticas de reemplazo** (o sustitución) determinan qué bloque debe ser expulsado de la memoria caché cuando es necesario cargar uno nuevo. Los bloques candidatos a ser reemplazados dependen de la estructura de la caché: en correspondencia directa solo hay una línea candidata, en las asociativas por conjuntos son las líneas de un conjunto específico, y en las totalmente asociativas puede ser cualquier línea.

Las estrategias de reemplazo que existen son:

- **Aleatoria (Random):** Se elige un bloque al azar. Es la estrategia con la implementación hardware más simple.
- **FIFO (First Input First Out):** Se sustituye el bloque que más tiempo lleva almacenado en la caché.
- **LRU (Least Recently Used):** Se sustituye el bloque que más tiempo lleva en la caché sin haber sido referenciado. Su implementación es más compleja.
- **LFU (Least Frequently Used):** Se expulsa el bloque que menos referencias ha tenido en total.
- **Pseudo-LRU:** Es una implementación simplificada de la LRU que se usa por motivos de coste y eficiencia, aunque no garantiza el reemplazo óptimo.

En la práctica, los esquemas más utilizados son el aleatorio y el Pseudo-LRU.

---

Por otro lado, cuando la CPU intenta escribir un dato en una dirección cuyo bloque no se encuentra almacenado en la memoria caché, se produce un **fallo en escritura**.

Lo que ocurre a continuación depende de la política que tenga implementada el sistema para gestionar estos fallos, existiendo dos posibilidades:

- **Con ubicación en escritura (Write Allocate, WA):** El sistema primero solicita el bloque a la memoria principal y lo ubica en la caché. Una vez que el bloque ha sido transferido a la caché, se escribe el dato sobre él.
- **Sin ubicación en escritura (No Write Allocate, NWA):** El nuevo dato se envía y se escribe directamente en el bloque correspondiente de la memoria principal, pero ese bloque **no se trae** a la memoria caché.
