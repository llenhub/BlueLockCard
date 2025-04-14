import os
import io  # for BytesIO
from PIL import Image, ImageDraw, ImageFont

# Directories for assets.
ASSET_DIR = "assets"
BACKGROUND_DIR = os.path.join(ASSET_DIR, "backgrounds")
CHARACTER_DIR = os.path.join(ASSET_DIR, "characters")

def get_background_path(rarity: str) -> str:
    rarity = rarity.lower()
    mapping = {
        "common": "common.png",
        "uncommon": "uncommon.png",
        "rare": "rare.png",
        "epic": "epic.png",
        "ultra rare": "ultrarare.png",
        "legendary": "legendary.png",
        "mythic": "mythic.png"
    }
    file_name = mapping.get(rarity, "common.png")
    return os.path.join(BACKGROUND_DIR, file_name)

from card_database import get_set_code, get_char_code

def get_character_image_path(card_set: str, name: str, variant: str = None) -> str:
    set_code = get_set_code(card_set)
    # If a variant is provided in the card, use it.
    if variant:
        char_code = variant
    else:
        char_code = get_char_code(name)
    file_name = f"{char_code}.png"
    return os.path.join(CHARACTER_DIR, set_code, file_name)

def generate_card_image(card) -> io.BytesIO:
    """
    Composes an image for the given card and returns an in-memory BytesIO object.
    The card object is expected to have these attributes:
      - card.rarity
      - card.card_set (human‑readable set name)
      - card.name
      - card.serial_number
      - card.stats (a dictionary)
    """
    # Load the background image based on rarity.
    bg_path = get_background_path(card.rarity)
    try:
        background = Image.open(bg_path).convert("RGBA")
    except Exception as e:
        print(f"Error loading background image: {e}")
        return None

    bg_width, bg_height = background.size

    # Load the character image.
    variant = getattr(card, "variant", None)  # works if card is an object/dict that includes variant
    char_path = get_character_image_path(card.card_set, card.name, variant)
    try:
        character = Image.open(char_path).convert("RGBA")
    except FileNotFoundError:
        print(f"Character image not found: {char_path}")
        return None

    # Resize the character image to match the background size.
    character = character.resize((bg_width, bg_height), Image.LANCZOS)

    # Compose the card image by pasting the character onto the background.
    background.paste(character, (0, 0), character)

    # Prepare to draw text.
    draw = ImageDraw.Draw(background)
    stroke_width = 4
    stroke_fill = (0, 0, 0)  # Black outline

    # Font for stat text (larger size).
    try:
        stats_font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        stats_font = ImageFont.load_default()

    # Font for bold text for the stat value.
    try:
        bold_font = ImageFont.truetype("arialbd.ttf", 60)  # Arial Bold; adjust path if needed.
    except IOError:
        bold_font = ImageFont.load_default()

    # Font for serial number (smaller size).
    try:
        serial_font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        serial_font = ImageFont.load_default()

    # Abbreviate stats to 3 letters.
    stat_abbreviations = {
        "Offense": "OFF",
        "Speed": "SPD",
        "Defense": "DEF",
        "Pass": "PAS",
        "Dribble": "DRI",
        "Shoot": "SHO"
    }

    # Define stat positions.
    positions = {
        "Offense": (200, 400),
        "Speed": (200, 480),
        "Defense": (200, 560),
        "Pass": (200, 640),
        "Dribble": (200, 720),
        "Shoot": (200, 800)
    }

    # Draw each stat using its designated position with a text stroke.
    # Draw the stat value in bold and the abbreviation in the regular font.
    for stat, value in card.stats.items():
        pos = positions.get(stat, (20, 20))  # Default position if stat not found in our mapping.
        abbr = stat_abbreviations.get(stat, stat[:3].upper())
        value_text = f"{value}"
        abbr_text = f" {abbr}"  # add a leading space between value and abbreviation

        # Draw the bolded stat value.
        draw.text(
            pos,
            value_text,
            font=bold_font,
            fill=(255, 255, 255),
            stroke_width=stroke_width,
            stroke_fill=stroke_fill
        )

        # Use textbbox to determine the width of the drawn bold text.
        bbox = draw.textbbox(pos, value_text, font=bold_font, stroke_width=stroke_width)
        value_width = bbox[2] - bbox[0]

        # Calculate the position for the abbreviation.
        abbr_pos = (pos[0] + value_width, pos[1])

        # Draw the abbreviation using the regular font.
        draw.text(
            abbr_pos,
            abbr_text,
            font=stats_font,
            fill=(255, 255, 255),
            stroke_width=stroke_width,
            stroke_fill=stroke_fill
        )

    # Prepare serial number text.
    serial_text = f"{card.serial_number}"
    # Calculate text size for the serial number using textbbox.
    bbox = draw.textbbox((0, 0), serial_text, font=serial_font, stroke_width=stroke_width)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    # Center the serial number horizontally and position it near the bottom.
    serial_pos = ((bg_width - text_width) // 2, (bg_height - text_height) - 250)
    draw.text(
        serial_pos,
        serial_text,
        font=serial_font,
        fill=(255, 255, 255),
        stroke_width=stroke_width,
        stroke_fill=stroke_fill
    )

    # Save the final composed image to a BytesIO stream instead of a disk file.
    output_stream = io.BytesIO()
    background.save(output_stream, format="PNG")
    output_stream.seek(0)
    # Set a name so that Discord recognizes the file type (this will be used in the attachment URL).
    output_stream.name = f"{card.serial_number}.png"
    return output_stream

# For testing imgen.py independently.
if __name__ == "__main__":
    class Card:
        def __init__(self, name, card_set, rarity, serial_number, stats):
            self.name = name
            self.card_set = card_set
            self.rarity = rarity
            self.serial_number = serial_number
            self.stats = stats

    sample_card = Card(
        name="Isagi Yoichi",
        card_set="Neo Egoist League",
        rarity="Legendary",
        serial_number="NEOL-UR-ISYO-1",
        stats={"Offense": 105, "Speed": 92, "Defense": 85, "Pass": 88, "Dribble": 100, "Shoot": 110}
    )
    img_stream = generate_card_image(sample_card)
    if img_stream:
        print(f"Generated card image in-memory with name: {img_stream.name}")
