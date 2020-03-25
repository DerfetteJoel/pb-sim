# pb-sim
pb-sim is a flexible api that can calculate Pokemon stats and
damage as well as presenting pokemon data to the console. It
gathers all data from [PokeAPI](https://pokeapi.co/), but is 
flexible enough to allow the user to create new Pokemon, Moves
and Types.

A client is planned that makes using the api more user-friendly.

## Using the api
You can use the api directly from the python shell.

#### Example 1: Creating a Pokemon
1. Import `Pokemon` from `api.pokemon`.
2. Create an existing Pokemon by calling its name in the 
constructor: `pkmn = Pokemon("bulbasaur")`. Note: You can also pass
the id of the pokemon, however that won't work when you want to get
a custom Pokemon so it's best practice to always use the name.
3. (Optional) Print Pokemon data to the console: `pkmn.print()`
will output formatted information about the Pokemon including its 
Types and Base Stats.

#### Example 2: Creating a move
1. Import `Move` from `api.move`.
2. Create an existing Move by calling it's name in the console:
`move = Move("flamethrower")`.

#### Example 3: Attacking a pokemon (calculating damage)
1. (Optional) Set the level of your Pokemon to any level you wish
using `pkmn.set_level(level)`. The level is 1 by default.
2. (Optional) Generate IVs, Nature and calculate the stats.
This is done using `pkmn.generate()`. You can skip step 3 if you
used this.
3. Calculate stats using `pkmn.calculate_stats()` and 
then `pkmn.heal()` to also set current stats used in battle.
4. Attack any pokemon you have instantiated by using 
`pkmn.attack(other_pokemon, move)`. In our example, we can make
Bulbasaur attack itself using Flamethrower by calling
`pkmn.attack(pkmn, move)`.

#### Example 4: Creating a completely new Pokemon
1. Call `custom = Pokemon(name)` using a unique, new name that
won't be found in PokeAPIs database, for example
`custom = Pokemon("dialga-primal")`.
2. Set the Pokemon's Base Stats, Types and ID by accessing its
variables directly: 
`custom.base_stats = [200, 160, 180, 160, 180, 90]`, 
`custom.types = [Type("dragon"), Type("steel")]`,
`custom.id = 808`. Pro-tip: You can also specify all of these
values directly in the constructor: 
`custom = Pokemon(name, base_stats, types, index)`
3. (Optional) Print your new pokemon to the console using
`custom.print()`.

#### Example 5: Saving custom Pokemon
When a Pokemon is created, the constructor first searches for a 
match in PokeAPIs database. If it doesn't find the specified
Pokemon there, it then searches in a dictionary where all custom
pokemon you created can be saved.
1. Import `pokemon` from `api`
2. Add your custom pokemon to the database by using
`pokemon.custom_dict["dialga-primal"] = custom`. Make sure the name
is lowercase, with spaces replaced by hyphens.

The next time you create a Pokemon with the name "dialga-primal",
The api won't create a brand new Pokemon, but instead instantiate
a new Pokemon with the stats, types and index of your Pokemon 
`custom`.

#### Example 6: Saving custom Pokemon to a file
When saving custom pokemon to the custom dictionary, all of your
pokemon will be lost when you close the shell. `pb-sim` also
provides a way to save Pokemon permanently:
1. Import `io_utils` from `api.util`
2. Call `io_utils.save_custom_pokemon(custom, "dialga-primal")`

Now, Your pokemon will be saved in a sub-directory 
`custom/pokemon.data`. It will automatically get a unique ID
starting at 808. You can load all of your custom Pokemon before
instantiating new Pokemon and save them to the custom dictionary
by calling 
`pokemon.custom_dict = io_utils.get_all_custom_pokemon()`.