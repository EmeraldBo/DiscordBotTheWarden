import nextcord
import supabaseMAIN 
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from variables import global_vars, server_vars

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    async def variable(self, interaction: Interaction):
        pass

    @variable.subcommand(description="Variable Testing")
    async def test(
        self,
        interaction: Interaction,
        type1: str = SlashOption(
            description="Type of variable",
            required=True,
            choices={
                "Global": "global_vars",
                "Server": "server_vars"
            }
        ),
        type2: str = SlashOption(
            description="Type of Value",
            required=True,
            choices={
                "Integer":"test_int",
                "String":"test_str"
            }
        )
    ):
        vars = {
            "global_vars": global_vars,
            "server_vars": server_vars
        }

        type1_map = {"global_vars": "Global", "server_vars": "Server"}

        response = f"This is a {type1_map[type1]} variable with the value of {vars[type1][type2]}"
        await interaction.response.send_message(response)
    
    @variable.subcommand(description="List all variables and their values for a user.")
    async def list(self, interaction: Interaction, user: nextcord.Member):
        user_data = supabaseMAIN.get_variable(user.id).data[0]
        balance = user_data['balance']
        inventory = user_data['inventory']

        embed = nextcord.Embed(
            title=f"Variables for {user.name}",
            description=f"Balance: {balance}\nInventory: {inventory}"
        )

        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command()
    async def supabase(self, interaction: Interaction):
        pass
    
    # CHANGE BALANCE
    @supabase.subcommand(description="Test Supabase Connection")
    async def add_balance(self, interaction: Interaction, amount: int = SlashOption(
            description="Amount of coins to set your balance to",
            required=True
    ), user: nextcord.Member = SlashOption(
        description="User to change the balance to",
        required=False
    )):
        user = user or interaction.user
        supabaseMAIN.set_variable(user.id, balance=amount)
        await interaction.response.send_message(f"Set balance to {amount} coins!")


    # ADD ITEM
    @supabase.subcommand(description="Test adding an item to the inventory")
    async def add_item(self, interaction: Interaction, 
       item: str = SlashOption(
            description="Item to add to your inventory",
            required=True
    ), amount: int = SlashOption(
            description="Amount of the item to add",
            required=True
    ), user: nextcord.Member = SlashOption(
        description="User to add the item to",
        required=False
    )):
        user = user or interaction.user
        inv = supabaseMAIN.get_variable(user.id).data[0]['inventory']
        inv[item] = amount 
        supabaseMAIN.set_variable(user.id, inventory=inv)
        
        await interaction.response.send_message(f"Added {amount} of {item} to inventory!")


    # REMOVE ITEMS
    @supabase.subcommand(description="Test subtracting an item to the inventory")
    async def remove_item(self, interaction: Interaction, 
        item: str = SlashOption(
            description="Item to subtract to your inventory",
            required=True
    ), amount: int = SlashOption(
            description="Amount of the item to subtract",
            required=True
    ), user: nextcord.Member = SlashOption(
        description="User to subtract the item from",
        required=False
    )):

        user = user or interaction.user
        inv = supabaseMAIN.get_variable(user.id).data[0]['inventory']
        if item in inv:
            inv[item] -= amount
            if inv[item] <= 0:
                del inv[item]
        supabaseMAIN.set_variable(user.id, inventory=inv)

        await interaction.response.send_message(f"Removed {amount} of {item} from inventory!")




# Cog Setup
async def setup(bot):
    bot.add_cog(Testing(bot))