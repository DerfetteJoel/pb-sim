from operator import itemgetter

import pokepy

from api.util import utils


def get_pokemon(pokemon_name: str):
    """Returns a dictionary containing all necessary data about the pokemon"""
    client = pokepy.V2Client()
    raw = client.get_pokemon(pokemon_name)
    types = []
    for i in range(len(raw.types) - 1, -1, -1):
        types.append(raw.types[i].type.name)
    abilities = []
    for i in range(len(raw.abilities) - 1,  -1, -1):
        abilities.append(raw.abilities[i].ability.name)
    base_stats = []
    for i in range(len(raw.stats) - 1, -1, -1):
        base_stats.append(raw.stats[i].base_stat)
    raw_species = client.get_pokemon_species(pokemon_name)
    move_list = []
    for key in raw.moves:
        move_list.append({
            'name': key.move.name,
            'learn_method': key.version_group_details[0].move_learn_method.name,
            'level_learned_at': key.version_group_details[0].level_learned_at
        })
    move_list.sort(key=itemgetter('level_learned_at'))
    move_list.sort(key=itemgetter('learn_method'))
    poke_data = {
        'name': raw.name,
        'id': raw.id,
        'types': types,
        'abilities': abilities,
        'base_stats': base_stats,
        'base_xp': raw.base_experience,
        'evolution_chain_id': raw_species.evolution_chain.url.split('/')[-2],
        'growth_rate': raw_species.growth_rate.name,
        'base_happiness': raw_species.base_happiness,
        'capture_rate': raw_species.capture_rate,
        'gender_rate': raw_species.gender_rate,
        'hatch_counter': raw_species.hatch_counter,
        'moves': move_list
    }
    utils.log(f'{pokemon_name} found in the database!')
    return poke_data


def get_move(move_name: str):
    """Returns a dictionary containing all necessary data about the move"""
    client = pokepy.V2Client()
    raw = client.get_move(move_name)
    move_data = {
        'name': raw.name,
        'id': raw.id,
        'accuracy': raw.accuracy,
        'power': raw.power,
        'pp': raw.pp,
        'effect_chance': raw.effect_chance,
        'priority': raw.priority,
        'damage_class': raw.damage_class.name,
        'type': raw.type.name,
        'description': raw.effect_entries[0].effect
    }
    utils.log(f'{move_name} found in the database!')
    return move_data


def get_evolution_chain(chain_id: int):
    """Returns a dictionary containing all necessary data about the evolution chain"""
    client = pokepy.V2Client()
    raw = client.get_evolution_chain(chain_id)
    stage_1_evolutions = []
    for key in raw.chain.evolves_to:
        try:
            item = key.evolution_details[0].item.name
        except AttributeError:
            item = None
        stage_1_evolutions.append({
            'name': key.species.name,
            'evolution_details': {
                'item': item,
                'min_level': key.evolution_details[0].min_level
            }
        })
    stage_2_evolutions = []
    for key in raw.chain.evolves_to[0].evolves_to:
        try:
            item = key.evolution_details[0].item.name
        except AttributeError:
            item = None
        stage_2_evolutions.append({
            'name': key.species.name,
            'evolution_details': {
                'item': item,
                'min_level': key.evolution_details[0].min_level
            }
        })
    evo_data = {
        'chain_id': raw.id,
        'base': raw.chain.species.name,
        'stage_1_evolutions': stage_1_evolutions,
        'stage_2_evolutions': stage_2_evolutions
    }
    utils.log(f'Evolution chain {chain_id} found in the database!')
    return evo_data
