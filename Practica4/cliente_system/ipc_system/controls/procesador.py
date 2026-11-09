def procesador_main(queue, memoria, salida=None):
    while True:
        data = queue.get()

        data["estado"] = "urgente" if data.get("prioridad") == "urgente" else "pendiente"

        if memoria is not None:
            memoria["data"] = data
        if salida is not None:
            salida.put(data)

        print("[IPC-Procesador]", data) 
