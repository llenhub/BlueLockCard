import random

# Mapping from character names to unique character codes.
CHAR_CODES = {
    "Isagi Yoichi": "ISYO",
    "Kira Ryosuke": "KIRY",
    "Bachira Meguru": "BAME",
    "Nagi Seishiro": "NAGI",
    "Itoshi Rin": "ITRI",
    "Mikage Reo": "MIRE",
    # Add more characters as needed.
}

# Mapping from rarity names to two-letter codes.
RARITY_CODES = {
    "Common": "CM",
    "Rare": "RA",
    "Epic": "EP",
    "Legendary": "UR"
}

# Mapping from set (variant) names to their unique codes.
# Note: Make sure the keys in this dictionary are unique.
SET_CODES = {
    "Ichinan High": "ICHI",
    "Ichinan High 2": "ICHI2",
    "1st Selection": "1SLC",
    "2nd Selection": "2SLC",
    "Neo Egoist League": "NEL"
}

# Hard‑coded list of card templates.
# Each template includes character name, human‑readable set, rarity, base stats, and drop_weight.
CARD_TEMPLATES = [
    {
        "name": "Isagi Yoichi",
        "set": "Ichinan High",
        "rarity": "Common",
        "base_stats": {
            "Offense": 40,
            "Speed": 40,
            "Defense": 40,
            "Pass": 40,
            "Dribble": 40,
            "Shoot": 40
        },
        "drop_weight": 70  # Higher weight means more common.
    },
    {
        "name": "Isagi Yoichi",
        "set": "Ichinan High 2",
        "rarity": "Common",
        "base_stats": {
            "Offense": 40,
            "Speed": 40,
            "Defense": 40,
            "Pass": 50,
            "Dribble": 40,
            "Shoot": 40
        },
        "drop_weight": 20  # Lower weight means rarer.
    }
    # Add more card templates as desired.
]

def get_all_cards() -> list:
    """Return the complete list of card templates."""
    return CARD_TEMPLATES

def get_random_card() -> dict:
    """Return a random card template from the database using weighted selection."""
    weights = [template.get("drop_weight", 1) for template in CARD_TEMPLATES]
    return random.choices(CARD_TEMPLATES, weights=weights, k=1)[0]

def get_char_code(name: str) -> str:
    """Return the unique character code for the given character name."""
    return CHAR_CODES.get(name, "UNKN")

def get_rarity_code(rarity: str) -> str:
    """Return the two-letter rarity code for the given rarity."""
    return RARITY_CODES.get(rarity, "UN")

def get_set_code(card_set: str) -> str:
    """Return the unique set code for the given human‑readable set name."""
    return SET_CODES.get(card_set, "UN")
