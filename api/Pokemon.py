import math
import random
import pokepy
from beckett.exceptions import InvalidStatusCodeError


class Pokemon:
    def __init__(self, name):
        client = pokepy.V2Client()
        try:
            raw = client.get_pokemon(name)
        except InvalidStatusCodeError:
            print("Pokemon not found, creating a new one...")
            raw = 0
        if raw != 0:
            self.id = raw.id
            self.name = raw.name.capitalize()
            self.base_stats = [raw.stats[5].base_stat, raw.stats[4].base_stat, raw.stats[3].base_stat,
                               raw.stats[2].base_stat, raw.stats[1].base_stat, raw.stats[0].base_stat]
            self.types = [raw.types[0].type.name] if len(raw.types) == 1 \
                else [raw.types[0].type.name, raw.types[1].type.name]
        else:
            self.id = -1
            self.name = name
            self.base_stats = [0, 0, 0, 0, 0, 0]
            self.types = ["normal"]
        self.level = 1
        self.ivs = [0, 0, 0, 0, 0, 0]
        self.evs = [0, 0, 0, 0, 0, 0]
        self.stats = [0, 0, 0, 0, 0, 0]
        self.current_stats = [0, 0, 0, 0, 0, 0]  # for use in battle
        self.moves = []

    def set_level(self, level):
        self.level = level
        self.calculate_stats()

    def set_ev(self, index, value):
        self.evs[index] = value
        self.calculate_stats()

    # ========== FUNCTIONS FOR CALCULATING & GENERATING ================================================================

    def calculate_stats(self):
        self.stats[0] = math.floor(
            ((2 * self.base_stats[0] + self.ivs[0] + math.floor(self.evs[0] / 4)) * self.level) / 100) + self.level + 10
        for x in range(1, 6):
            self.stats[x] = math.floor(
                (((2 * self.base_stats[x] + self.ivs[x] + math.floor(self.evs[x] / 4)) * self.level) / 100) + 5)

    def generate_ivs(self):
        for x in range(0, 6):
            self.ivs[x] = random.randint(0, 31)
        self.calculate_stats()

    # ========== FUNCTIONS FOR USE IN & AFTER BATTLE ===================================================================

    def heal(self):
        self.current_stats = self.stats
