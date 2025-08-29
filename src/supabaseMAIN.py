import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- SET VARIABLE ---
def set_variable(
    user_id: int,
    *,
    guild_id: int | None = None,
    balance: int | None = None,
    inventory: dict | None = None,
    health: int | None = None,
    stamina: int | None = None,
    defense: int | None = None,
    attack: int | None = None,
    max_health: int | None = None,
    attack_bonus: int | None = None,
    defense_bonus: int | None = None,
    special: int | None = None,
    equip_weapon: str | None = None,
    equip_armor: str | None = None,
    equip_spell: str | None = None,
):
    """Upsert user data. Only provided fields will be updated."""

    # Start with required key
    data = {"user_id": user_id}

    # Only add fields that are not None
    if guild_id is not None:
        data["guild_id"] = guild_id
    if balance is not None:
        data["balance"] = balance
    if inventory is not None:
        data["inventory"] = inventory
    if health is not None:
        data["health"] = health
    if stamina is not None:
        data["stamina"] = stamina
    if defense is not None:
        data["defense"] = defense
    if attack is not None:
        data["attack"] = attack
    if max_health is not None:
        data["max_health"] = max_health
    if attack_bonus is not None:
        data["attack_bonus"] = attack_bonus
    if defense_bonus is not None:
        data["defense_bonus"] = defense_bonus
    if special is not None:
        data["special"] = special
    if equip_weapon is not None:
        data["equip_weapon"] = equip_weapon
    if equip_armor is not None:
        data["equip_armor"] = equip_armor
    if equip_spell is not None:
        data["equip_spell"] = equip_spell

    return supabase.table("Discord Bot :D") \
        .upsert(data, on_conflict="user_id") \
        .execute()


# --- GET VARIABLE ---
def get_variable(
    user_id: int | None = None,
    guild_id: int | None = None,
    balance: int | None = None,
    inventory: dict | None = None,
    health: int | None = None,
    stamina: int | None = None,
    defense: int | None = None,
    attack: int | None = None,
    max_health: int | None = None,
    attack_bonus: int | None = None,
    defense_bonus: int | None = None,
    special: int | None = None
):
    """Fetch user data with optional filters."""

    query = supabase.table("Discord Bot :D").select("*")

    if user_id is not None:
        query = query.eq("user_id", user_id)
    if guild_id is not None:
        query = query.eq("guild_id", guild_id)
    if balance is not None:
        query = query.eq("balance", balance)
    if inventory is not None:
        query = query.eq("inventory", inventory)
    if health is not None:
        query = query.eq("health", health)
    if stamina is not None:
        query = query.eq("stamina", stamina)
    if defense is not None:
        query = query.eq("defense", defense)
    if attack is not None:
        query = query.eq("attack", attack)
    if max_health is not None:
        query = query.eq("max_health", max_health)
    if attack_bonus is not None:
        query = query.eq("attack_bonus", attack_bonus)
    if defense_bonus is not None:
        query = query.eq("defense_bonus", defense_bonus)
    if special is not None:
        query = query.eq("special", special)

    return query.execute()
