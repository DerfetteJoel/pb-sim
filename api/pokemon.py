import math
import random

import pokepy
from beckett.exceptions import InvalidStatusCodeError

from api.move import Move
from api.nature import Nature, natures
from api.type import Type
from api.evolution_chain import EvolutionChain
from api.util import util

# This can be filled with custom pokemon from the outside, for example using IOUtils.get_all_custom_pokemon()
custom_pokemon = {}


class Pokemon:
    # This constructor seems intimidating, but it really isn't doing any magic.
    # First, it searches the requested Pokemon in PokeAPIs database. If it doesn't find it there,
    # It looks up the custom pokemon dictionary. If one of these searches is successful, the variable
    # 'raw' is assigned its data. Since both cases are similar, they are handled in the same if-clause.
    # If the constructor doesnt find the pokemon either in the database nor in the custom dict, it creates a new
    # Pokemon.
    def __init__(self, name, base_stats=[0, 0, 0, 0, 0, 0], types=[Type("normal")], index=-1):
        client = pokepy.V2Client()
        self.id = index
        self.name = name.replace("-", " ").title()
        self.base_stats = base_stats
        self.types = types
        self.abilities = []
        self.base_experience = 0
        self.growth_rate = "slow"
        self.moves = []  # Moves will be saved in a dictionary to also save additional data like learn method and level
        self.evolves_to = {}
        try:
            raw = client.get_pokemon(name)
            util.log(raw.name + " was found in the database!")
        except InvalidStatusCodeError:
            util.log(name + " not found in the database, searching for custom Pokemon...")
            raw = custom_pokemon.get(name)
        if raw is not None:
            # Since the data is stored a bit differently in PokeApis database, the constructor cant use the same
            # code in the 2 scenarios (Pokemon found in database / Pokemon found in custom dict). It will just try
            # anyways.
            try:  # This is used in case the pokemon was found in the database
                self.base_stats = [raw.stats[5].base_stat, raw.stats[4].base_stat, raw.stats[3].base_stat,
                                   raw.stats[2].base_stat, raw.stats[1].base_stat, raw.stats[0].base_stat]
                self.types = [Type(raw.types[0].type.name)] if len(raw.types) == 1 \
                    else [Type(raw.types[0].type.name), Type(raw.types[1].type.name)]
                for a in raw.abilities:
                    self.abilities.insert(a.slot, a.ability.name)
                self.growth_rate = client.get_pokemon_species(name).growth_rate.name
                for m in raw.moves:
                    move_name = m.move.name
                    learn_method = m.version_group_details[0].move_learn_method.name
                    level_learned_at = m.version_group_details[0].level_learned_at
                    self.moves.append({"name": move_name, "learn_method": learn_method,
                                       "level_learned_at": level_learned_at})
                chain_id = client.get_pokemon_species(name).evolution_chain.url.split('/')[-2]
                self.evolution_chain = EvolutionChain(chain_id)
                self.evolution_chain.set_stage(raw.name)
                if self.evolution_chain.stage == 0:
                    self.evolves_to = self.evolution_chain.stage_1_evolutions
                elif self.evolution_chain.stage == 1:
                    self.evolves_to = self.evolution_chain.stage_2_evolutions
            except AttributeError:
                # This is used in case the pokemon was not found in the database,
                # but in the custom dict
                util.log("Custom Pokemon " + raw.name + " found!")
                self.base_stats = raw.base_stats
                self.types = raw.types
                self.abilities = raw.abilities
                self.growth_rate = raw.growth_rate
                self.moves = raw.moves
            self.id = raw.id
            self.name = raw.name.replace("-", " ").title()
            self.base_experience = raw.base_experience
        else:
            # If no pokemon in the database matched the request, these values can
            # be set manually or automatically using the constructor parameters.
            # This gives the user the ability to create completely new pokemon.
            util.log("No custom Pokemon found. Creating a new Pokemon.")
        while '' in self.abilities:
            self.abilities.remove('')  # remove "empty" abilities
        # These are values that can be different for each pokemon of a species
        self.level = 1
        self.ivs = [0, 0, 0, 0, 0, 0]
        self.evs = [0, 0, 0, 0, 0, 0]
        self.nature = Nature("hardy")
        self.stats = [0, 0, 0, 0, 0, 0]
        self.current_moves = []
        for m in self.moves:
            if m["level_learned_at"] == self.level:
                self.current_moves.append(Move(m["name"]))
        self.current_xp = self.exp(self.level)
        self.current_stats = [0, 0, 0, 0, 0, 0]  # Values that are needed in battle
        self.calculate_stats()
        self.heal()  # Set current stats

    # Use set_level rather than accessing level directly to automatically recalculate stats
    def set_level(self, level):
        self.level = level
        self.calculate_stats()
        # The following lines ensure that a Pokemon's current stats are recalculated upon the level up,
        # but the missing hp (if any) are not restored. This way, a hit pokemon won't magically heal
        # when it levels up.
        hp_diff = self.stats[0] - self.current_stats[0]  # If the is at full hp, this will be 0
        self.heal()
        self.current_stats[0] -= hp_diff

    # Adds amount xp to current_xp, calculates if there are any level ups, and checks for any level up moves
    def add_xp(self, amount):
        self.current_xp += amount
        old_stats = []
        for i in self.stats:
            old_stats.append(i)
        stat_diff = [0, 0, 0, 0, 0, 0]
        old_level = self.level
        new_level = self.level
        while (self.current_xp > self.exp(new_level)) and (new_level < 100):
            new_level += 1
        for i in range(0, new_level - old_level):
            self.set_level(self.level + 1)
            print(self.name + " reached Level " + str(self.level) + "! (", end='')
            for j in range(0, 6):
                stat_diff[j] = self.stats[j] - old_stats[j]
                print("+" + str(stat_diff[j]), end='')
                if j < 5: print(", ", end='')
            print(")")
            if self.evolution_chain.stage != 2:
                self.try_level_evolution()
            for j in range(0, 6):
                old_stats[j] = self.stats[j]
            for m in self.moves:
                if m["level_learned_at"] == self.level:
                    move = Move(m["name"])
                    if len(self.current_moves) == 4:
                        replace = 5
                        print(self.name + " wants to learn " + move.name + ", but it already knows 4 Moves:")
                        print(self.current_moves[0].name + ", " + self.current_moves[1].name + ", " +
                              self.current_moves[2].name + ", " + self.current_moves[3].name)
                        while 1:
                            try:
                                _in = input("Please specify which move shall be forgotten(1-4), "
                                            "leave empty if no move should be forgotten: ")
                                if _in != '': replace = int(_in)
                                else: replace = None
                                if (replace is None) or (1 <= replace <= 4):
                                    break
                            except ValueError:
                                pass
                            print("Invalid Input!")
                        if replace is not None:
                            print(self.name + " forgot " + self.current_moves[replace - 1].name + " and learned " +
                                  move.name + "!")
                            self.current_moves[replace - 1] = move
                        else:
                            print(self.name + " did not learn " + move.name + ".")
                    else:
                        self.current_moves.append(move)
                        print(self.name + " learned " + move.name + "!")

    # Use set_ev rather than accessing ev directly to automatically recalculate stats
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

    # Checks if min_level in evolves_to is sufficient and will attempt an evolution
    def try_level_evolution(self):
        if self.evolution_chain.stage == 2:
            return
        evolution_name = list(self.evolves_to.keys())[0]
        evolution_level = self.evolves_to[evolution_name]["min_level"]
        if (self.level >= evolution_level) and (evolution_level != 0):
            confirmation = ""
            while (confirmation.lower() != 'a') or (confirmation.lower() != 'b'):
                try:
                    confirmation = input(self.name + " is evolving! Type b to abort, leave empty to continue: ")
                    if (confirmation.lower() == '') or (confirmation.lower() == 'b'):
                        break
                except ValueError:
                    pass
                print("Invalid Input!")
            if confirmation == '':
                # perform evolution
                old_name = self.name
                evolution = Pokemon(evolution_name)
                evolution.name.replace("-", " ").title()
                evolution.current_xp = self.current_xp
                evolution.current_moves = self.current_moves
                evolution.ivs = self.ivs
                evolution.evs = self.evs
                evolution.nature = self.nature
                evolution.set_level(self.level)
                self.__dict__ = evolution.__dict__
                print("Congratulations! Your " + old_name + " evolved into " + self.name + "!")
                return
            print(self.name + " did not evolve.")

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
