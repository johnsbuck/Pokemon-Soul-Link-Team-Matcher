import re
from typing import List
import argparse


def blank_fn(*args, **kwargs):
    pass


def get_player_picks() -> List[str]:
    pokes = []
    
    text = ""
    text = input("Pokemon (none to stop): ")
    while text.lower() != "none":
        pokes.append(text)
        text = input("Pokemon (none to stop): ")

    return pokes


def get_regex(player: str, pokes: List[str]) -> str:
    GENERIC_TEAM_PATTERN = r"[a-z|A-Z|:|\||\n|\s|\d|-|']*"
    END_TEAM_PATTERN = r"[a-z|A-Z|:|\||\n|\s|-|']*"
    TEAM_END = r"\n\n"
    
    player_regex = r"%s\n" % player
    poke_regex = r"(?:" + r"|".join(x for x in pokes) + r")"
    return r"(" + player_regex + GENERIC_TEAM_PATTERN + GENERIC_TEAM_PATTERN.join(poke_regex for _ in pokes) + END_TEAM_PATTERN + TEAM_END + r")"


def script_prompt():
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


def get_output(regex: str, multi_players: bool, filename: str = "test.txt", output_name: str = "search.txt", verbose: bool = True):
    EOP = "EOP---EOP"
    EOM = "EOM--------------------------------EOM"
    
    vprint = print
    if not verbose:
        vprint = blank_fn
    
    text = ""
    with open(filename, "r") as f:
        text += f.read()
    
    vprint(regex)
    with open(output_name, "w+") as f:
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


def parse_args():
    parser = argparse.ArgumentParser("")
    parser.add_argument("-p", "--playerpoke", nargs='+', action='append')
    parser.add_argument("-f", "--filename", nargs=1, default="test.txt")
    parser.add_argument("-o", "--output", nargs=1, default="search.txt")
    return parser.parse_args()

def main():
    args = parse_args()
    print(args)
    if len(args.playerpoke) == 0:
        script_prompt()
        return
    
    SIZE_COUNT_REGEX_PATTERN = r"Team Size:.*\nTeam Count:.*\n\n"
    
    regex = r""
    for i in range(len(args.playerpoke)):
        regex += get_regex(args.playerpoke[i][0], args.playerpoke[i][1:])
        if i < len(args.playerpoke) - 1:
            regex += SIZE_COUNT_REGEX_PATTERN
    
    get_output(regex, len(args.playerpoke) > 1)
    

if __name__ == "__main__":
    main()