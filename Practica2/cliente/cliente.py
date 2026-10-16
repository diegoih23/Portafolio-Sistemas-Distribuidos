"""Cliente que se comunica con el servidor únicamente mediante archivos."""

from pathlib import Path
import os
import time
import uuid


CARPETA_COMPARTIDA = Path(__file__).resolve().parent.parent / "comunicacion"
ARCHIVO_ENTRADA = CARPETA_COMPARTIDA / "entrada_servidor.txt"
ARCHIVO_SALIDA = CARPETA_COMPARTIDA / "salida_servidor.txt"
ESPERA_SEGUNDOS = 0.25
TIEMPO_LIMITE_SEGUNDOS = 30


def preparar_archivos() -> None:
    CARPETA_COMPARTIDA.mkdir(parents=True, exist_ok=True)
    ARCHIVO_ENTRADA.touch(exist_ok=True)
    ARCHIVO_SALIDA.touch(exist_ok=True)


def enviar_mensaje(mensaje: str) -> None:
    """Limpia la respuesta anterior y publica la solicitud de forma atómica."""
    ARCHIVO_SALIDA.write_text("", encoding="utf-8")
    temporal = ARCHIVO_ENTRADA.with_name(f"{ARCHIVO_ENTRADA.name}.{uuid.uuid4().hex}.tmp")
    try:
        temporal.write_text(mensaje, encoding="utf-8")
        os.replace(temporal, ARCHIVO_ENTRADA)
    finally:
        temporal.unlink(missing_ok=True)


def esperar_respuesta() -> str:
    """Espera la respuesta del servidor, sin conocer cómo procesa la solicitud."""
    limite = time.monotonic() + TIEMPO_LIMITE_SEGUNDOS
    while time.monotonic() < limite:
        respuesta = ARCHIVO_SALIDA.read_text(encoding="utf-8").strip()
        if respuesta:
            return respuesta
        time.sleep(ESPERA_SEGUNDOS)
    raise TimeoutError("No llegó respuesta. Comprueba que el servidor esté activo.")


def solicitar_mensaje(mensaje: str) -> str:
    enviar_mensaje(mensaje)
    # Pequeña latencia simulada, además de la espera de respuesta.
    time.sleep(ESPERA_SEGUNDOS)
    return esperar_respuesta()


def ejecutar_cliente() -> None:
    preparar_archivos()
    print("Cliente listo. Deja el servidor ejecutándose en otra terminal.")
    print("Escribe 'salir' para terminar.\n")
    while True:
        try:
            mensaje = input("Mensaje: ")
        except (EOFError, KeyboardInterrupt):
            print("\nCliente finalizado.")
            break
        if mensaje.strip().lower() == "salir":
            break
        if not mensaje.strip():
            print("El mensaje está vacío; no se envió.\n")
            continue
        try:
            print(f"Respuesta: {solicitar_mensaje(mensaje)}\n")
        except TimeoutError as error:
            print(f"Error: {error}\n")


if __name__ == "__main__":
    ejecutar_cliente()
