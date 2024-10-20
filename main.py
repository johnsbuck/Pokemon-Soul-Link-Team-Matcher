"""Main program for Pokemon Souls Link matcher."""

import csv
from typing import List
from pokemon import Pokemon
from soul_link_matcher import get_pokemon_teams_by_type, format_pokemon_team_pairs_by_type


def parse_csv(file: str, header: bool = False) -> List[List[str]]:
    """Parses csv containing Pokemon pairs with typing.

    Args:
        file (str): File name
        header (bool, optional): Boolean for determining if there is a header. Defaults to False.

    Returns:
        List[List[str]]: _description_
    """
    output = []
    with open(file, 'r+', encoding="utf-8") as f:
        reader = csv.reader(f)
        for line in reader:
            if header:
                header = False
                continue
            output.append([Pokemon(line[0], line[1]),
                          Pokemon(line[2], line[3])])
    return output


def main():
    """Main function
    """
    # Parse file to get Pokemon pairs
    test = parse_csv("pokemon.csv")

    # Get every Pokemon team with the Soul Link pairs
    test = get_pokemon_teams_by_type(test)

    # Print Team Options
    text = format_pokemon_team_pairs_by_type(test, "Ray", "Shen")
    print(text)

    with open("test.txt", "w+", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    main()
