import os

from api import pokemon
from api.pokemon import Pokemon
from api.type import Type

root_dir = os.path.dirname(os.path.abspath(os.path.dirname("api" + os.path.sep)))


# Saves the pokemon in a sub-folder. Please make sure you use an unformatted name ("lower-case")
def save_custom_pokemon(pkmn, unformatted_name: str):
    try:
        os.mkdir(os.path.join(root_dir, "custom"))
    except FileExistsError:
        pass
    f = open(os.path.join(root_dir, "custom", "pokemon.data"), "a")
    unformatted_name.replace(";", "")  # make sure no apostrophes are in the unformatted name
    types = pkmn.types[0].name
    if len(pkmn.types) > 1:
        types += "," + pkmn.types[1].name
    abilities = pkmn.abilities[0]
    for i in range(1, len(pkmn.abilities)):
        abilities += "," + pkmn.abilities[i]
    index = 808 + custom_pokemon_count()
    f.write(str(index) + ";" + unformatted_name + ";" + str(pkmn.base_stats) + ";" + str(types) + ";" + abilities +
            ";\n")
    print(unformatted_name + " has been saved successfully with id " + str(index) + ".")
    f.close()


# Returns all custom pokemon as a dictionary
def get_all_custom_pokemon():
    print("Reading all custom Pokemon from \"custom/pokemon.data\"...")
    pokemon.enable_log = 0  # Temporarily disable constructor output to avoid spam
    custom_pokemon = {}
    try:
        f = open(os.path.join(root_dir, "custom", "pokemon.data"), "r")
    except FileNotFoundError:
        print("No custom Pokemon found.")
        pokemon.enable_log = 1
        return
    for x in range(0, custom_pokemon_count()):
        raw = f.readline().split(';')
        raw_base_stats = []
        for t in raw[2][1:-1].strip().split(','):
            raw_base_stats.append(int(t))
        raw_types = []
        for t in raw[3].split(','):
            raw_types.append(Type(t))
        raw_abilities = []
        for t in raw[4].split(','):
            raw_abilities.append(t)
        pkmn = Pokemon(raw[1], raw_base_stats, raw_types, raw[0])
        pkmn.abilities = raw_abilities
        custom_pokemon[raw[1]] = pkmn
    f.close()
    print("Finished reading custom Pokemon. Found " + str(len(custom_pokemon)) + " Pokemon.")
    pokemon.enable_log = 1  # Enabling constructor log again.
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
