# Ejercicio 3. Fábrica de ensamblaje — Productor-Consumidor

## Objetivo

Implementar el patrón productor-consumidor mediante una cola compartida de
capacidad limitada, semáforos y exclusión mutua. La sincronización debe impedir
que los productores inserten piezas cuando el almacén está lleno y que los
consumidores retiren piezas cuando está vacío.

## Situación planteada

La fábrica dispone de un almacén temporal con capacidad para cinco piezas. Dos
productores fabrican cinco piezas cada uno y dos consumidores las retiran para
ensamblarlas. En total se deben producir y consumir diez piezas.

## Recursos y mecanismos de sincronización

- **Recurso compartido:** cola `warehouse`, implementada con `ArrayDeque`.
- **Capacidad:** cinco piezas (`CAPACITY = 5`).
- **Semáforo `spaces`:** empieza en 5 y cuenta los espacios libres.
- **Semáforo `elements`:** empieza en 0 y cuenta las piezas disponibles.
- **Mutex:** semáforo justo de un permiso (`new Semaphore(1, true)`) que protege
  las operaciones de inserción y extracción de la cola.
- **Procesos concurrentes:** dos productores y dos consumidores; cada hilo
  procesa cinco piezas.

## Metodología / procedimiento

1. Se creó la cola compartida con capacidad máxima de cinco piezas.
2. Se inicializó `spaces` en 5, porque el almacén comienza vacío y tiene cinco
   lugares disponibles; `elements` se inicializó en 0, porque todavía no hay
   piezas para consumir.
3. Se creó un mutex para que solo un hilo a la vez pudiera modificar la cola.
4. Cada productor espera un permiso de `spaces`. Después adquiere el mutex,
   inserta una pieza identificada por productor y número de pieza, y libera el
   mutex. Finalmente incrementa `elements` para avisar que hay una pieza nueva.
5. Cada consumidor espera un permiso de `elements`. Después adquiere el mutex,
   retira una pieza de la cola y libera el mutex. Finalmente incrementa
   `spaces` para avisar que quedó un lugar disponible y registra el ensamblaje.
6. Se esperó la finalización de todos los hilos y se verificó que el máximo
   almacenado no excediera cinco y que la cola terminara vacía.

El orden de sincronización es:

```text
Productor: esperar espacios → adquirir mutex → insertar → liberar mutex →
           señalar elementos

Consumidor: esperar elementos → adquirir mutex → retirar → liberar mutex →
            señalar espacios → ensamblar
```

El mutex se libera dentro de un bloque `finally`, de modo que la sección crítica
quede protegida aun si se produce un error al operar sobre la cola.

## Resultados obtenidos

La ejecución correcta (valores iniciales `spaces = 5` y `elements = 0`) termina
con los siguientes resultados:

| Indicador | Resultado esperado y verificado |
| --- | ---: |
| Capacidad del almacén | 5 piezas |
| Productores / consumidores | 2 / 2 |
| Piezas producidas | 10 |
| Piezas consumidas | 10 |
| Máximo de piezas almacenadas | No supera 5 |
| Piezas restantes al finalizar | 0 |

Estos resultados cumplen el criterio de la guía: todos los productos son
consumidos, el almacén nunca supera su capacidad y queda sin inconsistencias.
El tiempo concurrente se mide en cada ejecución y puede variar según el equipo
y la planificación de los hilos.

## Análisis de la pregunta de la guía

**¿Qué sucede si `spaces` se inicializa en 0? ¿Qué sucede si `elements` se
inicializa en 5?**

- **`spaces = 0`:** ningún productor obtiene permiso para insertar, aunque el
  almacén esté vacío. Si los consumidores también esperan piezas, ambos grupos
  quedan bloqueados y el trabajo no puede avanzar. En esta implementación, la
  inicialización incorrecta se detecta antes de crear los hilos para evitar
  dejar bloqueada la aplicación.
- **`elements = 5`:** los consumidores reciben permisos que afirman que ya hay
  piezas, aunque la cola comienza vacía. Intentar retirar esas piezas produciría
  una extracción inválida y los contadores dejarían de representar el estado
  real de la cola. La implementación también detecta esta inicialización y
  muestra un diagnóstico sin iniciar los hilos.

Por eso, para representar correctamente un almacén inicialmente vacío, los
valores deben ser `spaces = 5` y `elements = 0`.

## Conclusión

Los semáforos coordinan la disponibilidad de lugares y piezas, mientras que el
mutex protege la cola compartida durante cada inserción y extracción. La
combinación de ambos mecanismos permite que productores y consumidores trabajen
concurrentemente sin sobrepasar la capacidad ni consumir elementos inexistentes.

## Ubicación de la implementación

- Servicio de simulación: `backend/src/main/java/ec/edu/unl/sd/practica3/productorconsumidor/ProducerConsumerService.java`.
- Interfaz y bitácora: `frontend/src/App.jsx`.
- Endpoint: `GET /api/ejercicios/3/productor-consumidor`.
- La interfaz permite probar otros valores iniciales de los semáforos y
  observar el diagnóstico de inicialización inválida sin bloquear la
  aplicación.
