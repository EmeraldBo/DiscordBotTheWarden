import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    default_guild_ids=[1405700347531497546]  # Applies to all slash commands
)

# Load cogs *before* starting the bot

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    synced = await bot.sync_application_commands()
    print(f"Synced {len(synced)} slash commands:")
    for cmd in synced:
        print(f" • {cmd.name}")

async def main():
    for filename in os.listdir("./src/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension(f"cogs.{filename[:-3]}")
    await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())