import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load environment variables and get the token from .env file.
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up bot intents and the command prefix.
intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    async def setup_hook(self):
        # Load cog extensions asynchronously.
        extensions = ['cogs.drop', 'cogs.list', 'cogs.show']
        for ext in extensions:
            try:
                await self.load_extension(ext)
                print(f"Loaded extension: {ext}")
            except Exception as e:
                print(f"Failed to load extension {ext}: {e}")
        # Sync slash commands.
        try:
            await self.tree.sync()
            print("Slash commands synchronized!")
        except Exception as e:
            print(f"Failed to sync slash commands: {e}")

# Initialize the bot using our custom subclass.
bot = MyBot(command_prefix="^", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Run the bot.
bot.run(TOKEN)
