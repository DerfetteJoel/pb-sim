from api.type import Type
from api.util import utils

move_data = {}
"""This can be filled with moves from the outside, for example using IOUtils.load_all_moves()"""


class Move:
    """Contains all data and methods needed for a move."""

    def __init__(self, name):
        """
        Will attempt to load the move specified by 'name' out of 'move_data'.
        If no matching move could be found, a new move is created.
        """
        raw = move_data.get(name)
        if raw is not None:
            self.damage_class = raw['damage_class']
            self.type = Type(raw['type'])
            self.id = raw['id']
            self.name = raw['name'].replace('-', ' ').title()
            self.accuracy = raw['accuracy']
            self.power = raw['power']
            self.pp = raw['pp']
            self.effect_chance = raw['effect_chance']
            self.priority = raw['priority']
        else:
            # If no move in the database matched the request, these values have to be set manually.
            # This gives the user the ability to create completely new moves.
            utils.log(name + ' not found. Creating a new move')
            self.id = -1
            self.name = name.replace('-', ' ').title()
            self.accuracy = 100
            self.power = 0
            self.pp = 5
            self.effect_chance = None
            self.priority = 0
            self.damage_class = 'physical'
            self.type = Type('normal')

        self.current_pp = self.pp

    def set_current_pp(self, value):
        self.current_pp = value if value <= self.pp else self.pp

    def refill_pp(self):
        self.current_pp = self.pp

    def get_effectivity(self, pokemon):
        """Return the effectivity of the move against a given Pokemon 'pokemon' as a number between 0 and 2."""
        effectivity = 1
        for _type in pokemon.types:
            if self.type.name in _type.double_damage_from:
                effectivity *= 2
            elif self.type.name in _type.half_damage_from:
                effectivity /= 2
            elif self.type.name in _type.no_damage_from:
                effectivity = 0
        return effectivity
