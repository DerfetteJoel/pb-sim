class Type:
    """A pokemon's type determines if attacks against it are going to be effective or not."""
    def __init__(self, name):
        self.name = name
        if name == 'normal':
            self.double_damage_from = ['fighting']
            self.double_damage_to = []
            self.half_damage_from = []
            self.half_damage_to = ['rock', 'steel']
            self.no_damage_from = ['ghost']
            self.no_damage_to = ['ghost']
        elif name == 'fighting':
            self.double_damage_from = ['flying', 'psychic', 'fairy']
            self.double_damage_to = ['normal', 'rock', 'steel', 'ice', 'dark']
            self.half_damage_from = ['rock', 'bug', 'dark']
            self.half_damage_to = ['flying', 'poison', 'bug', 'psychic', 'fairy']
            self.no_damage_from = []
            self.no_damage_to = ['ghost']
        elif name == 'flying':
            self.double_damage_from = ['rock', 'electric', 'ice']
            self.double_damage_to = ['fighting', 'bug', 'grass']
            self.half_damage_from = ['fighting', 'bug', 'grass']
            self.half_damage_to = ['rock', 'steel', 'electric']
            self.no_damage_from = ['ground']
            self.no_damage_to = []
        elif name == 'poison':
            self.double_damage_from = ['ground', 'psychic']
            self.double_damage_to = ['grass', 'fairy']
            self.half_damage_from = ['fighting', 'poison', 'bug', 'grass', 'fairy']
            self.half_damage_to = ['poison', 'ground', 'rock', 'ghost']
            self.no_damage_from = []
            self.no_damage_to = ['steel']
        elif name == 'ground':
            self.double_damage_from = ['water', 'grass', 'ice']
            self.double_damage_to = ['poison', 'rock', 'steel', 'fire', 'electric']
            self.half_damage_from = ['poison', 'rock']
            self.half_damage_to = ['bug', 'grass']
            self.no_damage_from = ['electric']
            self.no_damage_to = ['flying']
        elif name == 'rock':
            self.double_damage_from = ['fighting', 'ground', 'steel', 'water', 'grass']
            self.double_damage_to = ['flying', 'bug', 'fire', 'ice']
            self.half_damage_from = ['normal', 'flying', 'poison', 'fire']
            self.half_damage_to = ['fighting', 'ground', 'steel']
            self.no_damage_from = []
            self.no_damage_to = []
        elif name == 'bug':
            self.double_damage_from = ['flying', 'rock', 'fire']
            self.double_damage_to = ['grass', 'psychic', 'dark']
            self.half_damage_from = ['fighting', 'ground', 'grass']
            self.half_damage_to = ['fighting', 'flying', 'poison', 'ghost', 'steel', 'fire', 'fairy']
            self.no_damage_from = []
            self.no_damage_to = []
        elif name == 'ghost':
            self.double_damage_from = ['ghost', 'dark']
            self.double_damage_to = ['ghost', 'psychic']
            self.half_damage_from = ['poison', 'bug']
            self.half_damage_to = ['dark']
            self.no_damage_from = ['normal', 'fighting']
            self.no_damage_to = ['normal']
        elif name == 'steel':
            self.double_damage_from = ['fighting', 'ground', 'fire']
            self.double_damage_to = ['rock', 'ice', 'fairy']
            self.half_damage_from = ['normal', 'flying', 'rock', 'bug', 'steel', 'grass', 'psychic', 'ice', 'dragon',
                                     'fairy']
            self.half_damage_to = ['steel', 'fire', 'water', 'electric']
            self.no_damage_from = ['poison']
            self.no_damage_to = []
        elif name == 'fire':
            self.double_damage_from = ['ground', 'rock', 'water']
            self.double_damage_to = ['bug', 'steel', 'grass', 'ice']
            self.half_damage_from = ['bug', 'steel', 'fire', 'grass', 'ice', 'fairy']
            self.half_damage_to = ['rock', 'fire', 'water', 'dragon']
            self.no_damage_from = []
            self.no_damage_to = []
        elif name == 'water':
            self.double_damage_from = ['grass', 'electric']
            self.double_damage_to = ['ground', 'rock', 'fire']
            self.half_damage_from = ['steel', 'fire', 'water', 'ice']
            self.half_damage_to = ['water', 'grass', 'dragon']
            self.no_damage_from = []
            self.no_damage_to = []
        elif name == 'grass':
            self.double_damage_from = ['flying', 'poison', 'bug', 'fire', 'ice']
            self.double_damage_to = ['ground', 'rock', 'water']
            self.half_damage_from = ['ground', 'water', 'grass', 'electric']
            self.half_damage_to = ['flying', 'poison', 'bug', 'steel', 'fire', 'grass', 'dragon']
            self.no_damage_from = []
            self.no_damage_to = []
        elif name == 'electric':
            self.double_damage_from = ['ground']
            self.double_damage_to = ['flying', 'water']
            self.half_damage_from = ['flying', 'steel', 'electric']
            self.half_damage_to = ['grass', 'electric', 'dragon']
            self.no_damage_from = []
            self.no_damage_to = ['ground']
        elif name == 'psychic':
            self.double_damage_from = ['bug', 'ghost', 'dark']
            self.double_damage_to = ['fighting', 'poison']
            self.half_damage_from = ['fighting', 'psychic']
            self.half_damage_to = ['steel', 'psychic']
            self.no_damage_from = []
            self.no_damage_to = ['dark']
        elif name == 'ice':
            self.double_damage_from = ['fighting', 'rock', 'steel', 'fire']
            self.double_damage_to = ['flying', 'ground', 'grass', 'dragon']
            self.half_damage_from = ['ice']
            self.half_damage_to = ['steel', 'fire', 'water', 'ice']
            self.no_damage_from = []
            self.no_damage_to = []
        elif name == 'dragon':
            self.double_damage_from = ['ice', 'dragon', 'fairy']
            self.double_damage_to = ['dragon']
            self.half_damage_from = ['fire', 'water', 'grass', 'electric']
            self.half_damage_to = ['steel']
            self.no_damage_from = []
            self.no_damage_to = ['fairy']
        elif name == 'dark':
            self.double_damage_from = ['fighting', 'bug', 'fairy']
            self.double_damage_to = ['ghost', 'psychic']
            self.half_damage_from = ['ghost', 'dark']
            self.half_damage_to = ['fighting', 'dark', 'fairy', 'psychic']
            self.no_damage_from = ['psychic']
            self.no_damage_to = []
        elif name == 'fairy':
            self.double_damage_from = ['poison', 'steel']
            self.double_damage_to = ['fighting', 'dragon', 'dark']
            self.half_damage_from = ['fighting', 'bug', 'dark']
            self.half_damage_to = ['poison', 'steel', 'fire']
            self.no_damage_from = ['dragon']
            self.no_damage_to = []
        elif name == 'stellar':
            self.double_damage_from = []
            self.double_damage_to = ['normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug', 'ghost',
                                     'steel', 'fire', 'water', 'grass', 'electric', 'psychic', 'ice', 'dragon', 'dark',
                                     'fairy']
            self.half_damage_from = ['normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug', 'ghost',
                                     'steel', 'fire', 'water', 'grass', 'electric', 'psychic', 'ice', 'dragon', 'dark',
                                     'fairy']
            self.half_damage_to = []
            self.no_damage_from = []
            self.no_damage_to = []
        # If no type matched the request, these values have to be set manually.
        # This gives the user the ability to create completely new types.
        else:
            self.double_damage_from = []
            self.double_damage_to = []
            self.half_damage_from = []
            self.half_damage_to = []
            self.no_damage_from = []
            self.no_damage_to = []
