import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from responses import generate_card, add_card_to_collection  # Dynamic card generator and collection storage
from imgen import generate_card_image  # Function to generate the card image (assumed to be implemented)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
# Optionally restrict drops to a specific user:
MY_USER_ID = 239033440857489410

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class ClaimView(discord.ui.View):
    def __init__(self, card, user_id, image_path):
        super().__init__(timeout=60)  # View will timeout after 60 seconds
        self.card = card
        self.user_id = user_id
        self.image_path = image_path
        self.claimed = False

    @discord.ui.button(label="Claim Card", style=discord.ButtonStyle.green)
    async def claim_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Only allow the same user who dropped the card to claim it.
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This card drop is not for you!", ephemeral=True)
            return
        # If already claimed, don't do it again.
        if self.claimed:
            await interaction.response.send_message("You have already claimed this card.", ephemeral=True)
            return

        # Store the card in the user’s collection.
        add_card_to_collection(self.user_id, self.card)
        self.claimed = True
        button.disabled = True
        # Update the original message to indicate the card is claimed.
        await interaction.response.edit_message(content="Card claimed successfully!", view=self)

@tree.command(name="drop", description="Drop a Blue Lock card; click the button to claim it.")
async def drop(interaction: discord.Interaction):
    if interaction.user.id != MY_USER_ID:
        await interaction.response.send_message("You are not authorized to drop a card.", ephemeral=True)
        return

    card = generate_card()
    image_stream = generate_card_image(card)  # Assumed to return a BytesIO stream for the image
    
    embed = discord.Embed(
        title="Card Drop!",
        description="A new card has been dropped! Click the **Claim Card** button to add it to your collection."
    )
    if image_stream:
        embed.set_image(url="attachment://" + image_stream.name)
    
    view = ClaimView(card, interaction.user.id, image_stream)
    
    if image_stream:
        await interaction.response.send_message(embed=embed, view=view, file=discord.File(image_stream))
    else:
        await interaction.response.send_message(f"You dropped a card, but image generation failed.\n{card}", view=view)

@client.event
async def on_ready():
    try:
        synced = await tree.sync()  # Sync slash commands with Discord.
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    print(f"Logged in as {client.user}")

client.run(TOKEN)
