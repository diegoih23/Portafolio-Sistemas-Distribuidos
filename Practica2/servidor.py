"""Servidor de archivos: convierte números decimales enteros a binario."""

from pathlib import Path
import time


# Cliente y servidor comparten archivos dentro de esta misma práctica.
CARPETA_COMPARTIDA = Path(__file__).resolve().parent / "comunicacion"
ARCHIVO_ENTRADA = CARPETA_COMPARTIDA / "entrada_servidor.txt"
ARCHIVO_SALIDA = CARPETA_COMPARTIDA / "salida_servidor.txt"
INTERVALO_SEGUNDOS = 1


def preparar_archivos() -> None:
    """Crea la carpeta y los archivos de comunicación si aún no existen."""
    CARPETA_COMPARTIDA.mkdir(parents=True, exist_ok=True)
    ARCHIVO_ENTRADA.touch(exist_ok=True)
    ARCHIVO_SALIDA.touch(exist_ok=True)


def leer_mensaje() -> str:
    """Lee el mensaje actual; un archivo vacío representa que no hay solicitud."""
    return ARCHIVO_ENTRADA.read_text(encoding="utf-8").strip()


def procesar_mensaje(mensaje: str) -> str:
    """Convierte un entero decimal no negativo a su representación binaria."""
    try:
        numero = int(mensaje)
    except ValueError:
        return "Error: ingresa un número entero decimal."

    if numero < 0:
        return "Error: ingresa un número mayor o igual a cero."

    return bin(numero)[2:]


def guardar_respuesta(respuesta: str) -> None:
    """Publica la respuesta en el archivo de salida."""
    ARCHIVO_SALIDA.write_text(respuesta, encoding="utf-8")


def ejecutar_servidor() -> None:
    """Consulta continuamente la entrada y procesa cada mensaje no vacío nuevo."""
    preparar_archivos()
    ultima_version = None
    print(f"Servidor activo. Carpeta compartida: {CARPETA_COMPARTIDA}")
    print("Presiona Ctrl+C para detenerlo.")

    try:
        while True:
            mensaje = leer_mensaje()
            version = (ARCHIVO_ENTRADA.stat().st_ino, ARCHIVO_ENTRADA.stat().st_mtime_ns)
            if mensaje and version != ultima_version:
                respuesta = procesar_mensaje(mensaje)
                guardar_respuesta(respuesta)
                ultima_version = version
                print(f"Solicitud: {mensaje!r} -> Respuesta: {respuesta!r}")
            time.sleep(INTERVALO_SEGUNDOS)
    except KeyboardInterrupt:
        print("\nServidor detenido.")


if __name__ == "__main__":
    ejecutar_servidor()
