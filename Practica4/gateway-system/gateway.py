import socket
import json
import threading
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from agente_ia import decidir

HOST = "0.0.0.0"
PORT = 6000

def cargar_servidores():
    valor = os.getenv("WORKERS", "127.0.0.1:7001,127.0.0.1:7002")
    return [(host, int(puerto)) for host, puerto in (item.split(":", 1) for item in valor.split(","))]


servidores = cargar_servidores()
indice = 0
lock = threading.Lock()

# 🔹 IA con Ollama
def enviar(destino, data):
    with socket.create_connection(destino, timeout=5) as s:
        s.sendall((json.dumps(data) + "\n").encode())
        respuesta = s.recv(4096)
    return json.loads(respuesta.decode()) if respuesta else {"ok": True}


def manejar_cliente(conn, addr):
    global indice

    data = conn.recv(1024)

    if data:
        decoded = json.loads(data.decode())

        estado = [
            {"worker": i, "host": host, "puerto": int(puerto), "carga": 0, "distancia": decoded.get("distancias", {}).get(str(i), 0)}
            for i, (host, puerto) in enumerate(servidores)
        ]
        idx, origen = decidir(decoded, estado)

        destino = servidores[idx]

        print("[GATEWAY] Cliente", addr, "→", destino)

        try:
            respuesta = enviar(destino, decoded)
            print(f"[GATEWAY] Enviado a {destino} mediante {origen}: {respuesta}")
        except OSError as error:
            print(f"[ERROR GATEWAY] worker no disponible: {error}")

    conn.close()


def gateway():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    print("[GATEWAY] activo...")

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    gateway()
