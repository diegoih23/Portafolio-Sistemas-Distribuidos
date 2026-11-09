<div align="center">

# 🧠 Práctica 4 — IPC, sockets TCP y asignación inteligente

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TCP](https://img.shields.io/badge/Red-TCP-0891B2?style=for-the-badge)
![Ollama](https://img.shields.io/badge/IA-Ollama-111827?style=for-the-badge)

</div>

La práctica implementa el flujo:

```text
productor (proceso) → Queue IPC → procesador (proceso) → main → gateway TCP
                                                               ↓
                                             worker TCP 7001 / worker TCP 7002
```

El gateway consulta a Ollama para seleccionar un worker usando distancia y
carga. Si Ollama no está disponible, utiliza una regla fija que elige el nodo
con menor costo. Esto permite ejecutar y probar la práctica aun sin instalar
Ollama.

## 🧭 Índice

- [Ejecución local](#-ejecución-local)
- [Configuración remota](#-configuración-remota)
- [Componentes](#-qué-se-implementó)
- [Preguntas de control](#-preguntas-de-control)

## Ejecución local

Desde `Practica4/`, en cuatro terminales:

```bash
python worker.py 7001
python worker.py 7002
python gateway-system/gateway.py
USE_OLLAMA=0 python main.py
```

Para usar Ollama, levántalo y cambia la última orden por:

```bash
OLLAMA_MODEL=codegeex4 python main.py
```

La dependencia externa es `requests` (`python -m pip install requests`). Los
workers pueden estar en otras computadoras. En el gateway remoto se configura:

```bash
WORKERS=192.168.1.20:7001,192.168.1.21:7002 python gateway-system/gateway.py
```

## 🌐 Configuración remota

El servidor central puede apuntar a otro gateway con `GATEWAY_HOST` y
`GATEWAY_PORT`.

## Qué se implementó

- `productor.py`: genera pedidos con cliente, destino, prioridad y distancias.
- `procesador.py`: transforma los pedidos dentro de la cola IPC.
- `agente_ia.py`: integra la API HTTP de Ollama y ofrece fallback determinista.
- `gateway.py`: recibe pedidos y los distribuye por TCP.
- `worker.py`: recibe y simula la ejecución del pedido.
- `main.py`: coordina los procesos IPC y envía los pedidos al gateway.

## Preguntas de control

1. IPC usa mecanismos del mismo sistema operativo, como `multiprocessing.Queue`;
   TCP intercambia bytes entre hosts mediante una conexión de red.
2. No comparten memoria: el pedido se serializa como JSON y viaja por TCP.
3. Deben viajar el identificador, prioridad, distancia y estado/carga de los
   nodos. Sin carga, la decisión puede saturar un worker.
4. Si un worker se desconecta, el gateway registra el error; en un sistema
   productivo se debe reintentar o devolver el pedido a una cola durable.
5. IA aporta valor cuando hay múltiples variables y patrones cambiantes;
   reglas fijas son preferibles cuando se requiere una decisión rápida,
   explicable y completamente determinista.
