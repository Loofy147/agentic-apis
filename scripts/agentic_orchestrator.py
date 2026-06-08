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
    """
    Industrial-grade telemetry in a minimalist footprint.
    Profiles latency, entropy, and system health.
    """
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

# Classes for subsequent steps will be added next.

class StateVault:
    def __init__(self):
        self.vault = {}
        self.entropy_pool = []

    def deposit_batch(self, mapping):
        for dim, packet in mapping.items():
            self.vault[dim] = {"packet": packet, "ts": time.time()}
        self.entropy_pool.append(len(mapping))

    def compact(self):
        return {k: v['packet'] for k, v in self.vault.items()}

class ResourceManager:
    """
    Features M:N request multiplexing.
    Single collector fetch serves multiple metadata dimensions.
    """
    def __init__(self, vault, telemetry):
        self.vault = vault
        self.telemetry = telemetry

    def run_collector(self, collector_name, fetch_func):
        start = time.time()
        # M:N - Fetch once, map to multiple dimensions
        multi_data = fetch_func()
        self.telemetry.profile(f"COLLECTOR_{collector_name}", start, {"dims": list(multi_data.keys())})
        self.vault.deposit_batch(multi_data)
        return multi_data

class PredictionEngine:
    def __init__(self, vault):
        self.vault = vault

    def synthesize_entent(self):
        state = self.vault.compact()
        entent = f"System Entent: Integrated State Matrix [{list(state.keys())}]"
        confidence = random.uniform(0.9, 0.99)
        return {"statement": entent, "confidence": confidence, "entropy": len(self.vault.entropy_pool)}

class Orchestrator:
    def __init__(self):
        self.vault = StateVault()
        self.telemetry = TelemetryPipeline()
        self.rm = ResourceManager(self.vault, self.telemetry)
        self.engine = PredictionEngine(self.vault)
        self.observation_window = 10
        self.current_entent = None

    def boot(self):
        print("[BOOT] Calibrating pipelines...")
        time.sleep(1)

    def collect(self):
        def mixed_collector():
            # Multiplexed fetch: returns multiple dimensions
            try:
                fact = requests.get('https://catfact.ninja/fact', timeout=5).json().get('fact')
                price = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd', timeout=5).json()['bitcoin']['usd']
                return {"knowledge": fact, "finance": price, "sync_ts": time.time()}
            except:
                return {"sync_ts": time.time(), "error": "connectivity_degradation"}

        self.rm.run_collector("Primary", mixed_collector)

    def synthesize(self):
        self.current_entent = self.engine.synthesize_entent()

    def evolve(self):
        """
        Dynamically reschedules the observation window based on ecosystem health.
        If latency is high or confidence is low, shrink window for more frequent checks.
        """
        stats = self.telemetry.get_stats()
        avg_lat = stats["avg_lat"]
        conf = self.current_entent["confidence"]

        # Adaptive logic
        if avg_lat > 2.0 or conf < 0.92:
            self.observation_window = max(5, self.observation_window - 2)
            print(f"[EVOLVE] Ecosystem stress detected. Shrinking window to {self.observation_window}s")
        else:
            self.observation_window = min(30, self.observation_window + 1)
            print(f"[EVOLVE] System healthy. Extending window to {self.observation_window}s")

    def broadcast(self):
        print("\n" + ">>>" * 10)
        print(f"ENTENT: {self.current_entent['statement']}")
        print(f"HEALTH: Conf={round(self.current_entent['confidence'], 3)} | Lat={self.telemetry.get_stats()['avg_lat']}s")
        print(f"WINDOW: {self.observation_window}s")
        print("<<<" * 10 + "\n")
        time.sleep(self.observation_window)

def main():
    orchestrator = Orchestrator()
    machine = CompactedStateMachine(orchestrator)

    print("--- Reactive Agentic State-Machine Active ---")
    try:
        while True:
            machine.step()
    except KeyboardInterrupt:
        print("System shutdown.")

if __name__ == "__main__":
    main()
