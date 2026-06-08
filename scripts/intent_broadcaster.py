import requests
import time
import json
import random

def fetch_data():
    data = {}

    # 1. Cat Fact
    try:
        data['cat_fact'] = requests.get('https://catfact.ninja/fact', timeout=5).json().get('fact', 'N/A')
    except Exception as e:
        data['cat_fact'] = f"Entropy Signal: {e}"

    # 2. Bitcoin Price (Coingecko)
    try:
        price_data = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd', timeout=5).json()
        data['btc_price'] = price_data['bitcoin']['usd']
    except Exception as e:
        data['btc_price'] = f"Value Flux: {e}"

    # 3. Age Prediction (Agify)
    try:
        age_data = requests.get('https://api.agify.io/?name=agent', timeout=5).json()
        data['predicted_age'] = age_data.get('age', 'N/A')
    except Exception as e:
        data['predicted_age'] = f"Temporal Variance: {e}"

    # 4. Random Joke
    try:
        joke = requests.get('https://official-joke-api.appspot.com/random_joke', timeout=5).json()
        data['joke'] = f"{joke.get('setup')} - {joke.get('punchline')}"
    except Exception as e:
        data['joke'] = f"Semantic Glitch: {e}"

    return data

def synthesize_intent(packets):
    """
    Calculates predicted intent from multi-dimensional state.
    Merging entropy and data points into a unified statement.
    """
    fact = packets['cat_fact']
    price = packets['btc_price']
    age = packets['predicted_age']
    joke = packets['joke']

    intent_templates = [
        f"The state of the world is valued at ${price} USD. Wisdom of age {age} suggests: '{fact}'. Underlying paradox: {joke}.",
        f"Synchronicity detected. Age {age} entities observe BTC at ${price}. Reality check: '{fact}'. Harmonic resonance: {joke}.",
        f"Data compaction complete. In a state of ${price} BTC and {age} years of entropy, the core fact is: '{fact}'. Outputting intent: {joke}."
    ]

    return random.choice(intent_templates)

def main():
    print("--- Agentic API Intent Broadcaster Initialized ---")
    print("Flow running. Compacting multi-dimensional requests...")

    try:
        while True:
            packets = fetch_data()
            intent = synthesize_intent(packets)

            output = {
                "timestamp": time.time(),
                "merged_state": packets,
                "broadcasted_intent": intent
            }

            print("\n[BROADCASTING INTENT]")
            print(json.dumps(output, indent=2))

            # Broadcast to a "flow"
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nFlow terminated by operator.")

if __name__ == "__main__":
    main()
