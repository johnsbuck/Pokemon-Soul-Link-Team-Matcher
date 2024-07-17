from typing import List, Set, Annotated
from pokemon import Pokemon, PokemonTeam, PokemonType


PokemonPair = Annotated[List[Pokemon], 2]


def get_pokemon_teams(pairs: List[PokemonPair]) -> List[List[PokemonTeam]]:
    """Returns all unique pokemon teams.

    Args:
        pairs (List[List[Pokemon]]): The initial list of Pokemon pairs used for the Soul Link challenge.

    Returns:
        List[List[PokemonTeam]]: The list of all unique pokemon teams separated by the two teams.
    """
    type_set = set([])
    return _helper(pairs, 0, PokemonTeam(), PokemonTeam(), type_set, [])


def _helper(pairs: List[PokemonPair], idx: int, x: PokemonTeam, y: PokemonTeam, type_set: Set[PokemonType], team_pairs: List[List[PokemonTeam]]) -> List[List[PokemonTeam]]:
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
    if len(x) == PokemonTeam.MAX_POKEMON or idx == len(pairs):
        if _is_team_unique(x, team_pairs, 0) and _is_team_unique(y, team_pairs, 1):
            team_pairs.append([x[:], y[:]])
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
        team_pairs.append([x[:], y[:]])

    return team_pairs


def _is_team_unique(x: PokemonTeam | List[PokemonType], team_pairs: List[List[PokemonTeam]] | List[List[List[PokemonType]]], idx: int) -> bool:
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
        if len(check - set(pair[idx])) == 0:
            return False
    return True


def format_pokemon_team_pairs(team_pairs: List[List[PokemonTeam]], p1_name: str = "Team 1", p2_name: str = "Team 2", min_size: int = 0) -> str:
    if len(team_pairs) == 0:
        return ""
    
    team_pairs.sort(key=lambda x: len(x[0]), reverse=True)
    size = len(team_pairs[0][0])
    count = 0
    names = [p1_name, p2_name]
    
    output = "Pokemon Team Sizes: " + str(size) + "\n"
    output += "================================================================\n"
    
    for pair in team_pairs:
        curr = len(pair[0])
        if size != curr:
            output += "Total Count: " + str(count) + "\n"
            output += "--------------------------------\n"

            size = curr
            count = 0
            
            if size < min_size:
                return output

            output += "Pokemon Team Sizes: " + str(size) + "\n"
            output += "================================================================\n"
        count += 1
        for i in range(len(pair)):
            output += names[i] + "\n"
            output += str(pair[i]) + "\n"
        output += "--------------------------------\n"
    output += "Total Count: " + str(count) + "\n"
    output += "--------------------------------\n"
    return output


def get_pokemon_teams_by_type(pairs: List[PokemonPair]) -> List[List[List[List[Pokemon]]]]:
    types = [[[] for _ in range(len(PokemonType))] for _ in range(len(PokemonType))]
    for pair in pairs:
        types[pair[0].type.value][pair[1].type.value].append(pair)
    type_set = set([])
    type_listings = _helper_by_type(types, 0, [], [], type_set, [])
    output = []
    for team_pair in type_listings:
        output.append([[list(zip(*types[team_pair[0][i].value][team_pair[1][i].value]))[0] for i in range(len(team_pair[0]))],
                        [list(zip(*types[team_pair[0][i].value][team_pair[1][i].value]))[1] for i in range(len(team_pair[0]))]])
    return output


def _helper_by_type(type_grid: List[List[PokemonPair]], idx: int, x: List[PokemonType], y: List[PokemonType], type_set: Set[PokemonType], team_pairs: List[List[List[PokemonType]]]) -> List[List[List[PokemonType]]]:
    if len(x) == PokemonTeam.MAX_POKEMON or idx == len(type_grid):
        if _is_team_pair_unique(x, y, team_pairs):
            team_pairs.append([x[:], y[:]])
        return team_pairs
    
    found_addition = False
    for i in range(idx, len(PokemonType)):
        x_type = PokemonType(i)
        if x_type in type_set:
            continue
        for y_type in PokemonType:
            if x_type == y_type or y_type in type_set or len(type_grid[x_type.value][y_type.value]) == 0:
                continue
            found_addition = True

            type_set.add(x_type)
            type_set.add(y_type)
            x.append(x_type)
            y.append(y_type)
            
            _helper_by_type(type_grid, i+1, x, y, type_set, team_pairs)
            
            x.pop()
            y.pop()
            type_set.discard(x_type)
            type_set.discard(y_type)
            
    if not found_addition and len(x) > 0 and _is_team_pair_unique(x, y, team_pairs):
        team_pairs.append([x[:], y[:]])
        
    return team_pairs


def _is_team_pair_unique(x: List[PokemonType], y: List[PokemonType], team_pairs: List[List[List[PokemonType]]]) -> bool:
    """Checks if a given pokemon team is not a sub-team of an already existing team.

    Args:
        x (List[PokemonType]): Player 1's pokemon team types we are testing for its uniqueness.
        y (List[PokemonType]): Player 2's pokemon team types we are testing for its uniqueness.
        team_pairs (List[List[List[PokemonType]]]): The list of team types that we are pulling from.

    Returns:
        bool: Are the pokemon teams unique among the other generated teams?
    """
    check = set((a, b) for a, b in zip(x, y))
    for pair in team_pairs:
        if len(check - set(zip(*pair))) == 0:
            return False
    return True


def format_pokemon_team_pairs_by_type(team_pairs: List[List[List[List[Pokemon]]]], p1_name: str = "Ray", p2_name: str = "Shen", min_size: int = 0, pokemon_name_width: int = 10, type_name_width: int = 8) -> str:
    if len(team_pairs) == 0:
        return ""
    
    team_pairs.sort(key=lambda x: len(x[0]), reverse=True)
    size = len(team_pairs[0][0])
    count = 0
    names = [p1_name, p2_name]
    
    output = "Pokemon Team Sizes: " + str(size) + "\n"
    output += "================================================================\n"
    
    for pair in team_pairs:
        curr = len(pair[0])
        if size != curr:
            output += "Total Count: " + str(count) + "\n"
            output += "--------------------------------\n"

            size = curr
            count = 0
            
            if size < min_size:
                return output

            output += "Pokemon Team Sizes: " + str(size) + "\n"
            output += "================================================================\n"
        team_count = 1
        
        # Create strings of each team pair
        for i in range(len(pair)):
            output += names[i] + "\n"
            for x in pair[i]:
                # List each pokemon that match the type pair
                output += ("%-*s" % (type_name_width, x[0].type)) + ": "
                output += " | ".join("%-*s" % (pokemon_name_width, poke.name) for poke in x) + "\n"

                # Team sizes are the same, but need to be matched. Only look at one team.
                if i == 0:
                    team_count *= len(x)
            output += "\n"
            output += "Team Size: " + str(size) + "\n"
            output += "Team Count: " + str(team_count) + "\n\n"
        count += team_count
        output += "--------------------------------\n"
    output += "Total Count: " + str(count) + "\n"
    output += "--------------------------------\n"
    return output
        