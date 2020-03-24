import os

from api.Pokemon import Pokemon

root_dir = os.path.dirname(os.path.abspath(os.path.dirname("api" + os.path.sep)))


# Saves the pokemon in a sub-folder. Please make sure you use an unformatted name ("lower-case")
def save_custom_pokemon(pokemon: Pokemon, unformatted_name=""):
    try:
        os.mkdir(os.path.join(root_dir, "custom"))
    except FileExistsError:
        pass
    f = open(os.path.join(root_dir, "custom", "pokemon.data"), "a")
    name = unformatted_name if unformatted_name != "" else pokemon.name
    types = []
    for _type in pokemon.types:
        types.append(_type.name)
    index = 808 + custom_pokemon_count()
    f.write(str(index) + ";" + name + ";" + str(types) + ";" + str(pokemon.base_stats) + "\n")
    print(name + " has been saved successfully with id " + str(index) + ".")
    f.close()


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