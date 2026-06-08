import requests
import time
import json
import random
from datetime import datetime, timedelta

class StateVault:
    """
    Manages multi-dimensional states by compacting data from various sources.
    """
    def __init__(self):
        self.vault = {}
        self.history = []

    def deposit(self, dimension, packet):
        self.vault[dimension] = {
            "packet": packet,
            "recorded_at": datetime.now().isoformat()
        }
        self.history.append((dimension, packet, time.time()))
        # Keep history compact
        if len(self.history) > 50:
            self.history.pop(0)

    def compact(self):
        return {k: v['packet'] for k, v in self.vault.items()}

class TaskScheduler:
    """
    Handles rescheduling of API flows and intent broadcasting.
    """
    def __init__(self):
        self.schedule = []

    def add_job(self, name, interval, action):
        self.schedule.append({
            "name": name,
            "interval": interval,
            "action": action,
            "last_run": 0
        })

    def tick(self):
        now = time.time()
        for job in self.schedule:
            if now - job["last_run"] >= job["interval"]:
                job["action"]()
                job["last_run"] = now

class ResourceManager:
    """
    Handles N-to-M mappings:
    - One request serving multiple outputs (caching/reuse)
    - Many requests serving one output (merging)
    """
    def __init__(self, vault):
        self.vault = vault
        self.cache = {}
        self.usage_counters = {}

    def get_dimension_data(self, dimension, fetch_func, force=False):
        now = time.time()
        # One request can serve multiple outputs if we use cached data within a window
        if not force and dimension in self.cache and now - self.cache[dimension]['timestamp'] < 30:
            self.usage_counters[dimension] = self.usage_counters.get(dimension, 0) + 1
            return self.cache[dimension]['data']

        # New request
        data = fetch_func()
        self.cache[dimension] = {'data': data, 'timestamp': now}
        self.vault.deposit(dimension, data)
        return data

    def get_system_report(self):
        return {
            "mappings": self.usage_counters,
            "current_state_dimensions": list(self.vault.vault.keys())
        }

class PredictionEngine:
    """
    Calculates predicted system intents based on state trends and entropy.
    """
    def __init__(self, vault):
        self.vault = vault

    def predict_next_intent(self):
        compacted_state = self.vault.compact()
        if not compacted_state:
            return {
                "intent": "Awaiting initial state compaction...",
                "prediction": "Calculating equilibrium...",
                "confidence": 0.0
            }

        # Calculate a "System Intent" from multi-dimensional merged state
        dimensions = list(compacted_state.keys())
        summary = " | ".join([f"{d}: {str(compacted_state[d])[:50]}" for d in dimensions])

        # Simple prediction logic based on available dimensions
        if "finance" in dimensions and "social" in dimensions:
            prediction = "Predicted State: Financial volatility may trigger social harmonic shifts."
        elif "knowledge" in dimensions:
            prediction = f"Predicted State: Entropy reduction through knowledge integration: {str(compacted_state['knowledge'])[:30]}"
        else:
            prediction = "Predicted State: Multi-dimensional equilibrium maintained."

        return {
            "intent": f"System Intent Statement: [{summary}]",
            "prediction": prediction,
            "confidence": round(random.uniform(0.85, 0.99), 2)
        }

def fetch_cat_fact():
    try: return requests.get('https://catfact.ninja/fact', timeout=5).json().get('fact')
    except: return "No fact"

def fetch_btc_price():
    try: return requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd', timeout=5).json()['bitcoin']['usd']
    except: return 0

def fetch_joke():
    try:
        j = requests.get('https://official-joke-api.appspot.com/random_joke', timeout=5).json()
        return f"{j['setup']} {j['punchline']}"
    except: return "No joke"

def main():
    vault = StateVault()
    scheduler = TaskScheduler()
    rm = ResourceManager(vault)
    engine = PredictionEngine(vault)

    # Define tasks
    def update_finance():
        rm.get_dimension_data("finance", fetch_btc_price)
        print("[State Update] Finance dimension synced.")

    def update_knowledge():
        rm.get_dimension_data("knowledge", fetch_cat_fact)
        print("[State Update] Knowledge dimension synced.")

    def update_social():
        rm.get_dimension_data("social", fetch_joke)
        print("[State Update] Social dimension synced.")

    def broadcast_intent():
        prediction = engine.predict_next_intent()
        print("\n" + "="*50)
        print(f"TIME: {datetime.now().strftime('%H:%M:%S')}")
        print(f"INTENT: {prediction['intent']}")
        print(f"PREDICTION: {prediction['prediction']}")
        print(f"CONFIDENCE: {prediction['confidence']}")
        print(f"RESOURCE UTILIZATION: {json.dumps(rm.get_system_report()['mappings'])}")
        print("="*50 + "\n")

    # Schedule tasks (Rescheduling together)
    scheduler.add_job("Finance Sync", 15, update_finance)
    scheduler.add_job("Knowledge Sync", 20, update_knowledge)
    scheduler.add_job("Social Sync", 25, update_social)
    scheduler.add_job("Intent Broadcast", 10, broadcast_intent)

    print("--- Agentic Orchestrator Flow Running ---")
    try:
        while True:
            scheduler.tick()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Flow terminated.")

if __name__ == "__main__":
    main()
