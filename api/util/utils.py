enable_log = False

TOTAL_POKEMON_COUNT = 807
TOTAL_MOVES_COUNT = 728
TOTAL_EVOLUTION_CHAIN_COUNT = 419


def log(msg: object):
    """If logging is enabled, prints a log message to the console."""
    if enable_log:
        print(f'[LOG] {msg}')
