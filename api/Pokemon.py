import math
import random
import pokepy
from beckett.exceptions import InvalidStatusCodeError

from api.Type import Type


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
            self.types = [Type(raw.types[0].type.name)] if len(raw.types) == 1 \
                else [Type(raw.types[0].type.name), Type(raw.types[1].type.name)]
        else:
            # If no pokemon in the database matched the request, these values have to be set manually.
            # This gives the user the ability to create completely new pokemon.
            self.id = -1  # TODO automatic indexing system
            self.name = name
            self.base_stats = [0, 0, 0, 0, 0, 0]
            self.types = ["normal"]

        # These are values that can be different for each pokemon of a species
        self.level = 1
        self.ivs = [0, 0, 0, 0, 0, 0]
        self.evs = [0, 0, 0, 0, 0, 0]
        self.stats = [0, 0, 0, 0, 0, 0]
        self.moves = []
        # Values that are needed in battle
        self.current_stats = [0, 0, 0, 0, 0, 0]  # newly generated pokemon have to heal once for these values to be set.

    # Use set_level rather than accessing level directly to automatically recalculate stats
    def set_level(self, level):
        self.level = level
        self.calculate_stats()

    # Use set_level rather than accessing level directly to automatically recalculate stats
    def set_ev(self, index, value):
        self.evs[index] = value
        self.calculate_stats()

    # ========== FUNCTIONS FOR CALCULATING & GENERATING ================================================================

    # TODO use natures in calculate_stats
    def calculate_stats(self):
        self.stats[0] = math.floor(
            ((2 * self.base_stats[0] + self.ivs[0] + math.floor(self.evs[0] / 4)) * self.level) / 100) + self.level + 10
        for x in range(1, 6):
            self.stats[x] = math.floor(
                (((2 * self.base_stats[x] + self.ivs[x] + math.floor(self.evs[x] / 4)) * self.level) / 100) + 5)

    # Randomly generates all IVs for a pokemon
    def generate_ivs(self):
        for x in range(0, 6):
            self.ivs[x] = random.randint(0, 31)
        self.calculate_stats()

    # ========== FUNCTIONS FOR USE IN & AFTER BATTLE ===================================================================

    # Reset all stats
    # TODO reset pokemon status once implemented
    def heal(self):
        self.current_stats = self.stats
