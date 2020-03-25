import pokepy
from beckett.exceptions import InvalidStatusCodeError

from api.type import Type


class Move:
    def __init__(self, name):
        client = pokepy.V2Client()
        try:
            raw = client.get_move(name)
        except InvalidStatusCodeError:
            print("Move not found, creating a new one...")
            raw = 0
        if raw != 0:
            self.id = raw.id
            self.name = raw.name.replace("-", " ").title()
            self.accuracy = raw.accuracy
            self.power = raw.power
            self.pp = raw.pp
            self.effect_chance = raw.effect_chance
            self.priority = raw.priority
            self.damage_class = raw.damage_class.name
            self.type = Type(raw.type.name)
        else:
            # If no move in the database matched the request, these values have to be set manually.
            # This gives the user the ability to create completely new moves.
            self.id = -1  # TODO automatic indexing system
            self.name = name
            self.accuracy = 100
            self.power = 0
            self.pp = 5
            self.effect_chance = None
            self.priority = 0
            self.damage_class = "physical"
            self.type = Type("normal")

        self.current_pp = self.pp

    def set_current_pp(self, value):
        self.current_pp = value if value <= self.pp else self.pp

    def refill_pp(self):
        self.current_pp = self.pp

    # Returns the effectiveness of the move against a given Pokemon 'pokemon' as a number between 0 and 2
    def get_effectivity(self, pokemon):
        effectivity = 1
        for _type in pokemon.types:
            if self.type.name in _type.double_damage_from:
                effectivity *= 2
            elif self.type.name in _type.half_damage_from:
                effectivity /= 2
            elif self.type.name in _type.no_damage_from:
                effectivity = 0
        return effectivity
