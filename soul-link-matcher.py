import csv
from enum import Enum
from typing import List, Optional, Set


class PokemonType(Enum):
    Normal = 1
    Fighting = 2
    Flying = 3
    Poison = 4
    Ground = 5
    Rock = 6
    Bug = 7
    Ghost = 8
    Steel = 9
    Fire = 10
    Water = 11
    Grass = 12
    Electric = 13
    Psychic = 14
    Ice = 15
    Dragon = 16
    Dark = 17
    Fairy = 18
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()


class Pokemon:
    def __init__(self, name: str, type: str | PokemonType) -> None:
        self.name = name
        self.type = type

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, val: str) -> None:
        self._name = val

    @property
    def type(self) -> PokemonType:
        return self._type
    
    @type.setter
    def type(self, val: str | PokemonType) -> None:
        try:
            temp = PokemonType[val]
            self._type = temp
        except ValueError:
            raise ValueError("Invalid PokemonType", val)

    def __str__(self) -> str:
        return self.name + ": " + str(self.type)

    def __repr__(self) -> str:
        return self.__str__()


class PokemonTeam():
    MAX_POKEMON = 6
    
    def __init__(self, team: Optional[List[Pokemon]] = None) -> None:
        self._team = []
        if team is not None:
            self._team = team[:]
    
    def append(self, value: Pokemon) -> None:
        if len(self) == PokemonTeam.MAX_POKEMON:
            raise ValueError("Max number of Pokemon is 6")
        self._team.append(value)
        
    def __len__(self) -> int:
        return len(self._team)
    
    def __str__(self) -> str:
        output = "Team Size: " + str(len(self._team)) + '\n'
        for poke in self._team:
            output += '\t' + str(poke) + '\n'

        for i in range(PokemonTeam.MAX_POKEMON - len(self._team)):
            output += "\tempty\n"

        return output
    
    def __repr__(self) -> str:
        return self.__str__()


def parse_csv(file: str, header: bool = False) -> List[List[str]]:
    output = []
    with open(file, 'r+') as f:
        reader = csv.reader(f)
        for line in reader:
            if header:
                header = False
                continue
            output.append([Pokemon(line[0], line[1]), Pokemon(line[2], line[3])])
    return output


def get_pokemon_teams(pairs: List[List[Pokemon]]) -> List[List[PokemonTeam]]:
    type_set = set([])
    return helper(pairs, 0, [], [], type_set)


def helper(pairs: List[List[Pokemon]], idx: int, x: List[Pokemon], y: List[Pokemon], type_set: Set[PokemonType]) -> List[List[PokemonTeam]]:
    output = []

    # Check if we have a full team or are at the end of the pairs.
    if len(x) == PokemonTeam.MAX_POKEMON or idx == len(pairs):
        output.append([PokemonTeam(x), PokemonTeam(y)])
        return output

    # Search through each pair for a typing that wasn't used.
    found_addition = False
    for i in range(idx, len(pairs)):
        # Check if the types are already used.
        types = set([pairs[i][0].type, pairs[i][1].type])
        if len(types - type_set) != len(types):
            continue

        # Found a new Pokemon. Add to teams and type set.
        found_addition = True
        x.append(pairs[i][0])
        y.append(pairs[i][1])
        type_set = type_set.union(types)

        # Check for more Pokemon to add to teams.
        output += helper(pairs, i+1, x, y, type_set)

        # Remove types and pokemon to check for other pairs.
        type_set -= types
        x.pop()
        y.pop()
    
    # If there is no way to add more pokemon with our current setup, add the current roster.
    if not found_addition and len(x) > 0:
        output.append([PokemonTeam(x), PokemonTeam(y)])

    return output


def format_pokemon_team_pairs(team_pairs: List[List[PokemonTeam]], p1_name: str = "Team 1", p2_name: str = "Team 2") -> str:
    if len(team_pairs) == 0:
        return ""
    
    team_pairs.sort(key=lambda x: len(x[0]), reverse=True)
    size = len(team_pairs[0][0])
    names = [p1_name, p2_name]
    
    output = "Pokemon Team Sizes: " + str(size) + "\n"
    output += "================================================================\n"
    
    for pair in team_pairs:
        curr = len(pair[0])
        if size != curr:
            size = curr
            output += "Pokemon Team Sizes: " + str(size) + "\n"
            output += "================================================================\n"
        for i in range(len(pair)):
            output += names[i] + "\n"
            output += str(pair[i]) + "\n"
        output += "--------------------------------\n"
    return output


def main():
    # Parse file to get Pokemon pairs
    test = parse_csv("pokemon.csv")
    
    # Get every Pokemon team with the Soul Link pairs
    test = get_pokemon_teams(test)
    
    # Print Team Options
    print(format_pokemon_team_pairs(test, "Ray", "Shen"))
    

if __name__ == "__main__":
    main()
