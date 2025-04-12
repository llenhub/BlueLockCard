import random
from random import randint
import json
from card_database import get_random_card, get_char_code, get_rarity_code, get_set_code

# The file used for persistent storage of user collections
COLLECTION_FILENAME = "collections.json"

# Global dictionary to track drop counts per card (keyed by name and rarity)
card_counts = {}

def load_collections() -> dict:
    """Load stored collections from the JSON file."""
    try:
        with open(COLLECTION_FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def generate_serial_number(name: str, rarity: str, card_set: str) -> str:
    char_code = get_char_code(name)
    rarity_code = get_rarity_code(rarity)
    set_code = get_set_code(card_set)

    # Include the card_set in the key so that the numbering is independent per set.
    key = f"{name}|{rarity}|{card_set}"
    count = card_counts.get(key, 0) + 1

    # Load persistent collections to ensure uniqueness.
    collections = load_collections()
    existing_serials = set()
    for user_cards in collections.values():
        for card in user_cards:
            existing_serials.add(card["serial_number"])

    candidate = f"{set_code}-{rarity_code}-{char_code}-{count}"
    while candidate in existing_serials:
        count += 1
        candidate = f"{set_code}-{rarity_code}-{char_code}-{count}"
    card_counts[key] = count  # Update the drop counter for this specific card type.
    return candidate

def generate_stats(base_stats: dict) -> dict:
    """
    Generates dynamic stats by applying a random offset between -10 and +10
    to each provided base stat.
    """
    stats = {}
    for stat, base_value in base_stats.items():
        offset = randint(-10, 10)
        stats[stat] = base_value + offset
    return stats

class Card:
    def __init__(self, name: str, card_set: str, rarity: str, serial_number: str, stats: dict):
        self.name = name
        self.card_set = card_set   # Human‑readable set name (e.g., "Neo Egoist League")
        self.rarity = rarity
        self.serial_number = serial_number
        self.stats = stats

    def __str__(self) -> str:
        stats_str = "\n".join(f"- {stat}: {value}" for stat, value in self.stats.items())
        return (
            f"**Name:** {self.name}\n"
            f"**Set:** {self.card_set}\n"
            f"**Rarity:** {self.rarity}\n"
            f"**Serial Number:** {self.serial_number}\n"
            f"**Stats:**\n{stats_str}"
        )

def generate_card() -> Card:
    """
    Retrieves a random card template from the database then creates a new card
    with dynamic stats (base ±10) and a serial number that increments with each drop.
    Uses weighted selection through the card_database's get_random_card.
    """
    template = get_random_card()
    name = template["name"]
    card_set = template["set"]
    rarity = template["rarity"]
    base_stats = template["base_stats"]

    serial_number = generate_serial_number(name, rarity, card_set)
    stats = generate_stats(base_stats)
    return Card(name, card_set, rarity, serial_number, stats)

# --- Persistence for User Collections ---

def load_collections() -> dict:
    """Load the stored user collections from the JSON file."""
    try:
        with open(COLLECTION_FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Global user collections (mapping of user_id to list of card dicts).
user_collections = load_collections()

def save_collections(collections: dict) -> None:
    """Save the collections dictionary to the JSON file."""
    with open(COLLECTION_FILENAME, "w") as f:
        json.dump(collections, f, indent=4)

def add_card_to_collection(user_id: int, card: Card) -> None:
    """
    Adds the card (converted to a dictionary) to the given user's collection,
    then saves the updated collection.
    """
    user_key = str(user_id)
    if user_key not in user_collections:
        user_collections[user_key] = []
    card_data = {
        "serial_number": card.serial_number,
        "name": card.name,
        "set": card.card_set,
        "rarity": card.rarity,
        "stats": card.stats
    }
    user_collections[user_key].append(card_data)
    save_collections(user_collections)

def generate_card_for_user(user_id: int) -> Card:
    """
    Generates a new card, ensures its serial number is unique (via generate_serial_number),
    adds the card to the user's collection, then returns the card.
    """
    card = generate_card()
    add_card_to_collection(user_id, card)
    return card

def get_user_cards(user_id: int) -> list:
    """Returns a list of card dictionaries that the user has collected."""
    return user_collections.get(str(user_id), [])

def get_response(user_input: str) -> str:
    """
    Example response function.
    If the user types "!drop", a new card is generated and returned as text.
    """
    lowered = user_input.lower().strip()
    if lowered.startswith("!drop"):
        card = generate_card()
        return f"You received a new Blue Lock card!\n{card}"
    return "Command not recognized."
