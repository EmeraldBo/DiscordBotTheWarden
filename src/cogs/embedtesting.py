import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

class EmbedTesting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    async def embed(self, interaction: Interaction):
        pass  # Serves as a parent group only

    @embed.subcommand(description="Create a new embed")
    async def create(
        self,
        interaction: Interaction,
        title: str = SlashOption(description="Title of the embed", required=True),
        description: str = SlashOption(description="Description of the embed", required=True),
        color: str = SlashOption(
            description="Color of the embed",
            required=True,
            choices={
                "White": "white",
                "Grey": "grey",
                "Black": "black",
                "Dark Red": "dark red",
                "Lime": "lime",
                "Greyish Blue": "grey blue",
                "Purple": "purple"
            }
        ),
    ):
        colors = {
            "white": 0xFFFFFF,
            "grey": 0x808080,
            "black": 0x000000,
            "dark red": 0x8B0000,
            "lime": 0x00FF00,
            "grey blue": 0x607D8B,
            "purple": 0x800080,
        }
        embed = nextcord.Embed(title=title, description=description, color=colors[color])
        await interaction.response.send_message(embed=embed)

    @embed.subcommand(description="Edit an existing embed by message ID")
    async def edit(
        self,
        interaction: Interaction,
        message_id: str = SlashOption(description="ID of the embed message", required=True),
        new_content: str = SlashOption(description="New content for the embed", required=True)
    ):
        try:
            message = await interaction.channel.fetch_message(int(message_id))
        except Exception:
            await interaction.response.send_message("Embed not found.", ephemeral=True)
            return

        if not message.embeds:
            await interaction.response.send_message("No embed in that message.", ephemeral=True)
            return
        
        embed = message.embeds[0]
        embed.description = new_content
        await message.edit(embed=embed)
        await interaction.response.send_message("Embed updated successfully.")

async def setup(bot):
    bot.add_cog(EmbedTesting(bot))