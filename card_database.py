import random

# Full name -> code mapping.
# (Note: Avoid duplicates. If you need multiple variants for a given full name,
#  store them separately in your templates.)
CHAR_CODES = {
    "Isagi Yoichi": "ISYO",    
    "Isagi Yoichi": "ISYO2",
    "Isagi Yoichi": "ISYO3",
    "Kira Ryosuke": "KIRY",
    "Kira Ryosuke": "KIRY2",
    "Kocchi Ponkotsu": "KOPO",
    "Kazeyama Matsu": "KAMA",
    "Bachira Meguru": "BAME",
    "Nagi Seishiro": "NAGI",
    "Itoshi Rin": "ITRI",
    "Mikage Reo": "MIRE"
}

# Rarity mapping remains the same.
RARITY_CODES = {
    "Common": "CM",
    "Uncommon": "UC",
    "Rare": "RA",
    "Epic": "EP",
    "Ultra Rare": "UR",
    "Legendary": "LG",
    "Mythic": "MY"
}

# Set mapping from full set names to codes.
SET_CODES = {
    "Ichinan High": "ICHI",
    "Matsukaze Kokuo High": "MTKZ",
    "1st Selection": "1SLC",
    "2nd Selection": "2SLC",
    "Neo Egoist League": "NEL",
    "Samurai Blue": "JFA"
}

# Updated card templates using codes directly.
CARD_TEMPLATES = [
    {
        "name": "Isagi Yoichi",
        "variant": "ISYO",
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
        "drop_weight": 1000
    },
    {
        "name": "Isagi Yoichi",
        "variant": "ISYO2",
        "set": "Ichinan High",
        "rarity": "Common",
        "base_stats": {
            "Offense": 40,
            "Speed": 40,
            "Defense": 45,
            "Pass": 50, 
            "Dribble": 40,
            "Shoot": 40
        },
        "drop_weight": 500
    },
    {
        "name": "Isagi Yoichi",
        "variant": "ISYO3",
        "set": "Ichinan High",
        "rarity": "Common",
        "base_stats": {
            "Offense": 40,
            "Speed": 45,
            "Defense": 40,
            "Pass": 40, 
            "Dribble": 50,
            "Shoot": 40
        },
        "drop_weight": 500
    },
    {
        "name": "Kira Ryosuke",
        "variant": "KIRY",
        "set": "Matsukaze Kokuo High",
        "rarity": "Uncommon",
        "base_stats": {
            "Offense": 45,
            "Speed": 60,
            "Defense": 44,
            "Pass": 45, 
            "Dribble": 45,
            "Shoot": 60
        },
        "drop_weight": 100
    },
    {
        "name": "Kira Ryosuke",
        "variant": "KIRY2",
        "set": "Matsukaze Kokuo High",
        "rarity": "Uncommon",
        "base_stats": {
            "Offense": 55,
            "Speed": 60,
            "Defense": 40,
            "Pass": 45, 
            "Dribble": 40,
            "Shoot": 70
        },
        "drop_weight": 100
    },
    {
        "name": "Kocchi Ponkotsu",
        "variant": "KOPO",
        "set": "Matsukaze Kokuo High",
        "rarity": "Common",
        "base_stats": {
            "Offense": 35,
            "Speed": 35,
            "Defense": 35,
            "Pass": 35, 
            "Dribble": 35,
            "Shoot": 35
        },
        "drop_weight": 1000
    },
    {
        "name": "Kazeyama Matsu",
        "variant": "KAMA",
        "set": "Matsukaze Kokuo High",
        "rarity": "Common",
        "base_stats": {
            "Offense": 35,
            "Speed": 35,
            "Defense": 35,
            "Pass": 35, 
            "Dribble": 35,
            "Shoot": 35
        },
        "drop_weight": 1000
    },
    {
        "name": "Isagi Yoichi",
        "variant": "ISYO",
        "set": "Samurai Blue",
        "rarity": "Legendary",
        "base_stats": {
            "Offense": 97,
            "Speed": 97,
            "Defense": 85,
            "Pass": 83,
            "Dribble": 80,
            "Shoot": 95
        },
        "drop_weight": 1
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
    """
    Return the unique character code.
    
    If the provided name already appears to be a code (e.g. it's uppercase or in our list of valid codes),
    then return it unchanged. Otherwise, look it up by full name.
    """
    # Define a set of valid character codes based on your mapping
    valid_codes = set(CHAR_CODES.values())
    if name in valid_codes or name.isupper():
        return name
    return CHAR_CODES.get(name, "UNKN")

def get_rarity_code(rarity: str) -> str:
    """
    Return the two-letter rarity code.
    
    If rarity is already one of the codes, return it; otherwise look it up.
    """
    valid_rarity_codes = set(RARITY_CODES.values())
    if rarity in valid_rarity_codes:
        return rarity
    return RARITY_CODES.get(rarity, "UN")

def get_set_code(card_set: str) -> str:
    """
    Return the unique set code.
    
    If card_set is already a code, return it; otherwise perform a lookup.
    """
    valid_set_codes = set(SET_CODES.values())
    if card_set in valid_set_codes or card_set.isupper():
        return card_set
    return SET_CODES.get(card_set, "UN")
