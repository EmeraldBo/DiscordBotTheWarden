global_vars = {
    "test_int": 15,
    "test_str": "This is a global Variable",

    "money": 100
}

server_vars = {
    "test_int": 30,
    "test_str": "This is a server Variable"
}

shop_items = {
    "Weapons": {
        "Wooden Sword": 15,
        "Stone Sword": 30,
        "Iron Sword": 45,
        "Slingshot": 5,
        "Wooden Bow": 15,
        "Compound Bow": 30,
        "Wooden Dagger": 10,
        "Stone Dagger": 20,
        "Iron Dagger": 30,
    },
    "Armor": {
        "Leather Clothing": 15,
        "Chainmail Armor": 25,
        "Iron Armor": 35,
    },
    "Consumables": {
        "Health Potion": 5,
        "Mana Potion": 5,
        "Stamina Potion": 5,
    },
    "Collectibles": {
        "Phainon Plushy": 33550336
    },
    "Spells": {
        "Fireball Spell": 50,
        "Ice Shard Spell": 40,
        "Lightning Bolt Spell": 60
    }
}

enemies = {
    "goblin": {
        "name": "Goblin",
        "hp": 30,
        "atk": 5,
        "def": 2
    },
    "orc": {
        "name": "Orc",
        "hp": 50,
        "atk": 8,
        "def": 4
    },
    "phainon": {
        "name": "Phainon",
        "hp": 33550336,
        "atk": 100,
        "def": 1000
    }
}

bonus_stats = {
    "Weapons": {
        "Wooden Sword": {"atk": 4, "def": 0, "spec": 0},
        "Stone Sword": {"atk": 6, "def": 0, "spec": 0},
        "Iron Sword": {"atk": 8, "def": 0, "spec": 0},
        "Slingshot": {"atk": 3, "def": 0, "spec": 0},
        "Wooden Bow": {"atk": 5, "def": 0, "spec": 0},
        "Compound Bow": {"atk": 7, "def": 0, "spec": 0},
        "Wooden Dagger": {"atk": 2, "def": 0, "spec": 0},
        "Stone Dagger": {"atk": 4, "def": 0, "spec": 0},
        "Iron Dagger": {"atk": 6, "def": 0, "spec": 0},
    },
    "Armor": {
        "Leather Armor": {"atk": 0, "def": 2, "spec": 0},
        "Chainmail Armor": {"atk": 0, "def": 4, "spec": 0},
        "Plate Armor": {"atk": 0, "def": 6, "spec": 0},
    },
    "Spells": {
        "Fireball Spell": {"atk": 0, "def": 0, "spec": 10},
        "Ice Shard Spell": {"atk": 0, "def": 0, "spec": 20},
        "Lightning Bolt Spell": {"atk": 0, "def": 0, "spec": 30}
    }
}