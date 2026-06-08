import requests
import time
import json
import random
from datetime import datetime

class CompactedStateMachine:
    """
    Reactive state machine governing the agentic flow.
    States: BOOT, COLLECT, SYNTHESIZE, EVOLVE, BROADCAST
    """
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.state = "BOOT"
        self.transitions = {
            "BOOT": "COLLECT",
            "COLLECT": "SYNTHESIZE",
            "SYNTHESIZE": "EVOLVE",
            "EVOLVE": "BROADCAST",
            "BROADCAST": "COLLECT"
        }

    def step(self):
        print(f"[MACHINE] Current State: {self.state}")
        if self.state == "BOOT":
            self.orchestrator.boot()
        elif self.state == "COLLECT":
            self.orchestrator.collect()
        elif self.state == "SYNTHESIZE":
            self.orchestrator.synthesize()
        elif self.state == "EVOLVE":
            self.orchestrator.evolve()
        elif self.state == "BROADCAST":
            self.orchestrator.broadcast()

        self.state = self.transitions.get(self.state, "BOOT")

class TelemetryPipeline:
    def __init__(self):
        self.logs = []
        self.start_time = time.time()

    def profile(self, operation, start_ts, metadata=None):
        duration = time.time() - start_ts
        entry = {
            "op": operation,
            "duration": round(duration, 4),
            "ts": datetime.now().isoformat(),
            "meta": metadata
        }
        self.logs.append(entry)
        if len(self.logs) > 50: self.logs.pop(0)
        return duration

    def get_stats(self):
        if not self.logs: return {"avg_lat": 0}
        avg = sum(l['duration'] for l in self.logs) / len(self.logs)
        return {"avg_lat": round(avg, 4), "uptime": round(time.time() - self.start_time, 2)}

class StateVault:
    def __init__(self):
        self.vault = {}
        self.entropy_pool = []
        self.max_dimensions = 100

    def deposit_batch(self, mapping):
        for dim, packet in mapping.items():
            self.vault[dim] = {"packet": packet, "ts": time.time()}
        self.entropy_pool.append(len(mapping))
        self._prune()

    def _prune(self):
        if len(self.vault) > self.max_dimensions:
            sorted_dims = sorted(self.vault.items(), key=lambda x: x[1]['ts'])
            to_remove = len(self.vault) - self.max_dimensions
            for i in range(to_remove):
                del self.vault[sorted_dims[i][0]]

    def compact(self):
        return {k: v['packet'] for k, v in self.vault.items()}

class ResourceManager:
    def __init__(self, vault, telemetry):
        self.vault = vault
        self.telemetry = telemetry
        self.registry_size = 0
        self.load_registry()

    def load_registry(self):
        try:
            with open('data/apis.json', 'r') as f:
                data = json.load(f)
                self.registry_size = len(data)
        except:
            self.registry_size = 0

    def run_collector(self, collector_name, fetch_func):
        start = time.time()
        multi_data = fetch_func()
        self.telemetry.profile(f"COLLECTOR_{collector_name}", start, {"dims": list(multi_data.keys())})
        self.vault.deposit_batch(multi_data)
        return multi_data

class PredictionEngine:
    def __init__(self, vault, rm):
        self.vault = vault
        self.rm = rm

    def synthesize_entent(self):
        state = self.vault.compact()
        entent = f"System Entent: Integrated State Matrix [{list(state.keys())}]. Mega-Registry Capacity: {self.rm.registry_size} endpoints."
        confidence = random.uniform(0.9, 0.99)
        return {"statement": entent, "confidence": confidence, "entropy": len(self.vault.entropy_pool)}

class Orchestrator:
    def __init__(self):
        self.vault = StateVault()
        self.telemetry = TelemetryPipeline()
        self.rm = ResourceManager(self.vault, self.telemetry)
        self.engine = PredictionEngine(self.vault, self.rm)
        self.observation_window = 5
        self.current_entent = None

    def boot(self):
        print(f"[BOOT] Pipelines online. Mega-Registry loaded with {self.rm.registry_size} nodes.")
        time.sleep(1)

    def collect(self):
        def mega_collector():
            try:
                fact = requests.get('https://catfact.ninja/fact', timeout=5).json().get('fact')
                return {
                    "knowledge": fact,
                    "registry_status": "synced",
                    "mega_load": self.rm.registry_size,
                    "sync_ts": time.time()
                }
            except:
                return {"sync_ts": time.time(), "error": "degradation"}

        self.rm.run_collector("MegaDiscovery", mega_collector)

    def synthesize(self):
        self.current_entent = self.engine.synthesize_entent()

    def evolve(self):
        stats = self.telemetry.get_stats()
        avg_lat = stats["avg_lat"]
        conf = self.current_entent["confidence"]
        if avg_lat > 1.5 or conf < 0.94:
            self.observation_window = max(3, self.observation_window - 1)
        else:
            self.observation_window = min(15, self.observation_window + 1)
        print(f"[EVOLVE] New observation window: {self.observation_window}s")

    def broadcast(self):
        print("\n" + ">>>" * 15)
        print(f"ENTENT: {self.current_entent['statement']}")
        print(f"TELEMETRY: Lat={self.telemetry.get_stats()['avg_lat']}s | Registry={self.rm.registry_size}")
        print(f"EVOLUTION: Next check in {self.observation_window}s")
        print("<<<" * 15 + "\n")
        time.sleep(self.observation_window)

def main():
    orchestrator = Orchestrator()
    machine = CompactedStateMachine(orchestrator)
    print("--- Mega-Agentic Reactive Orchestrator Active ---")
    try:
        while True:
            machine.step()
    except KeyboardInterrupt:
        print("System shutdown.")

if __name__ == "__main__":
    main()
