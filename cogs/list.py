import discord
from discord import app_commands
from discord.ext import commands
from responses import get_user_cards

class ListNavigationView(discord.ui.View):
    def __init__(self, user_id: int, initial_page: int = 1):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.page = initial_page
        self.update_button_states()

    def update_button_states(self):
        # Disable the Previous button if on the first page.
        if self.page <= 1:
            self.previous_page.disabled = True
        else:
            self.previous_page.disabled = False

        # Check if there is a next page by comparing against the user_cards count.
        user_cards = get_user_cards(self.user_id)
        max_page = ((len(user_cards) - 1) // 10 + 1) if user_cards else 1
        if self.page >= max_page:
            self.next_page.disabled = True
        else:
            self.next_page.disabled = False

    def generate_embed(self) -> discord.Embed:
        user_cards = get_user_cards(self.user_id)
        start = (self.page - 1) * 10
        end = start + 10

        # Create description for the embed.
        if not user_cards or start >= len(user_cards):
            description = "No cards on this page. Please check your page number."
        else:
            page_cards = user_cards[start:end]
            description = ""
            for idx, card in enumerate(page_cards, start=start + 1):
                description += f"**{idx}.** {card['serial_number']} ({card['name']})\n"

        embed = discord.Embed(
            title=f"Your Cards (Page {self.page})",
            description=description,
            color=0x1abc9c
        )
        return embed

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Only let the original user interact.
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your card list!", ephemeral=True)
            return

        # Decrement the page number.
        self.page = max(1, self.page - 1)
        self.update_button_states()
        embed = self.generate_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Only let the original user interact.
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your card list!", ephemeral=True)
            return

        # Increment the page number.
        self.page += 1
        self.update_button_states()
        embed = self.generate_embed()
        await interaction.response.edit_message(embed=embed, view=self)


class ListCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="list",
        description="List your cards in your collection, 10 per page with navigation."
    )
    async def list(self, interaction: discord.Interaction, page: int = 1):
        user_cards = get_user_cards(interaction.user.id)
        if not user_cards:
            await interaction.response.send_message("You have no card!", ephemeral=True)
            return

        view = ListNavigationView(interaction.user.id, page)
        embed = view.generate_embed()
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(ListCog(bot))
