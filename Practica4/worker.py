"""Worker TCP: recibe y simula el procesamiento de pedidos."""

import json
import socket
import sys
import time


def _recibir(conn: socket.socket) -> dict:
    datos = bytearray()
    while True:
        bloque = conn.recv(4096)
        if not bloque:
            break
        datos.extend(bloque)
        if b"\n" in bloque:
            break
    return json.loads(bytes(datos).split(b"\n", 1)[0].decode())


def iniciar_worker(puerto: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind(("0.0.0.0", puerto))
        servidor.listen(20)
        print(f"[WORKER {puerto}] activo", flush=True)
        while True:
            conexion, direccion = servidor.accept()
            with conexion:
                try:
                    pedido = _recibir(conexion)
                    print(f"[WORKER {puerto}] pedido {pedido['id']} desde {direccion}", flush=True)
                    time.sleep(float(pedido.get("tiempo_procesamiento", 0.2)))
                    respuesta = {"ok": True, "pedido_id": pedido.get("id"), "worker": puerto}
                except (json.JSONDecodeError, KeyError, ValueError) as error:
                    respuesta = {"ok": False, "error": str(error)}
                conexion.sendall((json.dumps(respuesta) + "\n").encode())


if __name__ == "__main__":
    iniciar_worker(int(sys.argv[1]) if len(sys.argv) > 1 else 7001)
