import discord
from discord import app_commands
from discord.ext import commands
from responses import generate_card, add_card_to_collection
from imgen import generate_card_image

MY_USER_ID = 239033440857489410

# This ClaimView can either be moved to a shared file if reused elsewhere.
class ClaimView(discord.ui.View):
    def __init__(self, card, dropper_id, image_path):
        super().__init__(timeout=60)  # View times out after 60 seconds.
        self.card = card
        self.dropper_id = dropper_id
        self.image_path = image_path
        self.claimed = False

    @discord.ui.button(label="Claim Card", style=discord.ButtonStyle.green)
    async def claim_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.claimed:
            await interaction.response.send_message("This card has already been claimed.", ephemeral=True)
            return

        add_card_to_collection(interaction.user.id, self.card)
        self.claimed = True

        # Get the card's serial number; adjust as needed if card is an object.
        serial_number = self.card.get("serial_number") if isinstance(self.card, dict) else getattr(self.card, "serial_number", "Unknown")

        # Delete the original drop message.
        await interaction.message.delete()
        # Announce the claim.
        await interaction.channel.send(f"{interaction.user.mention} has claimed {serial_number}!")

class DropCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="drop",
        description="Drop a Blue Lock card; optionally specify a number of cards to drop (default is 1)."
    )
    async def drop(self, interaction: discord.Interaction, count: int = 1):
        if interaction.user.id != MY_USER_ID:
            await interaction.response.send_message("You are not authorized to drop a card.", ephemeral=True)
            return

        count = max(count, 1)

        for i in range(count):
            card = generate_card()
            image_stream = generate_card_image(card)

            embed = discord.Embed(
                title="Card Drop!",
                description="A new card has been dropped! Click the **Claim Card** button to add it to your collection.",
                color=0x3498db
            )
            if image_stream:
                embed.set_image(url="attachment://" + image_stream.name)

            view = ClaimView(card, interaction.user.id, image_stream)

            # Use the initial response for the first card and followup for additional drops.
            if i == 0:
                if image_stream:
                    await interaction.response.send_message(embed=embed, view=view, file=discord.File(image_stream))
                else:
                    await interaction.response.send_message(f"You dropped a card, but image generation failed.\n{card}", view=view)
            else:
                if image_stream:
                    await interaction.followup.send(embed=embed, view=view, file=discord.File(image_stream))
                else:
                    await interaction.followup.send(f"You dropped a card, but image generation failed.\n{card}", view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(DropCog(bot))
