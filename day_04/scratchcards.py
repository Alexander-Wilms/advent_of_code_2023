from pprint import pprint
import re


def solve_puzzle_part(file_name: str, part: int) -> int:
    with open(file_name) as f:
        sum_of_points = 0
        for line in f.readlines():
            line = line.strip()
            print(line)
            all_numbers_string = line.split(":")[1]
            winning_numbers_string = all_numbers_string.split("|")[0]
            my_numbers_string = all_numbers_string.split("|")[1]
            # print(winning_numbers_string)
            # print(my_numbers_string)
            winning_numbers = re.findall(r"\d+", winning_numbers_string)
            my_numbers = re.findall(r"\d+", my_numbers_string)
            # pprint(winning_numbers)
            # pprint(my_numbers)
            winning_numbers = [
                int(winning_numbers[i]) for i in range(len(winning_numbers))
            ]
            my_numbers = [int(my_numbers[i]) for i in range(len(my_numbers))]
            pprint(winning_numbers)
            pprint(my_numbers)
            matches = set(winning_numbers).intersection(set(my_numbers))
            print(f"{matches=}")
            number_of_matches = len(matches)
            print(f"{number_of_matches=}")
            points = int(2 ** (number_of_matches - 1))
            print(f"{points=}")
            sum_of_points += points
    print(f"{sum_of_points=}")
    return sum_of_points


def test_solutions():
    sum = solve_puzzle_part("day_04/example_1.txt", 1)
    assert sum == 13

    sum = solve_puzzle_part("day_04/input.txt", 1)
    assert sum == 18519


if __name__ == "__main__":
    test_solutions()
