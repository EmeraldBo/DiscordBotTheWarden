import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import cogs
import sys
from importlib import reload

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command(name="reload")
    async def reload(self, ctx, extension: str):
        try:

            if 'cogs' in sys.modules:
                reload(sys.modules['cogs'])

            self.bot.reload_extension(f"cogs.{extension}")
            await ctx.send(f"Reloaded {extension} (and cogs/__init__.py if needed) successfully!")
        except Exception as e:
            await ctx.send(f"Failed to reload {extension}. Error: {e}")

    @commands.command(name="load")
    async def load(self, ctx, extension: str):
        try:
            self.bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"Loaded {extension} successfully!")
        except Exception as e:
            await ctx.send(f"Failed to load {extension}. Error: {e}")
    
    @commands.command(name="unload")
    async def unload(self, ctx, extension: str):
        try:
            self.bot.unload_extension(f"cogs.{extension}")
            await ctx.send(f"Unloaded {extension} successfully!")
        except Exception as e:
            await ctx.send(f"Failed to unload {extension}. Error: {e}")

def setup(bot):
    bot.add_cog(AdminCommands(bot))