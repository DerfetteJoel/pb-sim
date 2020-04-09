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

# List of all custom pokemon that will be saved once the function 'save_custom_pokemon' is called
custom_pokemon_data = {'pokemon': []}

# List of all custom moves that will be saved once the function 'save_custom_move' is called
custom_move_data = {'moves': []}


# Saves the pokemon in a sub-folder. Please make sure you use an unformatted name ('lower-case')
def save_custom_pokemon(pkmn: Pokemon):
    try:
        os.makedirs(custom_path)
    except FileExistsError:
        pass
    unformatted_name = pkmn.name \
        .lower() \
        .replace(' ', '-')
    index = pkmn.id if pkmn.id != -1 else utils.TOTAL_POKEMON_COUNT + custom_pokemon_count()
    type_1 = pkmn.types[0].name
    type_2 = 'none'
    if len(pkmn.types) > 1:
        type_2 = pkmn.types[1].name
    ability_1 = 'none'
    ability_2 = 'none',
    ability_3 = 'none'
    try:
        ability_1 = pkmn.abilities[0]
        ability_2 = pkmn.abilities[1]
        ability_3 = pkmn.abilities[2]
    except IndexError:
        pass
    custom_pokemon_data['pokemon'].append({
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
        json.dump(custom_pokemon_data, file, indent=2)


# Saves the move in a sub-folder. Please make sure you use an unformatted name ('lower-case')
def save_custom_move(move: Move):
    try:
        os.makedirs(custom_path)
    except FileExistsError:
        pass
    unformatted_name = move.name.lower().replace(' ', '-')
    index = move.id if move.id != -1 else utils.TOTAL_POKEMON_COUNT + custom_pokemon_count()
    custom_move_data['moves'].append({
        'name': unformatted_name,
        'id': index,
        'accuracy': move.accuracy,
        'power': move.power,
        'pp': move.pp,
        'effect_chance': move.effect_chance,
        'priority': move.priority,
        'damage_class': move.damage_class,
        'type': move.type.name
    })
    with open(os.path.join(custom_path, 'moves.json'), 'w') as file:
        json.dump(custom_move_data, file, indent=2)


# Load all pokemon from /data/pokemon.json and /data/custom/pokemon.json
def load_all_pokemon():
    data = {}
    try:
        with open(os.path.join(root_dir, 'data', 'pokemon.json')) as json_data:
            raw_data = json.load(json_data)
        for key in raw_data['pokemon']:
            data[key['name']] = key
    except FileNotFoundError or UnboundLocalError:
        print('Pokemon data not found (this is bad). Try redownloading the data.')
    try:
        with open(os.path.join(root_dir, 'data', 'custom', 'pokemon.json')) as json_data:
            raw_custom_data = json.load(json_data)
        for key in raw_custom_data['pokemon']:
            data[key['name']] = key
    except FileNotFoundError or UnboundLocalError:
        print('No custom pokemon found.')
    print('Finished loading ' + str(len(data)) + ' pokemon.')
    return data


# Load all moves from /data/moves.json and /data/custom/moves.json
def load_all_moves():
    data = {}
    try:
        with open(os.path.join(root_dir, 'data', 'moves.json')) as json_data:
            raw_data = json.load(json_data)
        for key in raw_data['moves']:
            data[key['name']] = key
    except FileNotFoundError or UnboundLocalError:
        print('Move data not found (this is bad). Try redownloading the data.')
    try:
        with open(os.path.join(root_dir, 'data', 'custom', 'moves.json')) as json_data:
            raw_custom_data = json.load(json_data)
        for key in raw_custom_data['moves']:
            data[key['name']] = key
    except FileNotFoundError or UnboundLocalError:
        print('No custom moves found.')
    print('Finished loading ' + str(len(data)) + ' moves.')
    return data


# Returns the number of custom pokemon, needed for automatically indexing new pokemon
def custom_pokemon_count():
    return len(custom_pokemon_data)


# Returns the number of custom moves, needed for automatically indexing new moves
def custom_moves_count():
    return len(custom_move_data)


# Deletes all custom pokemon
def delete_custom_pokemon():
    count = custom_pokemon_count()
    os.remove(os.path.join(custom_path, 'pokemon.json'))
    if count == 1:
        print('1 Pokemon has been deleted.')
    else:
        print(str(count) + ' Pokemon have been deleted.')


def delete_custom_moves():
    count = custom_moves_count()
    os.remove(os.path.join(custom_path, 'move.json'))
    if count == 1:
        print('1 move has been deleted.')
    else:
        print(str(count) + ' moves have been deleted.')
