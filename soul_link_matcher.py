from typing import List, Set
from pokemon import Pokemon, PokemonTeam, PokemonType


def get_pokemon_teams(pairs: List[List[Pokemon]]) -> List[List[PokemonTeam]]:
    """Returns all unique pokemon teams.

    Args:
        pairs (List[List[Pokemon]]): The initial list of Pokemon pairs used for the Soul Link challenge.

    Returns:
        List[List[PokemonTeam]]: The list of all unique pokemon teams separated by the two teams.
    """
    type_set = set([])
    return _helper(pairs, 0, [], [], type_set, [])


def _helper(pairs: List[List[Pokemon]], idx: int, x: List[Pokemon], y: List[Pokemon], type_set: Set[PokemonType], team_pairs: List[List[PokemonTeam]]) -> List[List[PokemonTeam]]:
    """A _helper function for get_pokemon_teams.

    Args:
        pairs (List[List[Pokemon]]): The initial list of Pokemon pairs used for the Soul Link challenge. 
        idx (int): The initial index to start or continue searching the pairs list. 
        x (List[Pokemon]): The current team of Pokemon for the first player.
        y (List[Pokemon]): The current team of Pokemon for the second player.
        type_set (Set[PokemonType]): The set of currently used Pokemon types.
        team_pairs (List[List[PokemonTeam]]): The output of all unique Pokemon teams per player. Referenced for use and checking if a team is already used in some capacity.

    Returns:
        List[List[PokemonTeam]]: The output of all unique Pokemon teams per player.
    """
    # Check if we have a full team or are at the end of the pairs.
    if (len(x) == PokemonTeam.MAX_POKEMON or idx == len(pairs)) and _is_team_unique(x, team_pairs, 0) and _is_team_unique(y, team_pairs, 1):
        team_pairs.append([PokemonTeam(x), PokemonTeam(y)])
        return team_pairs

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
        _helper(pairs, i+1, x, y, type_set, team_pairs)

        # Remove types and pokemon to check for other pairs.
        type_set -= types
        x.pop()
        y.pop()
    
    # If there is no way to add more pokemon with our current setup, add the current roster.
    if not found_addition and len(x) > 0 and _is_team_unique(x, team_pairs, 0) and _is_team_unique(y, team_pairs, 1):
        team_pairs.append([PokemonTeam(x), PokemonTeam(y)])

    return team_pairs

def _is_team_unique(x: PokemonTeam, team_pairs: List[List[PokemonTeam]], idx: int) -> bool:
    """Checks if a given pokemon team is not a sub-team of an already existing team.

    Args:
        x (PokemonTeam): The pokemon team we are testing for its uniqueness.
        team_pairs (List[List[PokemonTeam]]): The list of teams that we are pulling from.
        idx (int): The specific index for the team_pairs that we wish to use (i.e. 1 or 2)

    Returns:
        bool: Is the pokemon team (x) unique among the other generated teams?
    """
    check = set(x)
    for pair in team_pairs:
        temp = set(pair[idx]._team)
        if len(check - temp) == 0:
            return False
    return True

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
