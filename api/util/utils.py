enable_log = 0

TOTAL_POKEMON_COUNT = 807
TOTAL_MOVES_COUNT = 728
TOTAL_EVOLUTION_CHAIN_COUNT = 419

TYPE_COLORS = {
    'normal': '#a8a87e',
    'fighting': '#b23c31',
    'flying': '#a493ea',
    'poison': '#95499c',
    'ground': '#dcc075',
    'rock': '#b5a04b',
    'bug': '#acb642',
    'ghost': '#6c5b94',
    'steel': '#b8b9ce',
    'fire': '#e25844',
    'water': '#6f92e9',
    'grass': '#8bc561',
    'electric': '#f2d054',
    'psychic': '#e66488',
    'ice': '#a6d7d7',
    'dragon': '#6745ef',
    'dark': '#6d594a',
    'fairy': '#e29dac',
    '???': '#759f91'
}


def log(msg: object) -> object:
    """If logging is enabled, prints a log message to the console."""
    if enable_log:
        print(f'[LOG] {msg}')
