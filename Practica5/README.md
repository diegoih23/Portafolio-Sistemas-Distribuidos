<div align="center">

# 📡 Práctica 5 — MQTT, SQLite y RabbitMQ

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-Mosquitto-660066?style=for-the-badge)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)

</div>

Simulación de una flota de tres vehículos: los sensores publican por MQTT,
un suscriptor almacena la telemetría en SQLite y un puente reenvía los datos
relevantes a RabbitMQ.

## 🧭 Índice

- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Ejecución](#-ejecución)
- [Verificación](#-verificación)
- [Estructura](#-estructura)

## 📦 Requisitos

- Docker y Docker Compose.
- Python 3.10 o superior.

## ⚙️ Instalación

Desde `Practica5/`:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Ejecución

Abre cuatro terminales. En todas, activa el entorno virtual.

**Terminal 1 — brokers:**

```bash
docker compose up -d
```

**Terminal 2 — suscriptor y SQLite:**

```bash
python suscriptor.py
```

**Terminal 3 — puente MQTT → RabbitMQ:**

```bash
python mqtt_rabbitmq_bridge.py
```

**Terminal 4 — simulador:**

```bash
python simulador_sensores.py
```

El simulador publica continuamente GPS, temperatura y combustible para los
vehículos `VH-001`, `VH-002` y `VH-003`.

## 🔎 Verificación

- Panel RabbitMQ: <http://localhost:15672> (`guest` / `guest`).
- Topics MQTT:
  ```bash
  docker exec -it mosquitto_broker mosquitto_sub -t 'flota/#' -v
  ```
- Datos SQLite:
  ```bash
  python -c "import sqlite3; c=sqlite3.connect('telemetria.db'); print(list(c.execute('SELECT * FROM temp_data ORDER BY id DESC LIMIT 5')))"
  ```

Las alertas se generan cuando la temperatura supera `4 °C` o el combustible
baja de `20 %`.

## 🛑 Detener

Detén los tres scripts con `Ctrl+C` y luego ejecuta:

```bash
docker compose down
```

## 📂 Estructura

| Archivo | Función |
|---|---|
| `docker-compose.yml` | Mosquitto y RabbitMQ |
| `simulador_sensores.py` | Publica telemetría MQTT |
| `suscriptor.py` | Guarda SQLite y muestra alertas |
| `mqtt_rabbitmq_bridge.py` | Reenvía mensajes a RabbitMQ |
