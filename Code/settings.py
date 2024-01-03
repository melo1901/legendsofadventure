WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
MANA_BAR_SIZE = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'graphics/fonts/IMMORTAL.ttf'
UI_FONT_SIZE = 18

# colors
UI_BG_COLOR = '#363b42'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
MANA_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_UI_FONT = 'graphics/fonts/prstartk.ttf'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

WORLD_MAP = [
    ["p"]
]

weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15, 'graphic':'graphics/weapons/sword/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'graphics/weapons/axe/full.png'}
}

magic_data = {
    'flame': {'strength' : 5, 'cost': 20, 'damage' : 40, 'graphic' : 'graphics/magic/flame/fire.png'},
	'heal': {'strength' : 10, 'cost': 10, 'damage' : 0, 'graphic' : 'graphics/magic/heal/heal.png'}
}

#enemy
monster_data = {
    'fire' : {'health': 300, 'exp': 100, 'damage': 20, 'attack_type': 'flame', 'speed': 2, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 300},
    'ghost' : {'health': 360, 'exp': 150, 'damage': 15, 'attack_type': 'flame', 'speed': 2, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'bee' : {'health': 150, 'exp': 50, 'damage': 10, 'attack_type': 'flame', 'speed': 2, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 250}
}