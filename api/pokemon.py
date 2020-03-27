import math
import random

import pokepy
from beckett.exceptions import InvalidStatusCodeError

from api.nature import Nature, natures
from api.type import Type

# This can be filled with custom pokemon from the outside, for example using IOUtils.get_all_custom_pokemon()
custom_dict = {}

# Set this to 0 if you want to disable Pokemon constructor messages
enable_log = 1


class Pokemon:
    def __init__(self, name, base_stats=[0, 0, 0, 0, 0, 0], types=[Type("normal")], index=-1):
        client = pokepy.V2Client()
        self.abilities = ["", "", ""]
        self.moves = []
        raw = None
        try:
            raw = client.get_pokemon(name)
            if raw is not None:
                self.id = raw.id
                self.name = raw.name.replace("-", " ").title()
                self.base_stats = [raw.stats[5].base_stat, raw.stats[4].base_stat, raw.stats[3].base_stat,
                                   raw.stats[2].base_stat, raw.stats[1].base_stat, raw.stats[0].base_stat]
                self.types = [Type(raw.types[0].type.name)] if len(raw.types) == 1 \
                    else [Type(raw.types[0].type.name), Type(raw.types[1].type.name)]
                for a in raw.abilities:
                    self.abilities.insert(a.slot, a.ability.name)
                self.base_experience = raw.base_experience
                self.growth_rate = client.get_pokemon_species(name).growth_rate.name
                for m in raw.moves:
                    self.moves.append(m.move.name)
        except InvalidStatusCodeError:
            if enable_log: print(name + " not found, searching for custom Pokemon...")
            try:
                raw = custom_dict.get(name)
            except AttributeError:
                if enable_log: print("Custom dictionary seems to be empty...")
            if raw is not None:
                if enable_log: print("Custom Pokemon " + raw.name + " found!")
                self.id = raw.id
                self.name = raw.name.replace("-", " ").title()
                self.base_stats = raw.base_stats
                self.types = raw.types
                self.abilities = ["none"]
                self.base_experience = 0
                self.growth_rate = "slow"
            else:
                # If no pokemon in the database matched the request, these values can
                # be set manually or automatically using the constructor parameters.
                # This gives the user the ability to create completely new pokemon.
                if enable_log: print("No custom Pokemon found. Creating new Pokemon from template.")
                self.id = index
                self.name = name.replace("-", " ").title()
                self.base_stats = base_stats
                self.types = types
                self.abilities = ["none"]
                self.base_experience = 0
                self.growth_rate = "slow"
        while '' in self.abilities:
            self.abilities.remove('')  # remove "empty" abilities

        # These are values that can be different for each pokemon of a species
        self.level = 1
        self.ivs = [0, 0, 0, 0, 0, 0]
        self.evs = [0, 0, 0, 0, 0, 0]
        self.nature = Nature("hardy")
        self.stats = [0, 0, 0, 0, 0, 0]
        self.current_moves = []
        self.current_xp = 0
        self.set_level(5)  # If no level is specified, it is set to 5 by default
        # Values that are needed in battle
        self.current_stats = [0, 0, 0, 0, 0, 0]
        self.heal()  # Set current stats

    # Use set_level rather than accessing level directly to automatically recalculate stats
    def set_level(self, level):
        self.level = level
        self.current_xp = self.exp(level)
        self.calculate_stats()

    # Use set_level rather than accessing level directly to automatically recalculate stats
    def set_ev(self, index, value):
        self.evs[index] = value
        self.calculate_stats()

    # Calculates the amount of xp needed to reach the level
    def exp(self, level):
        if self.growth_rate == "slow-then-very-fast":
            if level <= 1:
                return 0
            elif (level > 1) and (level <= 50):
                return math.floor((level ** 3) * ((100 - level) / 50))
            elif (level > 50) and (level <= 68):
                return math.floor((level ** 3) * ((150 - level) / 100))
            elif (level > 68) and (level <= 98):
                return math.floor((level ** 3) * (math.floor((1911 - 10 * level) / 3) / 500))
            else:
                return math.floor((level ** 3) * ((160 - level) / 100))
        elif self.growth_rate == "fast":
            if level <= 1:
                return 0
            else:
                return math.floor((4 * (level ** 3)) / 5)
        elif self.growth_rate == "medium-fast":
            return level ** 3
        elif self.growth_rate == "medium-slow":
            if level <= 1:
                return 0
            else:
                return math.floor(((6 / 5) * (level ** 3)) - (15 * (level ** 2)) + (100 * level) - 140)
        elif self.growth_rate == "slow":
            if level <= 1:
                return 0
            else:
                return math.floor((5 * (level ** 3)) / 4)
        elif self.growth_rate == "fast-then-very-slow":
            if level <= 1:
                return 0
            elif (level > 1) and (level <= 15):
                return math.floor((level ** 3) * ((24 + math.floor((level + 1) / 3)) / 50))
            elif (level > 15) and (level <= 36):
                return math.floor((level ** 3) * ((14 + level) / 50))
            else:
                return math.floor((level ** 3) * ((32 + math.floor(level / 2)) / 50))

    # Calculates the xp that self gets for defeating Pokemon other
    def battle_xp(self, other):
        return math.floor(((other.base_experience * other.level) / 5) *
                          (((2 * other.level + 10) ** 2.5) / ((other.level + self.level + 10) ** 2.5)) + 1)

    # Print formatted information about the Pokemon species on the screen
    def print(self):
        print("_" * 56)
        types = self.types[0].name.capitalize()
        if len(self.types) > 1: types += (", " + self.types[1].name.capitalize())
        print('{:<20} {:>35}'.format(self.name, types))
        print("\nBase Stats:")
        for stat in self.base_stats:
            i = math.ceil(stat / 10) * 2
            print("█" * i + "░" * (52 - i) + " " + str(stat))
        print("Total: " + str(sum(self.base_stats)))
        print('_' * 56)

    # ========== FUNCTIONS FOR CALCULATING & GENERATING ================================================================

    def calculate_stats(self):
        self.stats[0] = math.floor(
            ((2 * self.base_stats[0] + self.ivs[0] + math.floor(self.evs[0] / 4)) * self.level) / 100) + self.level + 10
        for x in range(1, 6):
            self.stats[x] = math.floor(
                (((2 * self.base_stats[x] + self.ivs[x] + math.floor(self.evs[x] / 4)) * self.level) / 100) + 5)
            if x == self.nature.increased_stat:
                self.stats[x] = math.floor(self.stats[x] * 1.1)
            elif x == self.nature.decreased_stat:
                self.stats[x] = math.floor(self.stats[x] * 0.9)

    # Randomly generates all IVs for a pokemon
    def generate_ivs(self):
        for x in range(0, 6):
            self.ivs[x] = random.randint(0, 31)
        self.calculate_stats()

    # Randomly generate a nature
    def generate_nature(self):
        self.nature = Nature(natures[random.randint(0, len(natures) - 1)])
        self.calculate_stats()

    # All-In-One method for generating all required values for a new pokemon
    def generate(self):
        self.generate_ivs()
        self.generate_nature()
        self.calculate_stats()
        self.heal()

    # ========== FUNCTIONS FOR USE IN & AFTER BATTLE ===================================================================

    # Reset all stats
    # TODO reset pokemon status once implemented
    def heal(self):
        self.current_stats = self.stats

    # This method is used to perform an attack against a Pokemon 'other' using the Move 'move'
    def attack(self, other, move):
        print(self.name + " used " + move.name + "!")
        if random.randint(1, 100) > move.accuracy:
            print("The opposing " + other.name + " avoided the attack!")
            return
        damage = math.floor(self.level * 2 / 5) + 2
        damage *= move.power
        if move.damage_class == "special":
            damage *= self.current_stats[3] / (50 * other.current_stats[4])
        else:
            damage *= self.current_stats[1] / (50 * other.current_stats[2])
        damage = math.floor(damage)
        damage += 2
        critical = (1.5 if random.randint(1, 100) < 7 else 1)  # Critical chance is set to 6% for now
        if critical > 1: print("A critical hit!")
        damage *= critical
        damage = math.floor(damage)
        damage *= (random.randint(85, 100) / 100)
        damage = math.floor(damage)
        if len(self.types) == 1:
            if self.types[0].name == move.type.name:
                damage *= 1.5
        elif (self.types[0].name == move.type.name) or (self.types[1].name == move.type.name):
            damage *= 1.5
        damage = math.floor(damage)
        effectivity = move.get_effectivity(other)
        damage *= effectivity
        if effectivity >= 2:
            print("It's super effective!")
        elif effectivity < 1:
            print("It's not very effective...")
        elif effectivity == 0:
            print("It doesn't affect the opposing " + other.name + "...")
        damage = math.floor(damage)
        if damage > other.current_stats[0]: damage = other.current_stats[0]
        print("The opposing " + other.name + " lost "
              + str(math.floor((damage / other.stats[0]) * 100)) + "% (" + str(damage) + " HP) of its health!")
        other.current_stats[0] -= damage
