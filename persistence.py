import json

DATA_FILE = "card_counts.json"

def load_card_counts() -> dict:
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_card_counts(counts: dict) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(counts, f, indent=4)
