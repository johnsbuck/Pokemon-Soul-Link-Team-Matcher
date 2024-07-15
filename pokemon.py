from _collections_abc import MutableSequence
from enum import Enum
from typing import List, Optional, Generator, override


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


class PokemonTeam(MutableSequence):
    MAX_POKEMON = 6
    ADD_SIZE_ERROR = ValueError("Team is at maximum size of 6. Cannot add any more Pokemon to team.")
    
    def __init__(self, team: Optional[List[Pokemon]] = None) -> None:
        self._team = []
        if team is not None:
            self._init_team(team)
            
    def _init_team(self, team: List[Pokemon]) -> None:
        if len(team) > PokemonTeam.MAX_POKEMON:
            raise ValueError("Given list of Pokemon is more than team size.")
        if any(type(x) is not Pokemon for x in team):
            raise ValueError("Not all values in list are Pokemon.")
        self._team = team[:]
    
    @override
    def append(self, value: Pokemon) -> None:
        if self.is_max_team():
            raise PokemonTeam.ADD_SIZE_ERROR
        self._team.append(value)
    
    @override
    def insert(self, idx: int, value: Pokemon) -> None:
        if self.is_max_team():
            raise PokemonTeam.ADD_SIZE_ERROR
        self._team.insert(idx, value)

    def is_max_team(self) -> bool:
        return self.__len__() == PokemonTeam.MAX_POKEMON

    @override
    def __iter__(self) -> Generator:
        yield from self._team
    
    @override
    def __getitem__(self, key):
        if isinstance(key, int):
            return self._team[key]
        return self.__class__(self._team.__getitem__(key))
    
    @override
    def __setitem__(self, key, value: Pokemon) -> None:
        self._team.__setitem__(key, value)
    
    @override
    def  __delitem__(self, key: Pokemon) -> None:
        self._team.__delitem__(key)
    
    @override
    def __len__(self) -> int:
        return len(self._team)
    
    @override
    def __str__(self) -> str:
        output = "Team Size: " + str(len(self._team)) + '\n'
        for poke in self._team:
            output += '\t' + str(poke) + '\n'

        for i in range(PokemonTeam.MAX_POKEMON - len(self._team)):
            output += "\tempty\n"

        return output
    
    @override
    def __repr__(self) -> str:
        return self.__str__()
