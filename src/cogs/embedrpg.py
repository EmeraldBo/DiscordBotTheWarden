import nextcord
import supabaseMAIN
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import random as rnd
from . import global_vars, server_vars, shop_items, enemies, bonus_stats

class FightView(nextcord.ui.View):
    def __init__(self, interaction, player, enemy):
        super().__init__(timeout=60)
        self.user_id = interaction.user.id
        self.player = player
        self.enemy = enemy
        self.turn = "player"
        self.player_hp = self.player["hp"]
        self.player_stamina = self.player["stamina"]
        self.enemy_hp = enemy["hp"]    
    def player_damage(self):
        damage = rnd.randint(max(0, self.enemy["atk"] - self.player["def"]), self.enemy["atk"]) - self.player.get('def_bonus', 0)
        self.player_hp -= damage
        supabaseMAIN.set_variable(self.user_id, health=self.player_hp)
        return damage
    
    def stamina_cost(self):
        cost = rnd.randint(5, 10)  # Example stamina cost
        self.player_stamina -= cost
        supabaseMAIN.set_variable(self.user_id, stamina=self.player_stamina)
        return cost
    
    def stamina_cost_magic(self):
        cost = rnd.randint(10, 20)  # Example stamina cost
        self.player_stamina -= cost
        supabaseMAIN.set_variable(self.user_id, stamina=self.player_stamina)
        return cost
    
    def stamina_regen(self):
        regen = rnd.randint(5, 10)  # Example stamina regen
        self.player_stamina += regen
        supabaseMAIN.set_variable(self.user_id, stamina=self.player_stamina)
        return regen

    async def update_message(self, interaction):
        desc = (
            f"**Battle!**\n\n"
            f"{interaction.user.display_name}: {self.player_hp}/{self.player['hp']} HP\n"
            f"Stamina: {self.player_stamina}/{self.player['stamina']} \n"
            f"{self.enemy['name']}: {self.enemy_hp}/{self.enemy['hp']} HP\n"
            f"It's {self.turn}'s turn!"
        )
        embed = nextcord.Embed(title="RPG Battle", description=desc)
        try:
            await interaction.response.edit_message(embed=embed, view=self)
        except nextcord.InteractionResponded:
            await interaction.edit_original_message(embed=embed, view=self)

    @nextcord.ui.button(label="Attack", style=nextcord.ButtonStyle.primary)
    async def attack(self, button, interaction: Interaction):
        if self.turn != "player":
            await interaction.response.send_message("It's not your turn!", ephemeral=True)
            return

        if self.player_stamina < 5:
            await interaction.response.send_message("Not enough stamina!", ephemeral=True)
            return

        damage = rnd.randint(max(1, self.player["atk"] - self.enemy["def"]), self.player["atk"]) + self.player["atk_bonus"]
        self.enemy_hp -= damage
        self.stamina_cost()  # Example stamina cost
        await interaction.response.send_message(f"You attacked {self.enemy['name']} for {damage} damage with {self.player['atk_bonus']} attack bonus!")

        if self.enemy_hp <= 0:
            await interaction.followup.send(f"You defeated {self.enemy['name']}!")
            self.stop()
            return

        self.turn = "enemy"
        await self.update_message(interaction)
        await self.enemy_attack(interaction)
    
    async def enemy_attack(self, interaction):
        dmg = self.player_damage()

        if self.player_hp <= 0:
            embed = nextcord.Embed(
                title="Defeat...",
                description=f"💀 {self.enemy['name']} defeated {interaction.user.display_name}!"
            )
            self.player_hp = 1  # Prevent negative HP
            supabaseMAIN.set_variable(interaction.user.id, health=self.player_hp)
            await interaction.edit_original_message(embed=embed, view=None)
            self.stop()
            return

        self.turn = "player"
        # update message again
        await self.update_message(interaction)
    
    async def enemy_attack_defense(self, interaction):
        dmg = self.player_damage() / 2

        if self.player_hp <= 0:
            embed = nextcord.Embed(
                title="Defeat...",
                description=f"💀 {self.enemy['name']} defeated {interaction.user.display_name}!"
            )
            self.player_hp = 1  # Prevent negative HP
            supabaseMAIN.set_variable(interaction.user.id, health=self.player_hp)
            await interaction.edit_original_message(embed=embed, view=None)
            self.stop()
            return

        self.turn = "player"
        # update message again
        await self.update_message(interaction)

    @nextcord.ui.button(label="Defend", style=nextcord.ButtonStyle.primary)
    async def defend(self, interaction):
        if self.turn != "player":
            await interaction.response.send_message("It's not your turn!", ephemeral=True)
            return

        self.stamina_regen()
        await interaction.response.send_message(f"You defended and increased your stamina!")

        self.turn = "enemy"
        await self.update_message(interaction)
        await self.enemy_attack(interaction)

    @nextcord.ui.button(label="Special", style=nextcord.ButtonStyle.primary)
    async def special(self, button, interaction: Interaction):
        if self.turn != "player":
            await interaction.response.send_message("It's not your turn!", ephemeral=True)
            return

        if self.player_stamina < 10:
            await interaction.response.send_message("Not enough stamina!", ephemeral=True)
            return

        damage = rnd.randint(max(1, self.player["atk"] - self.enemy["def"]), self.player["atk"]) + self.player["spec"] * 2

        self.enemy_hp -= damage
        self.stamina_cost_magic()  # Example stamina cost
        await interaction.response.send_message(f"You attacked {self.enemy['name']} for {damage} damage with {self.player['spec']} special bonus!")

        if self.enemy_hp <= 0:
            await interaction.followup.send(f"You defeated {self.enemy['name']}!")
            self.stop()
            return

        self.turn = "enemy"
        await self.update_message(interaction)
        await self.enemy_attack(interaction)

    @nextcord.ui.button(label="Run", style=nextcord.ButtonStyle.danger)
    async def run(self, button, interaction: Interaction):
        await interaction.response.send_message("You fled the battle!")
        self.stop()

