<div align="center">

# 🚚 Práctica 6 — Microservicios con RabbitMQ

![Java](https://img.shields.io/badge/Java-21-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5-6DB33F?style=for-the-badge&logo=springboot&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-AMQP-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)

</div>

Esta práctica consume la telemetría generada por la Práctica 5. Spring Boot
recibe GPS y alertas desde RabbitMQ, registra la información y expone una API
REST con el estado de la flota.

## 🧭 Índice

- [Requisitos](#-requisitos)
- [Ejecución](#-ejecución)
- [API](#-api)
- [Verificación y apagado](#-verificación-y-apagado)
- [Estructura](#-estructura)

## 📦 Requisitos

- Docker y Docker Compose.
- Python 3.10 o superior.
- JDK 21 y Maven 3.9 o superior.
- Haber instalado las dependencias de `Practica5`.

## ▶️ Ejecución

Desde `Practica6/`, abre cuatro terminales. La Práctica 5 se utiliza como fuente
de mensajes; sus scripts están disponibles en `practica5/`.

**Terminal 1 — Mosquitto y RabbitMQ de esta práctica:**

```bash
cd practica5
docker compose down
cd ../practica6
docker compose -f docker-compose-rabbitmq.yml up -d
```

**Terminal 2 — aplicación Spring Boot:**

```bash
cd practica6/fleet-monitor
mvn spring-boot:run
```

**Terminal 3 — puente MQTT → RabbitMQ:**

```bash
python practica6/mqtt_rabbitmq_bridge.py
```

**Terminal 4 — simulador de la Práctica 5:**

```bash
python practica5/simulador_sensores.py
```

## 🔌 API

```bash
curl http://localhost:8080/api/fleet/status
curl http://localhost:8080/api/fleet/vehicle/VH-001/telemetria
```

El primer endpoint devuelve el resumen de vehículos y alertas; el segundo
devuelve la telemetría GPS almacenada para un vehículo.

## 🔎 Verificación y apagado

- RabbitMQ: <http://localhost:15672> (`admin` / `admin123`).
- La consola de Spring Boot debe mostrar mensajes GPS y alertas.
- Las colas principales se consumen y `cola.notificaciones` conserva las
  notificaciones generadas.

Para apagar el entorno:

```bash
cd practica6
docker compose -f docker-compose-rabbitmq.yml down
cd ../practica5
docker compose down
```

## 📂 Estructura

| Archivo | Función |
|---|---|
| `practica6/docker-compose-rabbitmq.yml` | RabbitMQ con usuario de la práctica |
| `practica6/fleet-monitor/` | Microservicio Spring Boot |
| `practica6/mqtt_rabbitmq_bridge.py` | Puente hacia `exchange.fleet` |
| `practica5/simulador_sensores.py` | Generador de telemetría |

Los perfiles distribuidos y la ejecución en varias computadoras se documentan
en `practica6/docker-compose-servicio.yml`.
