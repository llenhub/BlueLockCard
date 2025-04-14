import discord
from discord import app_commands
from discord.ext import commands
from types import SimpleNamespace
from responses import get_user_cards
from imgen import generate_card_image

class ShowCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="show",
        description="Show a specific card from your collection by its list index (with image)."
    )
    async def show(self, interaction: discord.Interaction, index: int):
        user_cards = get_user_cards(interaction.user.id)
        if not user_cards or index < 1 or index > len(user_cards):
            await interaction.response.send_message("You have no card!", ephemeral=True)
            return

        card = user_cards[index - 1]
        # Convert the dict to an object with proper attributes expected by generate_card_image.
        card_obj = SimpleNamespace(
            name=card["name"],
            card_set=card["set"],  # Adjust this if needed.
            rarity=card["rarity"],
            serial_number=card["serial_number"],
            stats=card["stats"]
        )
        image_stream = generate_card_image(card_obj)

        stats_str = "\n".join([f"- {stat}: {value}" for stat, value in card.get("stats", {}).items()])
        embed = discord.Embed(
            title=f"{card['name']}",
            description=(
                f"**Rarity:** {card['rarity']}\n"
                f"**Serial Number:** {card['serial_number']}\n"
                f"**Stats:**\n{stats_str}"
            ),
            color=0xe74c3c
        )

        # Add author info
        embed.set_author(
            name=f"{card['set']}\n"
        )

        if image_stream:
            embed.set_image(url="attachment://" + image_stream.name)
            await interaction.response.send_message(embed=embed, file=discord.File(image_stream))
        else:
            await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(ShowCog(bot))
