import nextcord
from nextcord.ext import commands

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello!")
    
    @commands.command()
    async def embed(self, ctx):
        embed = nextcord.Embed(colour=None, title="test embed", type='rich', url=None, description="hello there, mate.", timestamp=None)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Hello(bot))