import csv
from typing import List
from pokemon import Pokemon
from soul_link_matcher import get_pokemon_teams, format_pokemon_team_pairs


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


def main():
    # Parse file to get Pokemon pairs
    test = parse_csv("pokemon.csv")
    
    # Get every Pokemon team with the Soul Link pairs
    test = get_pokemon_teams(test)

    # Print Team Options
    print(format_pokemon_team_pairs(test, "Ray", "Shen"))

if __name__ == "__main__":
    main()
