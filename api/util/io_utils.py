import os

from api.pokemon import Pokemon
from api.type import Type

root_dir = os.path.dirname(os.path.abspath(os.path.dirname("api" + os.path.sep)))


# Saves the pokemon in a sub-folder. Please make sure you use an unformatted name ("lower-case")
def save_custom_pokemon(pokemon, unformatted_name):
    try:
        os.mkdir(os.path.join(root_dir, "custom"))
    except FileExistsError:
        pass
    f = open(os.path.join(root_dir, "custom", "pokemon.data"), "a")
    types = pokemon.types[0].name
    if len(pokemon.types) > 1:
        types += "," + pokemon.types[1].name
    index = 808 + custom_pokemon_count()
    f.write(str(index) + ";" + unformatted_name + ";" + str(types) + ";" + str(pokemon.base_stats) + ";\n")
    print(unformatted_name + " has been saved successfully with id " + str(index) + ".")
    f.close()


# Returns all custom pokemon as a dictionary
def get_all_custom_pokemon():
    custom_pokemon = {}
    f = open(os.path.join(root_dir, "custom", "pokemon.data"), "r")
    for x in range(0, custom_pokemon_count()):
        raw = f.readline().split(';')
        raw_types = []
        for t in raw[2].split(','):
            raw_types.append(Type(t))
        raw_base_stats = []
        for t in raw[3][1:-1].strip().split(','):
            raw_base_stats.append(int(t))
        pkmn = Pokemon(raw[1], raw_base_stats, raw_types, raw[0])
        custom_pokemon[raw[1]] = pkmn
    f.close()
    return custom_pokemon


# Returns the number of custom pokemon, needed for automatically indexing new pokemon
def custom_pokemon_count():
    with open(os.path.join(root_dir, "custom", "pokemon.data"), "r") as f:
        i = -1
        for i, l in enumerate(f):
            pass
    return i + 1


# Deletes all custom pokemon
def delete_custom_pokemon():
    count = custom_pokemon_count()
    os.remove(os.path.join(root_dir, "custom", "pokemon.data"))
    if count == 1:
        print("1 Pokemon has been deleted.")
    else:
        print(str(count) + " Pokemon have been deleted.")
