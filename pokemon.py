from _collections_abc import MutableSequence
from enum import Enum
from typing import List, Optional, Generator, override, TypeVar, Iterator, Generic


class PokemonType(Enum):
    Normal = 0
    Fighting = 1
    Flying = 2
    Poison = 3
    Ground = 4
    Rock = 5
    Bug = 6
    Ghost = 7
    Steel = 8
    Fire = 9
    Water = 10
    Grass = 11
    Electric = 12
    Psychic = 13
    Ice = 14
    Dragon = 15
    Dark = 16
    Fairy = 17

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Pokemon:
    """Pokemon data class
    """

    def __init__(self, name: str, poke_type: str | PokemonType) -> None:
        self.name = name
        self.poke_type = poke_type

    @property
    def name(self) -> str:
        """The name of the Pokemon

        Returns:
            str: Pokemon's name.
        """
        return self._name

    @name.setter
    def name(self, val: str) -> None:
        self._name = val

    @property
    def poke_type(self) -> PokemonType:
        """Type of the Pokemon.

        Returns:
            PokemonType: Pokemon's type.
        """
        return self._poke_type

    @poke_type.setter
    def poke_type(self, val: str | PokemonType) -> None:
        try:
            temp = PokemonType[val]
            self._poke_type = temp
        except ValueError as e:
            raise ValueError("Invalid PokemonType", val) from e

    def __str__(self) -> str:
        return self.name + ": " + str(self.poke_type)

    def __repr__(self) -> str:
        return self.__str__()


T = TypeVar("T")


class Team(MutableSequence, Generic[T]):
    """A mutuable sequence of max length 6, that can be used for reviewing Pokemon.
    """
    MAX_POKEMON = 6
    ADD_SIZE_ERROR = ValueError(
        "Team is at maximum size of 6. Cannot add any more Pokemon to team.")

    def __init__(self, team: Optional[List] = None) -> None:
        self._team = []
        if team is not None:
            self._init_team(team)

    @classmethod
    def from_iterator(cls, team: Iterator[T]) -> "Team":
        """Generates a Team object from an iterator

        Args:
            team (Iterator): An interator

        Returns:
            Team: _description_
        """
        check_team = list(team)
        if len(check_team) > Team.MAX_POKEMON:
            raise ValueError("Given list of Pokemon is more than team size.")
        return cls(check_team)

    def _init_team(self, team: List[T]) -> None:
        if len(team) > Team.MAX_POKEMON:
            raise ValueError("Given list of Pokemon is more than team size.")
        self._team = team[:]

    @override
    def append(self, value: T) -> None:
        if self.is_max_team():
            raise Team.ADD_SIZE_ERROR
        self._team.append(value)

    @override
    def insert(self, index: int, value: T) -> None:
        if self.is_max_team():
            raise Team.ADD_SIZE_ERROR
        self._team.insert(index, value)

    def is_max_team(self) -> bool:
        """Checks if the team at its maximum length.

        Returns:
            bool: If team is at maximum length, return True. Otherwise False.
        """
        return len(self) == Team.MAX_POKEMON

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
    def __delitem__(self, key: Pokemon) -> None:
        self._team.__delitem__(key)

    @override
    def __len__(self) -> int:
        return len(self._team)

    @override
    def __str__(self) -> str:
        output = "Team Size: " + str(len(self._team)) + '\n'
        for poke in self._team:
            output += '\t' + str(poke) + '\n'

        for _ in range(Team.MAX_POKEMON - len(self._team)):
            output += "\tempty\n"

        return output

    @override
    def __repr__(self) -> str:
        return self.__str__()
