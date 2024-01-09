WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
MANA_BAR_SIZE = 140
ITEM_BOX_SIZE = 80
UI_FONT = "graphics/fonts/IMMORTAL.ttf"
UI_FONT_SIZE = 18

# colors
UI_BG_COLOR = "#363b42"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"
WATER_COLOR = "#5c699f"

# ui colors
HEALTH_COLOR = "red"
MANA_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

# upgrade menu
TEXT_COLOR_SELECTED = "#111111"
BAR_COLOR = "#EEEEEE"
BAR_COLOR_SELECTED = "#111111"
UPGRADE_UI_FONT = "graphics/fonts/prstartk.ttf"
UPGRADE_BG_COLOR_SELECTED = "#EEEEEE"

WORLD_MAP = [["p"]]

weapon_data = {
    "sword": {
        "cooldown": 100,
        "damage": 15,
        "graphic": "graphics/weapons/sword/full.png",
    },
    "axe": {"cooldown": 300, "damage": 20, "graphic": "graphics/weapons/axe/full.png"},
}

magic_data = {
    "flame": {
        "strength": 5,
        "cost": 20,
        "damage": 40,
        "graphic": "graphics/magic/flame/fire.png",
    },
    "heal": {
        "strength": 10,
        "cost": 10,
        "damage": 0,
        "graphic": "graphics/magic/heal/heal.png",
    },
}

upgrade_exp_data = {
    "health": {"actual": 0, "max": 6},
    "attack": {"actual": 0, "max": 3},
    "mana": {"actual": 0, "max": 3},
    "magic": {"actual": 0, "max": 3},
    "speed": {"actual": 0, "max": 3},
}

upgrade_gold_data = {
    "sword": {"actual": 0, "max": 6},
    "axe": {"actual": 0, "max": 6},
    "heal": {"actual": 0, "max": 6},
    "flame_damage": {"actual": 0, "max": 6},
    "flame_range": {"actual": 0, "max": 3},
}

# enemy
monster_data = {
    "fire": {
        "health": 90,
        "exp": 100,
        "gold": 2,
        "damage": 20,
        "attack_type": "flame",
        "speed": 2,
        "resistance": 3,
        "attack_radius": 80,
        "notice_radius": 300,
    },
    "ghost": {
        "health": 100,
        "exp": 150,
        "gold": 2,
        "damage": 15,
        "attack_type": "flame",
        "speed": 2,
        "resistance": 3,
        "attack_radius": 80,
        "notice_radius": 360,
    },
    "bee": {
        "health": 70,
        "exp": 50,
        "gold": 1,
        "damage": 10,
        "attack_type": "flame",
        "speed": 2,
        "resistance": 3,
        "attack_radius": 80,
        "notice_radius": 250,
    },
}