class RPG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def find_item_price(self, item_name: str) -> int | None:
        """Search for an item price in shop_items (nested dict)."""
        for category in shop_items.values():
            if item_name in category:
                return category[item_name]
        return None

    def update_inventory(self, inv: dict, item: str, amount: int):
        """Update inventory with item addition/removal."""
        inv[item] = inv.get(item, 0) + amount
        if inv[item] <= 0:
            del inv[item]
        return inv

    def check_character(self, interaction):
        response = supabaseMAIN.get_variable(interaction.user.id)

        return response.data[0] if response.data else None
    # Grouping
    @nextcord.slash_command()
    async def rpg(self, interaction: Interaction):
        pass
    
    @rpg.subcommand(description="Create your character!")
    async def start(self, interaction: Interaction):
        user_id = supabaseMAIN.get_variable(interaction.user.id)

        if user_id:
            supabaseMAIN.set_variable(interaction.user.id)
            await interaction.response.send_message("Successfully made character, enjoy!")
        else:
            await interaction.response.send_message("You already have a character!")

    # INVENTORY
    @rpg.subcommand(description="Test the inventory")
    async def inventory(self, interaction: Interaction):

        user_data = self.check_character(interaction) or {}
        if not user_data:
            await interaction.response.send_message("You don’t have a character yet! Use `/rpg start` to begin.")
            return
        items = user_data['inventory'] or {}
        balance = user_data['balance'] or 0
        items_text = "\n".join([f"{item}: {amount}" for item, amount in items.items()]) if items else "No items"
        embed = nextcord.Embed(
            title="Inventory Test",
            description=f"Balance: {balance}\n\nYour inventory contains:\n{items_text}"
        )

        await interaction.response.send_message(embed=embed)

    # Shop
    @rpg.subcommand(description="Test the shop")
    async def shop(self, interaction: Interaction):
        
        def create_shop_embeds():
            categories = {}

            for category, items in shop_items.items():
                embeds = []
                items_per_page = 3
                pages = [list(items.items())[i:i+items_per_page] for i in range(0, len(items), items_per_page)]

                for page_num, page_items in enumerate(pages, start=1):
                    desc = f"# {category}:\n"
                    for name, price in page_items:
                        desc += f"- {name}: {price}\n"

                    embed = nextcord.Embed(
                        title=f"Shop {page_num}/{len(pages)}",
                        description=desc
                    )
                    embeds.append(embed)

                categories[category] = embeds

            return categories

        categories = create_shop_embeds()

        current_category = "Weapons"
        current_page = 0

        embed = categories[current_category][current_page]

        view = nextcord.ui.View()
        
        class CategorySelect(nextcord.ui.Select):
            def __init__(self):
                options = [
                    nextcord.SelectOption(label="Weapons", description="Browse weapons"),
                    nextcord.SelectOption(label="Armor", description="Browse armor"),
                    nextcord.SelectOption(label="Consumables", description="Browse consumables"),
                    nextcord.SelectOption(label="Collectibles", description="Browse collectibles"),
                    nextcord.SelectOption(label="Spells", description="Browse spells")
                ]
                super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)

            async def callback(self, interaction: Interaction):
                nonlocal current_category, current_page
                current_category = self.values[0]
                current_page = 0
                await interaction.response.edit_message(embed=categories[current_category][current_page], view=view)
            
        view.add_item(CategorySelect())

        # Previous Button
        prev_button = nextcord.ui.Button(label="<", style=nextcord.ButtonStyle.secondary)
        async def prev_callback(interaction: Interaction):
            nonlocal current_page
            current_page = (current_page - 1) % len(categories[current_category])
            await interaction.response.edit_message(embed=categories[current_category][current_page])

        prev_button.callback = prev_callback
        view.add_item(prev_button)
        
        # Next Button
        next_button = nextcord.ui.Button(label=">", style=nextcord.ButtonStyle.secondary)
        async def next_callback(interaction: Interaction):
            nonlocal current_page
            current_page = (current_page + 1) % len(categories[current_category])
            await interaction.response.edit_message(embed=categories[current_category][current_page])

        next_button.callback = next_callback
        view.add_item(next_button)

        await interaction.response.send_message(embed=embed, view=view)

    @rpg.subcommand(description="Buy items")
    async def buy(
        self,
        interaction: Interaction,
        item: str = SlashOption(
            description="Item to buy",
            required=True,
            choices=[i for cat in shop_items.values() for i in cat.keys()]  # flatten categories
        ),
        amount: int = SlashOption(description="Amount to buy", required=True)
    ):
        user_data = self.check_character(interaction)
        balance = user_data['balance'] or 0
        inv = user_data['inventory'] or {}

        item_price = self.find_item_price(item)
        if item_price is None:
            await interaction.response.send_message("That item doesn't exist in the shop!")
            return

        total_cost = item_price * amount
        if total_cost > balance:
            await interaction.response.send_message("You don't have enough coins!")
            return

        # Deduct balance + update inventory
        balance -= total_cost
        inv = self.update_inventory(inv, item, amount)

        supabaseMAIN.set_variable(interaction.user.id, balance=balance, inventory=inv)

        await interaction.response.send_message(f"✅ Bought {amount}x {item} for {total_cost} coins!")


    @rpg.subcommand(description="Sell items")
    async def sell(
        self,
        interaction: Interaction,
        item: str = SlashOption(
            description="Item to sell",
            required=True,
            choices=[i for cat in shop_items.values() for i in cat.keys()]
        ),
        amount: int = SlashOption(description="Amount to sell", required=True)
    ):
        user_data = self.check_character(interaction)
        balance = user_data['balance'] or 0
        inv = user_data['inventory'] or {}

        if item not in inv or inv[item] < amount:
            await interaction.response.send_message("You don't have enough of that item!")
            return

        item_price = self.find_item_price(item)
        if item_price is None:
            await interaction.response.send_message("That item can't be sold!")
            return

        total_gain = item_price * amount

        # Remove item(s) and add balance
        inv = self.update_inventory(inv, item, -amount)
        balance += total_gain

        supabaseMAIN.set_variable(interaction.user.id, balance=balance, inventory=inv)

        await interaction.response.send_message(f"💰 Sold {amount}x {item} for {total_gain} coins!")

    @rpg.subcommand(description="Equip a weapon/armor/spell!")
    async def equip(self, interaction: Interaction, item: str = SlashOption(
        choices=list(shop_items['Weapons'].keys()) +
                list(shop_items['Armor'].keys()) +
                list(shop_items['Spells'].keys()),
        description="Item to equip", required=True
    )):
        user_data = self.check_character(interaction)
        if not user_data:
            await interaction.response.send_message(
                "You don’t have a character yet! Use `/start` to begin."
            )
            return

        # ✅ Use defaults if values are None
        equip_weapon = user_data.get('equip_weapon') or None
        equip_armor = user_data.get('equip_armor') or None
        equip_spell = user_data.get('equip_spell') or None
        special = (bonus_stats["Spells"][item]['atk'] if item in bonus_stats["Spells"] else 0)
        attack_bonus = (bonus_stats["Weapons"][item]['atk'] if item in bonus_stats["Weapons"] else 0)
        defense_bonus = (bonus_stats["Armor"][item]['def'] if item in bonus_stats["Armor"] else 0)
        inv = user_data.get('inventory') or {}

        # Check if item exists in inventory
        if item not in inv or inv[item] < 1:
            await interaction.response.send_message("You do not have that item!")
            return

        # Check if already equipped
        if item in (equip_weapon, equip_armor, equip_spell):
            await interaction.response.send_message("That item is already equipped!")
            return

        # Equip logic
        if item in shop_items['Weapons']:
            supabaseMAIN.set_variable(interaction.user.id, attack_bonus=attack_bonus)
            supabaseMAIN.set_variable(interaction.user.id, equip_weapon=item)
            await interaction.response.send_message(f"Equipped weapon: {item}")
        elif item in shop_items['Armor']:
            supabaseMAIN.set_variable(interaction.user.id, defense_bonus=defense_bonus)
            supabaseMAIN.set_variable(interaction.user.id, equip_armor=item)
            await interaction.response.send_message(f"Equipped armor: {item}")
        elif item in shop_items['Spells']:
            supabaseMAIN.set_variable(interaction.user.id, special=special)
            supabaseMAIN.set_variable(interaction.user.id, equip_spell=item)
            await interaction.response.send_message(f"Equipped spell: {item}")


    @rpg.subcommand(description="Unequip a weapon/armor/spell!")
    async def unequip(self, interaction: Interaction, item: str = SlashOption(
        choices=list(shop_items['Weapons'].keys()) +
                list(shop_items['Armor'].keys()) +
                list(shop_items['Spells'].keys()),
        description="Item to unequip", required=True
    )):
        user_data = self.check_character(interaction)
        if not user_data:
            await interaction.response.send_message(
                "You don’t have a character yet! Use `/start` to begin."
            )
            return

        # ✅ Current equipped items
        equip_weapon = user_data.get('equip_weapon') or None
        equip_armor = user_data.get('equip_armor') or None
        equip_spell = user_data.get('equip_spell') or None

        # Check if the item is actually equipped
        if item not in (equip_weapon, equip_armor, equip_spell):
            await interaction.response.send_message("That item is not currently equipped!")
            return

        # Unequip logic
        if item == equip_weapon:
            supabaseMAIN.set_variable(interaction.user.id, attack_bonus=0, equip_weapon='')  # reset/remove bonus
            await interaction.response.send_message(f"Unequipped weapon: {item}")
        elif item == equip_armor:
            supabaseMAIN.set_variable(interaction.user.id, defense_bonus=0, equip_armor='')
            await interaction.response.send_message(f"Unequipped armor: {item}")
        elif item == equip_spell:
            supabaseMAIN.set_variable(interaction.user.id, special=0, equip_spell='')
            await interaction.response.send_message(f"Unequipped spell: {item}")

    @rpg.subcommand(description="Fight an enemy!")
    async def fight(self, interaction: Interaction, enemy: str):
        if enemy not in enemies:
            return await interaction.response.send_message("Enemy not found!", ephemeral=True)

        user_data = self.check_character(interaction)
        if not user_data:
            await interaction.response.send_message(
                "You don’t have a character yet! Use `/start` to begin."
            )
            return

        # ✅ Default stats if missing
        player_stats = {
            "name": interaction.user.display_name,
            "hp": user_data.get('health') or 0,
            "max_hp": user_data.get('max_health') or 0,
            "atk": user_data.get('attack') or 0,
            "atk_bonus": user_data.get('attack_bonus') or 0,
            "def": user_data.get('defense') or 0,
            "def_bonus": user_data.get('defense_bonus') or 0,
            "spec": user_data.get('special') or 0,
            "stamina": user_data.get('stamina') or 0,
            "max_stamina": user_data.get('max_stamina') or 0
        }
        enemy_stats = enemies[enemy].copy()

        view = FightView(interaction, player_stats, enemy_stats)
        embed = nextcord.Embed(
            title="Fight!",
            description=f"👤 {player_stats['name']}: {player_stats['hp']}/{player_stats['max_hp']} HP\n"
                        f"Stamina: {player_stats['stamina']}/{player_stats['max_stamina']} \n"
                        f"👹 {enemy_stats['name']}: {enemy_stats['hp']} HP\n\n"
                        f"It’s **your turn!**"
        )
        await interaction.response.send_message(embed=embed, view=view)
# Cog Setup
async def setup(bot):
    bot.add_cog(RPG(bot))
    await bot.sync_application_commands(guild_id=1405700347531497546)