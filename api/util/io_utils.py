import os
import json

from api import pokemon
from api.evolution_chain import EvolutionChain
from api.move import Move
from api.pokemon import Pokemon
from api.type import Type
from api.util import utils

root_dir = os.path.dirname(os.path.abspath(os.path.dirname('api' + os.path.sep)))
custom_path = os.path.join(root_dir, 'data', 'custom')  # Path to the directory where all custom data is stored

# List of all custom pokemon that will be saved in the json file
pokemon_data = {'pokemon': []}

# List of all custom moves that will be saved in the json file
move_data = {'moves': []}


# Saves the pokemon in a sub-folder. Please make sure you use an unformatted name ('lower-case')
def save_custom_pokemon(pkmn: Pokemon):
    try:
        os.makedirs(custom_path)
    except FileExistsError:
        pass
    unformatted_name = pkmn.name\
        .lower()\
        .replace(' ', '-')
    index = utils.TOTAL_POKEMON_COUNT + custom_pokemon_count()
    type_1 = pkmn.types[0].name
    type_2 = 'none'
    if len(pkmn.types) > 1:
        type_2 = pkmn.types[1].name
    ability_1 = pkmn.abilities[0]
    ability_2 = 'none',
    ability_3 = 'none'
    try:
        ability_2 = pkmn.abilities[1]
        ability_3 = pkmn.abilities[2]
    except IndexError: pass
    pokemon_data['pokemon'].append({
        'name': unformatted_name,
        'id': index,
        'types': {'type_1': type_1, 'type_2': type_2},
        'abilities': {'ability_1': ability_1, 'ability_2': ability_2, 'ability_3': ability_3},
        'base_stats': pkmn.base_stats,
        'evolution_chain_id': pkmn.evolution_chain.chain_id,
        'growth_rate': pkmn.growth_rate,
        'base_xp': pkmn.base_experience,
        'moves': pkmn.moves
    })
    with open(os.path.join(custom_path, 'pokemon.json'), 'w') as file:
        json.dump(pokemon_data, file, indent=2)


# Saves the move in a sub-folder. Please make sure you use an unformatted name ('lower-case')
def save_custom_move(move: Move):
    try:
        os.makedirs(custom_path)
    except FileExistsError:
        pass
    unformatted_name = move.name.lower().replace(' ', '-')
    move_data['moves'].append({
        'name': unformatted_name,
        'id': utils.TOTAL_MOVES_COUNT + custom_moves_count(),
        'accuracy': move.accuracy,
        'power': move.power,
        'pp': move.pp,
        'effect_chance': move.effect_chance,
        'priority': move.priority,
        'damage_class': move.damage_class,
        'type': move.type.name
    })
    with open(os.path.join(custom_path, 'moves.json'), 'w') as file:
        json.dump(move_data, file, indent=2)


# Returns all custom pokemon as a dictionary
def get_all_custom_pokemon():
    print('Reading all custom Pokemon from \'data/custom/pokemon.data\'...')
    custom_pokemon = {}
    try:
        file = open(os.path.join(custom_path, 'pokemon.json'))
    except FileNotFoundError:
        print('No custom Pokemon found.')
        return
    data = json.load(file)
    file.close()
    for key in data['pokemon']:
        pkmn = Pokemon(key['name'], key['base_stats'], [Type(key['types']['type_1'])], key['id'])
        type_2 = key['types']['type_2']
        if type_2 != 'none': pkmn.types.append(Type(type_2))
        for abilities in key['abilities']:
            if abilities != 'none':
                pkmn.abilities.append(key['abilities'][abilities])
        pkmn.base_stats = key['base_stats']
        pkmn.evolution_chain = EvolutionChain(key['evolution_chain_id'])
        pkmn.growth_rate = key['growth_rate']
        pkmn.base_experience = key['base_xp']
        pkmn.moves = key['moves']
        custom_pokemon[key['name']] = pkmn
    print('Finished reading custom Pokemon. Found ' + str(len(custom_pokemon)) + ' Pokemon.')
    return custom_pokemon


def get_all_custom_moves():
    print('Reading all custom Pokemon from \'custom/moves.json\'...')
    custom_moves = {}
    try:
        file = open(os.path.join(custom_path, 'moves.json'), 'r')
    except FileNotFoundError:
        print('No custom moves found.')
        return
    data = json.load(file)
    for key in data['moves']:
        move = Move(key['name'])
        move.id = key['id']
        move.accuracy = key['accuracy']
        move.power = key['power']
        move.pp = key['pp']
        move.effect_chance = key['effect_chance']
        move.priority = key['priority']
        move.damage_class = key['damage_class']
        move.type = Type(key['type'])
        custom_moves[key['name']] = move
    file.close()
    print('Finished reading custom Moves. Found ' + str(len(custom_moves)) + ' Moves.')
    return custom_moves


# Returns the number of custom pokemon, needed for automatically indexing new pokemon
def custom_pokemon_count():
    return len(pokemon_data)


# Returns the number of custom moves, needed for automatically indexing new moves
def custom_moves_count():
    return len(move_data)


# Deletes all custom pokemon
def delete_custom_pokemon():
    count = custom_pokemon_count()
    os.remove(os.path.join(custom_path, 'pokemon.data'))
    if count == 1:
        print('1 Pokemon has been deleted.')
    else:
        print(str(count) + ' Pokemon have been deleted.')


def delete_custom_moves():
    count = custom_moves_count()
    os.remove(os.path.join(custom_path, 'move.data'))
    if count == 1:
        print('1 move has been deleted.')
    else:
        print(str(count) + ' moves have been deleted.')
