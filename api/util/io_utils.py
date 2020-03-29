import os

from api import pokemon
from api.move import Move
from api.pokemon import Pokemon
from api.type import Type

root_dir = os.path.dirname(os.path.abspath(os.path.dirname("api" + os.path.sep)))
custom_path = os.path.join(root_dir, "data", "custom")  # Path to the directory where all custom data is stored


# Saves the pokemon in a sub-folder. Please make sure you use an unformatted name ("lower-case")
def save_custom_pokemon(pkmn: Pokemon, unformatted_name: str):
    try:
        os.makedirs(custom_path)
    except FileExistsError:
        pass
    f = open(os.path.join(custom_path, "pokemon.data"), "a")
    unformatted_name.replace(";", "")  # make sure no apostrophes are in the unformatted name
    types = pkmn.types[0].name
    if len(pkmn.types) > 1:
        types += "," + pkmn.types[1].name
    abilities = pkmn.abilities[0]
    for i in range(1, len(pkmn.abilities)):
        abilities += "," + pkmn.abilities[i]
    moves = str(pkmn.moves[0]) if pkmn.moves else ""
    for i in range(1, len(pkmn.moves)):
        moves += "," + str(pkmn.moves[i])
    moves = moves.replace(" ", "").replace("'", "").replace("},{", "#").replace("{", "").replace("}", "")
    index = 808 + custom_pokemon_count()
    f.write(str(index) + ";" + unformatted_name + ";" + str(pkmn.base_stats) + ";" + str(types) + ";" + abilities
            + ";" + str(pkmn.base_experience) + ";" + pkmn.growth_rate + ";" + moves + ";\n")
    print(unformatted_name + " has been saved successfully with id " + str(index) + ".")
    f.close()


# Saves the move in a sub-folder. Please make sure you use an unformatted name ("lower-case")
def save_custom_move(move: Move, unformatted_name: str):
    try:
        os.makedirs(custom_path)
    except FileExistsError:
        pass
    f = open(os.path.join(custom_path, "move.data"), "a")
    index = 729 + custom_moves_count()
    f.write(str(index) + ";" + move.name + ";" + str(move.accuracy) + ";" + str(move.power) + ";"
            + str(move.pp) + ";" + str(move.effect_chance) + ";" + str(move.priority) + ";"
            + move.damage_class + ";" + move.type.name + ";\n")
    print(unformatted_name + " has been saved successfully with id " + str(index))
    f.close()


# Returns all custom pokemon as a dictionary
def get_all_custom_pokemon():
    print("Reading all custom Pokemon from \"data/custom/pokemon.data\"...")
    pokemon.enable_log = 0  # Temporarily disable constructor output to avoid spam
    custom_pokemon = {}
    try:
        f = open(os.path.join(custom_path, "pokemon.data"), "r")
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
        raw_moves = []
        for t in raw[7].split('#'):
            raw_m = t.split(',')
            move_name = raw_m[0].split(':')[1]
            learn_method = raw_m[1].split(':')[1]
            level_learned_at = int(raw_m[2].split(':')[1])
            raw_moves.append({"name": move_name, "learn_method": learn_method,
                              "level_learned_at": level_learned_at})
        pkmn = Pokemon(raw[1], raw_base_stats, raw_types, raw[0])
        pkmn.abilities = raw_abilities
        pkmn.base_experience = int(raw[5])
        pkmn.growth_rate = raw[6]
        pkmn.moves = raw_moves
        custom_pokemon[raw[1]] = pkmn
    f.close()
    print("Finished reading custom Pokemon. Found " + str(len(custom_pokemon)) + " Pokemon.")
    pokemon.enable_log = 1  # Enabling constructor log again.
    return custom_pokemon


def get_all_custom_moves():
    print("Reading all custom Pokemon from \"custom/pokemon.data\"...")
    custom_moves = {}
    try:
        f = open(os.path.join(custom_path, "move.data"), "r")
    except FileNotFoundError:
        print("No custom moves found.")
        return
    for x in range(0, custom_moves_count()):
        raw = f.readline().split(';')
        move = Move(raw[1])
        move.id = int(raw[0])
        move.accuracy = int(raw[2])
        move.power = int(raw[3])
        move.pp = int(raw[4])
        move.effect_chance = int(raw[5]) if raw[5] != "None" else None
        move.priority = int(raw[6])
        move.damage_class = raw[7]
        move.type = Type(raw[8])
        custom_moves[raw[1]] = move
    f.close()
    print("Finished reading custom Moves. Found " + str(len(custom_moves)) + " Moves.")
    return custom_moves


# Returns the number of custom pokemon, needed for automatically indexing new pokemon
def custom_pokemon_count():
    with open(os.path.join(custom_path, "pokemon.data"), "r") as f:
        i = -1
        for i, l in enumerate(f):
            pass
    return i + 1


# Returns the number of custom moves, needed for automatically indexing new moves
def custom_moves_count():
    with open(os.path.join(custom_path, "move.data"), "r") as f:
        i = -1
        for i, l in enumerate(f):
            pass
    return i + 1


# Deletes all custom pokemon
def delete_custom_pokemon():
    count = custom_pokemon_count()
    os.remove(os.path.join(custom_path, "pokemon.data"))
    if count == 1:
        print("1 Pokemon has been deleted.")
    else:
        print(str(count) + " Pokemon have been deleted.")


def delete_custom_moves():
    count = custom_moves_count()
    os.remove(os.path.join(custom_path, "move.data"))
    if count == 1:
        print("1 move has been deleted.")
    else:
        print(str(count) + " moves have been deleted.")
