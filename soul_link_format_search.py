import re
from typing import List


def get_player_picks() -> List[str]:
    pokes = []
    
    text = ""
    text = input("Pokemon (none to stop): ")
    while text.lower() != "none":
        pokes.append(text)
        text = input("Pokemon (none to stop): ")

    return pokes


def get_regex(player: str, pokes: List[str]) -> str:
    GENERIC_TEAM_PATTERN = r"[a-z|A-Z|:|\||\n|\s|\d]*"
    END_TEAM_PATTERN = r"[a-z|A-Z|:|\||\n|\s]*"
    TEAM_END = r"\n\n"
    
    player_regex = r"%s\n" % player
    poke_regex = r"(?:" + r"|".join(x for x in pokes) + r")"
    return r"(" + player_regex + GENERIC_TEAM_PATTERN + GENERIC_TEAM_PATTERN.join(poke_regex for _ in pokes) + END_TEAM_PATTERN + TEAM_END + r")"


def main():
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
    
    
    text = ""
    with open("test.txt", "r") as f:
        text += f.read()
    
    print(regex)

    with open("search.txt", "w+") as f:
        for match in re.finditer(regex, text):
            print(match.group(1), end="")
            f.write(match.group(1))
            if two_players:
                print("EOP----EOP")
                f.write("EOP----EOP\n")
                f.write(match.group(2))
                print(match.group(2), end="")
            print("EOM--------------------------------EOM")
            f.write("EOM--------------------------------EOM\n")
    print(regex)


if __name__ == "__main__":
    main()