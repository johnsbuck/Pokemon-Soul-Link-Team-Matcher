from enum import Enum
from typing import List, Optional


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
