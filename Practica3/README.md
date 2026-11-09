<div align="center">

# 🧵 Práctica 3 — Sincronización de procesos

![Java](https://img.shields.io/badge/Java-21-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.3-6DB33F?style=for-the-badge&logo=springboot&logoColor=white)
![React](https://img.shields.io/badge/React-Vite-61DAFB?style=for-the-badge&logo=react&logoColor=111827)

</div>

Práctica 3 de Sistemas Distribuidos: sincronización de procesos con Java,
Spring Boot, React y Vite.

## 🧭 Índice

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Verificación](#verificación)
- [Ejercicios](#ejercicio-1-estacionamiento)

Actualmente los ejercicios 1 (**Estacionamiento**), 3
(**Productor-Consumidor**) y 5 (**Centro de impresión**) cuentan con
simulaciones funcionales. Los ejercicios 2 y 4 conservan su espacio para
futuras implementaciones.

## Requisitos

Instalar las siguientes herramientas antes de ejecutar el proyecto:

- Git.
- Java JDK 21.
- Maven 3.9 o superior.
- Node.js 20 LTS o superior.
- npm, incluido con Node.js.

Verificar las versiones:

```bash
java -version
mvn -version
node --version
npm --version
```

## Instalación

Desde `Practica3/`, instalar las dependencias del frontend:

```bash
cd frontend
npm ci
cd ..
```

`npm ci` utiliza el archivo `frontend/package-lock.json` para instalar las
versiones exactas y reproducir el entorno del proyecto.

## Ejecución

La aplicación requiere dos procesos: el backend y el frontend.

### Backend

En una terminal:

```bash
cd backend
mvn spring-boot:run
```

El backend se inicia en <http://localhost:8080>.

### Frontend

En otra terminal, desde la raíz del proyecto:

```bash
cd frontend
npm run dev
```

Abrir <http://localhost:5173>.

El frontend utiliza el proxy de Vite para enviar las solicitudes `/api` al
backend en el puerto 8080. Por eso ambos procesos deben estar ejecutándose.

## Verificación

Ejecutar las pruebas del backend:

```bash
cd backend
mvn test
```

Verificar que el frontend compile para producción:

```bash
cd frontend
npm run build
```

## Ejercicio 1: Estacionamiento

La simulación se ejecuta desde la interfaz o mediante el endpoint:

```text
GET http://localhost:8080/api/ejercicios/1/estacionamiento
```

Parámetros opcionales:

```text
?vehiculos=10&permisosSemaforo=4&estadiaMs=20
```

Ejemplo con `curl`:

```bash
curl "http://localhost:8080/api/ejercicios/1/estacionamiento?vehiculos=10&permisosSemaforo=4&estadiaMs=20"
```

Escenarios de referencia:

- `permisosSemaforo=4`: respeta la capacidad física de cuatro vehículos.
- `permisosSemaforo=1`: permite un vehículo a la vez.
- `permisosSemaforo=10`: permite observar la violación de la capacidad física.

## Ejercicio 3: Fábrica de ensamblaje (productor-consumidor)

La implementación está en
[`ProducerConsumerService.java`](./backend/src/main/java/ec/edu/unl/sd/practica3/productorconsumidor/ProducerConsumerService.java).
La simulación representa un almacén compartido con capacidad para cinco piezas.
Los productores esperan espacio antes de insertar y los consumidores esperan
una pieza antes de retirarla. Un mutex protege cada acceso a la cola.

### Dónde está cada parte

| Parte del procedimiento | Ubicación en el código |
| --- | --- |
| Capacidad del almacén (5), número de productores/consumidores y piezas fabricadas | Constantes `CAPACITY`, `WORKERS` y `PIECES_PER_WORKER`, líneas 19–21 de `ProducerConsumerService.java` |
| Cola compartida | `Queue<String> warehouse = new ArrayDeque<>(CAPACITY)`, línea 33. La cola mantiene las piezas; los semáforos impiden que se inserten más de cinco. |
| Semáforo `espacios` iniciado en 5 | `new Semaphore(initialSpaces, true)`, línea 34. Con la configuración normal, `initialSpaces` debe ser 5. |
| Semáforo `elementos` iniciado en 0 | `new Semaphore(initialElements, true)`, línea 35. Con la configuración normal, `initialElements` debe ser 0. |
| Mutex iniciado disponible | `new Semaphore(1, true)`, línea 36. Solo un hilo a la vez modifica la cola. |
| Validación de valores iniciales | Líneas 23–31. Si los valores no son `espacios=5` y `elementos=0`, se informa el problema sin iniciar hilos que puedan bloquearse o retirar de una cola vacía. |
| Productor: esperar espacio, tomar mutex, insertar, liberar mutex y señalar pieza | Bucle de productores, líneas 42–60. En particular, `spaces.acquireUninterruptibly()` espera espacio; `mutex.acquireUninterruptibly()` protege `warehouse.add(piece)`; luego `mutex.release()` libera la cola y `elements.release()` avisa que hay una pieza disponible. |
| Consumidor: esperar pieza, tomar mutex, retirar, liberar mutex y señalar espacio | Bucle de consumidores, líneas 62–80. `elements.acquireUninterruptibly()` espera una pieza; dentro del mutex se ejecuta `warehouse.remove()`; después `mutex.release()` y `spaces.release()` avisa que quedó un espacio disponible. |
| Espera a que terminen los hilos y comprobación final | Líneas 82–100. Se verifica que nunca se excedió la capacidad y que no quedaron piezas en el almacén. |

### Orden de sincronización

El productor sigue este orden: **esperar `espacios` → adquirir `mutex` →
insertar pieza → liberar `mutex` → incrementar `elementos`**. El consumidor hace
el inverso: **esperar `elementos` → adquirir `mutex` → retirar pieza → liberar
`mutex` → incrementar `espacios`**. El `try/finally` garantiza que el mutex se
libere incluso si ocurre un error durante la operación de la cola.

La interfaz de este ejercicio se encuentra en
[`App.jsx`](./frontend/src/App.jsx), donde se configuran los valores iniciales
y se presenta la bitácora. La llamada al backend está en `runProducerConsumer()`;
el endpoint es `GET /api/ejercicios/3/productor-consumidor`. Para probar la
configuración correcta, usa `espacios=5` y `elementos=0`.

## Ejercicio 5: Centro de impresión

La simulación ordena las etapas de diseño (D), revisión (R) e impresión (I)
mediante semáforos. Puede ejecutarse desde la interfaz o usando:

```text
GET http://localhost:8080/api/ejercicios/5/impresion
```

Parámetros opcionales:

```text
?documentos=3&omitir=NINGUNO&timeoutMs=250&trabajoMs=20
```

`omitir` acepta `NINGUNO`, `REVISION`, `IMPRESION` o `DISENO`. Para probar el
relevo completo usa `NINGUNO`; los otros valores omiten una señal entre etapas
y permiten observar el bloqueo controlado por timeout. La respuesta incluye
el orden observado, las etapas ejecutadas, los hilos bloqueados y la bitácora.

Ejemplo para omitir la señal de revisión:

```bash
curl "http://localhost:8080/api/ejercicios/5/impresion?documentos=3&omitir=REVISION&timeoutMs=250&trabajoMs=20"
```

## Ejercicio 2: Cajero automático compartido

La simulación recibe sus datos desde el formulario del frontend o mediante el
endpoint:

```text
GET http://localhost:8080/api/ejercicios/2/cajero
```

Parámetros opcionales:

```text
?saldoInicial=1000&retiroProceso1=300&retiroProceso2=250&depositoProceso3=200&usarMutex=true&repeticiones=50
```

Con `usarMutex=true`, el saldo esperado se conserva en todas las ejecuciones.
Con `usarMutex=false`, la bitácora y el resumen permiten observar la condición
de carrera producida al consultar y actualizar el saldo simultáneamente.

## Estructura principal

```text
backend/    API Spring Boot y servicios de sincronización
frontend/   Interfaz React/Vite
ESTRUCTURA.md
GUIA_EJERCICIOS.md
README.md
```

Consulta [ESTRUCTURA.md](./ESTRUCTURA.md) para conocer los paquetes,
endpoints y responsabilidades del proyecto. La guía de implementación se
encuentra en [GUIA_EJERCICIOS.md](./GUIA_EJERCICIOS.md).

## Archivos que no se suben al repositorio

El [`.gitignore`](./.gitignore) excluye dependencias instaladas, compilaciones,
logs, configuraciones locales y archivos del IDE. El archivo
`frontend/package-lock.json` sí debe conservarse porque permite instalar
dependencias con versiones reproducibles.
