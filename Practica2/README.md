<div align="center">

# 🔁 Práctica 2 — Comunicación por archivos

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![IPC](https://img.shields.io/badge/Comunicaci%C3%B3n-Archivos-0891B2?style=for-the-badge)

Cliente y servidor intercambian un número decimal mediante archivos compartidos.
El servidor lo convierte a binario y publica la respuesta.

</div>

## 🧭 Índice

- [Requisitos](#-requisitos)
- [Ejecución](#-ejecución)
- [Prueba rápida](#-prueba-rápida)
- [Estructura](#-estructura)

## 📦 Requisitos

- Python 3.10 o superior.
- Dos terminales en el mismo equipo, o una carpeta compartida entre equipos.

No requiere instalar dependencias externas.

## ▶️ Ejecución

Desde `Practica2/`, abre dos terminales.

**Terminal 1 — servidor:**

```bash
python servidor.py
```

**Terminal 2 — cliente:**

```bash
python cliente/cliente.py
```

Escribe un entero decimal, por ejemplo `9688`. El cliente mostrará su
representación binaria. Escribe `salir` para terminar; el servidor se detiene
con `Ctrl+C`.

## 🧪 Prueba rápida

El archivo `comunicacion/entrada_servidor.txt` contiene la solicitud y
`comunicacion/salida_servidor.txt` contiene la respuesta. También se puede
probar el conversor sin iniciar procesos:

```bash
python -c "from servidor import procesar_mensaje; print(procesar_mensaje('10'))"
```

Resultado esperado: `1010`.

## 📂 Estructura

```text
Practica2/
├── servidor.py
├── cliente/cliente.py
└── comunicacion/
    ├── entrada_servidor.txt
    └── salida_servidor.txt
```

El flujo demostrado es: **cliente → archivo de entrada → servidor → archivo
de salida → cliente**.
