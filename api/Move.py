import pokepy
from beckett.exceptions import InvalidStatusCodeError


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
            self.name = raw.name.capitalize()
            self.accuracy = raw.accuracy
            self.power = raw.power
            self.pp = raw.pp
            self.effect_chance = raw.effect_chance
            self.priority = raw.priority
            self.damage_class = raw.damage_class.name
            self.type = raw.type.name
        else:
            self.id = -1  # TODO automatic indexing system
            self.name = name
            self.accuracy = 100
            self.power = 0
            self.pp = 5
            self.effect_chance = None
            self.priority = 0
            self.damage_class = "physical"
            self.type = "normal"
        self.current_pp = self.pp

    def set_current_pp(self, value):
        self.current_pp = value if value <= self.pp else self.pp
