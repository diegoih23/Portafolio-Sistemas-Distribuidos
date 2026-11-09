import time
import random
import uuid

def productor_main(queue):
    while True:
        data = {
            "id": str(uuid.uuid4())[:8],
            "cliente": f"cliente-{random.randint(1, 20)}",
            "origen": random.choice(["Centro", "Norte", "Sur"]),
            "destino": random.choice(["Centro", "Norte", "Sur"]),
            "distancias": {"0": random.randint(1, 20), "1": random.randint(1, 20)},
            "prioridad": random.choice(["normal", "urgente"]),
            "tiempo_procesamiento": random.uniform(0.1, 0.5),
            "timestamp": time.time(),
        }
        print("[IPC-Productor]", data)
        queue.put(data)
        time.sleep(1) 
