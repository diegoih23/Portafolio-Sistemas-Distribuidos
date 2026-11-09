import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from worker import iniciar_worker

def servidor_base(puerto):
    iniciar_worker(puerto)

if __name__ == "__main__":
    puerto = int(sys.argv[1])
    servidor_base(puerto)
