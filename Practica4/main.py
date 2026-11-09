"""Servidor central: IPC (productor -> procesador) y cliente del gateway."""

import multiprocessing
import queue
import os
import socket
import json
import time
from pathlib import Path
import sys

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "cliente_system"))
from ipc_system.controls.productor import productor_main
from ipc_system.controls.procesador import procesador_main


def enviar_gateway(pedido: dict) -> None:
    host = os.getenv("GATEWAY_HOST", "127.0.0.1")
    puerto = int(os.getenv("GATEWAY_PORT", "6000"))
    with socket.create_connection((host, puerto), timeout=5) as conexion:
        conexion.sendall((json.dumps(pedido) + "\n").encode())


def main() -> None:
    entrada = multiprocessing.Queue()
    salida = multiprocessing.Queue()
    productor = multiprocessing.Process(target=productor_main, args=(entrada,))
    procesador = multiprocessing.Process(target=procesador_main, args=(entrada, None, salida))
    productor.start()
    procesador.start()
    print("[MAIN] IPC activo; enviando pedidos al gateway", flush=True)
    try:
        while True:
            try:
                pedido = salida.get(timeout=2)
            except queue.Empty:
                continue
            try:
                enviar_gateway(pedido)
                print(f"[MAIN] Pedido {pedido['id']} enviado", flush=True)
            except OSError as error:
                print(f"[MAIN] Gateway no disponible: {error}", flush=True)
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        productor.terminate()
        procesador.terminate()
        productor.join()
        procesador.join()


if __name__ == "__main__":
    main()
