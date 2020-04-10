# pb-sim
pb-sim is a flexible api that can calculate Pokemon stats and
damage as well as presenting pokemon data to the console. It
gathers all data from [PokeAPI](https://pokeapi.co/), but is 
flexible enough to allow the user to create new Pokemon, Moves
and Types.

**Note that while the api is more or less stable, the client is extremely experimental at this point.**

If you want to use the client, you'll have to install PyQt5 via `pip install PyQt5`.

## Using the api
You can use the api directly from the python shell.
It is recommended that you start by loading all Pokemon data. Only three statements are necessary to do so:
1. `from api.util import io_utils`
2. `from api import pokemon`
3. `pokemon.pokemon_data = io_utils.load_all_pokemon()`
If everything was set up correctly, you'll get feedback on how many pokemon were loaded.

#### Example 1: Creating a Pokemon
1. Import `Pokemon` from `api.pokemon`.
2. Create an existing Pokemon by calling its name in the 
constructor: `bulbasaur = Pokemon("bulbasaur")`.
3. (Optional) Print Pokemon data to the console: `bulbasaur.print()`
will output formatted information about the Pokemon including its 
Types and Base Stats.

#### Example 2: Creating a move
1. Import `Move` from `api.move`.
2. Create an existing Move by calling it's name in the console:
`flamethrower = Move("flamethrower")`.

#### Example 3: Attacking a pokemon (calculating damage)
1. (Optional) Set the level of your Pokemon to any level you wish
using `bulbasaur.set_level(level)`. The level is 1 by default.
2. (Optional) Generate IVs and Nature.
This is done using `pkmn.generate()`.
3. Attack any pokemon you have instantiated by using 
`attack(other_pokemon, move)`. In our example, we can make
Bulbasaur attack itself using Flamethrower by calling
`bulbasaur.attack(bulbasaur, flamethrower)`.

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

#### Example 5: Saving custom Pokemon to a file
When saving custom pokemon to the custom dictionary, all of your
pokemon will be lost when you close the shell. `pb-sim` also
provides a way to save Pokemon permanently:
1. Import `io_utils` from `api.util`
2. Call `io_utils.save_custom_pokemon(custom)`

Now, Your pokemon will be saved in a sub-directory 
`data/custom/pokemon.json`. It will automatically get a unique 
ID starting at 808. You can load all of your custom Pokemon 
before instantiating new Pokemon and save them to the custom 
dictionary by calling 
`pokemon.pokemon_data = io_utils.load_all_pokemon()`.