evolution_chain_data = {}
"""This can be filled with evolution chains from the outside, for example using IOUtils.load_all_evolution_chains()"""

evolution_details = {
    'item': None,
    'min_level': 0
}


class EvolutionChain:
    """
    EvolutionChain contains information about all evolutions a pokemon with the matching chain_id can perform.
    All Pokemon that stem from the same Base Pokemon also share the same evolution chain id.
    """

    def __init__(self, chain_id: int):
        """
        Will attempt to load the evolution chain specified by 'name' out of 'evolution_chain_data'.
        If no matching evolution chain could be found, a new evolution chain is created.
        """
        self.chain_id = chain_id
        self.base = None
        self.stage_1_evolutions = {}
        self.stage_2_evolutions = {}
        raw = evolution_chain_data.get(chain_id)
        if raw is not None:
            self.base = raw['base']
            self.stage_1_evolutions = raw['stage_1_evolutions']
            self.stage_2_evolutions = raw['stage_2_evolutions']
        self.stage = 0

    def set_stage(self, name):
        """
        Searches the evolution chain for 'name' and sets the stage accordingly.
        A pokemon's stage is avalue between 0 and 2.
        """
        if self.base == name:
            self.stage = 0
        elif name in self.stage_1_evolutions:
            self.stage = 1
        elif name in self.stage_2_evolutions:
            self.stage = 2
