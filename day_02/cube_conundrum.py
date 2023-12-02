import re
from pprint import pprint
from typing import Dict


def get_cube_counts(line: str, color: str) -> list[int]:
    matches = re.findall(r"\d* " + color, line)
    for index in range(0, len(matches)):
        matches[index] = int(re.findall(r"\d*", matches[index])[0])

    pprint(matches)
    return matches


def solve_puzzle_part(file_name: str, part: int) -> int:
    games: Dict[int, Dict[str, list[int]]] = {}

    cubes_in_bag = {"red": 12, "green": 13, "blue": 14}

    with open(file_name) as f:
        for line in f.readlines():
            line = line.strip()
            print(line)
            game_id_string = re.findall(r"Game \d*", line)[0]
            game_id = int(re.findall(r"\d+", game_id_string)[0])
            print(f"{game_id=}")
            games[game_id] = {}
            for color in cubes_in_bag.keys():
                games[game_id][color] = get_cube_counts(line, color)

    pprint(games)

    sum_of_id_of_games_with_valid_number_of_balls = 0

    sum_of_powers = 0
    for game_id in games.keys():
        print(f"Checking game {game_id}")
        possible = True
        power = 1
        for color in cubes_in_bag.keys():
            print(f"\tChecking color {color}")
            max_number_of_current_color = max(games[game_id][color])
            power *= max_number_of_current_color
            if max_number_of_current_color <= cubes_in_bag[color]:
                print("\t\tthis number of this color is possible")
            else:
                print("\t\tthis number of this color is impossible")
                possible = False
        print(f"{power=}")
        sum_of_powers += power
        if possible:
            sum_of_id_of_games_with_valid_number_of_balls += game_id

    if part == 1:
        print(f"{sum_of_id_of_games_with_valid_number_of_balls=}")
        return sum_of_id_of_games_with_valid_number_of_balls
    else:
        print(f"{sum_of_powers=}")
        return sum_of_powers


def test_solutions():
    sum = solve_puzzle_part("day_02/example_1.txt", 1)
    assert sum == 8
    sum = solve_puzzle_part("day_02/input.txt", 1)
    assert sum == 2176
    sum = solve_puzzle_part("day_02/example_1.txt", 2)
    assert sum == 2286
    sum = solve_puzzle_part("day_02/input.txt", 2)
    assert sum == 63700


if __name__ == "__main__":
    test_solutions()
