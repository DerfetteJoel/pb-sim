enable_log = 0

TOTAL_POKEMON_COUNT = 808
TOTAL_MOVES_COUNT = 746
TOTAL_EVOLUTION_CHAIN_COUNT = 419


def log(msg: object) -> object:
    if enable_log:
        print('[LOG] ', end='')
        print(msg)
