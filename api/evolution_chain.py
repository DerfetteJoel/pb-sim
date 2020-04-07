import copy

import pokepy
from beckett.exceptions import InvalidStatusCodeError

custom_evolution_chains = {}

evolution_details = {
                     "item": None,
                     "min_level": 0
                     }


class EvolutionChain:
    def __init__(self, chain_id):
        client = pokepy.V2Client()
        self.chain_id = chain_id
        self.base = None
        self.stage = 0
        self.stage_1_evolutions = {}
        self.stage_2_evolutions = {}
        try:
            raw = client.get_evolution_chain(chain_id)
        except InvalidStatusCodeError:
            raw = custom_evolution_chains.get(chain_id)
        if raw is not None:
            try:
                self.base = raw.chain.species.name
                for e in raw.chain.evolves_to:
                    evo_details = copy.deepcopy(evolution_details)
                    try:
                        evo_details["item"] = e.evolution_details[0].item.name
                    except AttributeError:
                        pass
                    evo_details["min_level"] = e.evolution_details[0].min_level or 0
                    self.stage_1_evolutions[e.species.name] = evo_details
                    for f in e.evolves_to:
                        evo_details = copy.deepcopy(evolution_details)
                        try:
                            evo_details["item"] = e.evolves_to[0].evolution_details[0].item.name
                        except AttributeError:
                            pass
                        evo_details["min_level"] = e.evolves_to[0].evolution_details[0].min_level or 0
                        self.stage_2_evolutions[f.species.name] = evo_details
            except AttributeError:
                self.base = raw.base
                self.stage = raw.stage
                self.stage_1_evolutions = raw.stage_1_evolutions
                self.stage_2_evolutions = raw.stage_2_evolutions

    def set_stage(self, name):
        if self.base == name:
            self.stage = 0
        elif name in self.stage_1_evolutions:
            self.stage = 1
        elif name in self.stage_2_evolutions:
            self.stage = 2
