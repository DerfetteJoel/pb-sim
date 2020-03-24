from api.Move import Move
from api.Pokemon import Pokemon

if __name__ == '__main__':
    pokemon = Pokemon(1)
    move = Move("flamethrower")
    print(move.get_effectivity(pokemon))
    print(pokemon.name)
