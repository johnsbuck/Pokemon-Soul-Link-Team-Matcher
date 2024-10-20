"""Finds teams with Pokemon that each player want via regex search."""

import re
from typing import List
import argparse


SIZE_COUNT_REGEX_PATTERN = r"Team Size:.*\nTeam Count:.*\n\n"
GENERIC_TEAM_PATTERN = r"[a-z|A-Z|:|\||\n|\s|\d|-|']*"
END_TEAM_PATTERN = r"[a-z|A-Z|:|\||\n|\s|-|']*"
TEAM_END = r"\n\n"
EOP = "EOP---EOP"
EOM = "EOM--------------------------------EOM"


# pylint: disable=unused-argument
def blank_fn(*args, **kwargs) -> None:
    """Fill-in function for do nothing tasks.
    Uses args and kwargs to take in anything to be passed with no failure.
    """
    return


def get_player_picks() -> List[str]:
    """Gets pokemon that player wants for their team.

    Returns:
        List[str]: List of pokemon names
    """
    pokes = []

    text = ""
    text = input("Pokemon (none to stop): ")
    while text.lower() != "none":
        pokes.append(text)
        text = input("Pokemon (none to stop): ")

    return pokes


def get_regex(player: str, pokes: List[str]) -> str:
    """The regex for getting a player's possible Pokemons.

    Args:
        player (str): The name of the player.
        pokes (List[str]): The list of pokemon names.

    Returns:
        str: Regex pattern for searching for viable teams.
    """
    player_regex = rf"{player}\n"
    poke_regex = r"(?:" + r"|".join(x for x in pokes) + r")"
    return r"(" + player_regex + GENERIC_TEAM_PATTERN + GENERIC_TEAM_PATTERN.join(
        poke_regex for _ in pokes) + END_TEAM_PATTERN + TEAM_END + r")"


def script_prompt():
    """Prompt for getting information on players and their pokemon picks.
    """
    player = input("Player One: ")
    pokes = get_player_picks()

    regex = get_regex(player, pokes)

    player = input("Player Two (none to skip): ")
    two_players = False
    if player.lower() != "none":
        two_players = True
        regex += r"Team Size:.*\nTeam Count:.*\n\n"
        pokes = get_player_picks()
        regex += get_regex(player, pokes)

    get_output(regex, two_players)


def get_output(regex: str, multi_players: bool, filename: str = "test.txt",
               output_name: str = "search.txt", verbose: bool = True):
    """Outputs search results from filename to output_name. Prints results if verbose is true.

    Args:
        regex (str): The regex pattern being used to search the filename.
        multi_players (bool): Whether we are searching one or more players.
        filename (str, optional): The name of the input file. Defaults to "test.txt".
        output_name (str, optional): The name of the output file. Defaults to "search.txt".
        verbose (bool, optional): If true, we print the results. Defaults to True.
    """

    vprint = print
    if not verbose:
        vprint = blank_fn

    text = ""
    with open(filename, "r", encoding="utf-8") as f:
        text += f.read()

    vprint(regex)
    with open(output_name, "w+", encoding="utf-8") as f:
        for match in re.finditer(regex, text):
            vprint(match.group(1), end="")
            f.write(match.group(1))
            if multi_players:
                vprint(EOP)
                f.write(EOP)
                f.write("\n")

                vprint(match.group(2), end="")
                f.write(match.group(2))
            vprint(EOM)
            f.write(EOM)
            f.write("\n")
    vprint(regex)


def parse_args() -> argparse.ArgumentParser:
    """Creates the default parser for arguments.

    Returns:
        ArgumentParser: The argument parser with added arguments.
    """
    parser = argparse.ArgumentParser("")
    parser.add_argument("-p", "--playerpoke", nargs='+', action='append',
                        help="The name of the player and the pokemon they want in their team.")
    parser.add_argument("-f", "--filename", nargs=1, default="test.txt",
                        help="The input file for searching for viable teams.")
    parser.add_argument("-o", "--output", nargs=1, default="search.txt",
                        help="The output file for results found.")
    return parser.parse_args()


def main():
    """The main function
    """
    args = parse_args()
    print("Args")
    print(args.playerpoke)
    if not args.playerpoke:
        script_prompt()
        return

    regex = r""
    for i, player_args in enumerate(args.playerpoke):
        regex += get_regex(player_args[0], player_args[1:])
        if i < len(args.playerpoke) - 1:
            regex += SIZE_COUNT_REGEX_PATTERN

    get_output(regex, len(args.playerpoke) > 1)


if __name__ == "__main__":
    main()
