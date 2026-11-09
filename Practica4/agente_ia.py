"""Decisión de asignación de pedidos con Ollama y respaldo determinista."""

import json
import os
from typing import Any

import requests


def _regla_fija(pedido: dict[str, Any], workers: list[dict[str, Any]]) -> int:
    """Selecciona el nodo con menor costo considerando carga y distancia."""
    if not workers:
        raise ValueError("No hay workers configurados")

    def costo(worker: dict[str, Any]) -> float:
        carga = float(worker.get("carga", 0))
        distancia = float(worker.get("distancia", 0))
        return carga * 2 + distancia

    return min(range(len(workers)), key=lambda i: costo(workers[i]))


def decidir(pedido: dict[str, Any], workers: list[dict[str, Any]]) -> tuple[int, str]:
    """Devuelve (índice del worker, origen de la decisión).

    Ollama puede desactivarse con USE_OLLAMA=0. Si no está disponible o
    responde algo inválido, el sistema sigue funcionando con reglas fijas.
    """
    fallback = _regla_fija(pedido, workers)
    if os.getenv("USE_OLLAMA", "1").lower() in {"0", "false", "no"}:
        return fallback, "reglas-fijas"

    prompt = (
        "Eres un despachador de pedidos. Elige el worker más conveniente "
        "combinando distancia y carga. Responde únicamente con un JSON válido "
        'con la forma {"worker": 0}.\n'
        f"Pedido: {json.dumps(pedido, ensure_ascii=False)}\n"
        f"Workers: {json.dumps(workers, ensure_ascii=False)}"
    )
    try:
        response = requests.post(
            os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate"),
            json={
                "model": os.getenv("OLLAMA_MODEL", "codegeex4"),
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=float(os.getenv("OLLAMA_TIMEOUT", "5")),
        )
        response.raise_for_status()
        result = response.json().get("response", "")
        selected = json.loads(result).get("worker")
        selected = int(selected)
        if 0 <= selected < len(workers):
            return selected, "ollama"
    except (requests.RequestException, ValueError, TypeError, KeyError, json.JSONDecodeError):
        pass

    print("[IA] Ollama no disponible o respuesta inválida; se usan reglas fijas")
    return fallback, "reglas-fijas"
