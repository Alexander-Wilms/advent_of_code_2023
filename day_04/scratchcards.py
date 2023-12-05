import re
from pprint import pprint


def get_id(line: str) -> int:
    card_number = int(re.findall(r"\d+", line.split(":")[0])[0])
    return card_number


def solve_puzzle_part(file_name: str, part: int) -> int:
    with open(file_name) as f:
        sum_of_points = 0
        scratchcards = {}
        for line in f.readlines():
            line = line.strip()
            print(line)
            card_number = get_id(line)
            all_numbers_string = line.split(":")[1]
            winning_numbers_string = all_numbers_string.split("|")[0]
            my_numbers_string = all_numbers_string.split("|")[1]
            # print(winning_numbers_string)
            # print(my_numbers_string)
            winning_numbers = re.findall(r"\d+", winning_numbers_string)
            my_numbers = re.findall(r"\d+", my_numbers_string)
            # pprint(winning_numbers)
            # pprint(my_numbers)
            winning_numbers = [int(winning_numbers[i]) for i in range(len(winning_numbers))]
            my_numbers = [int(my_numbers[i]) for i in range(len(my_numbers))]
            pprint(winning_numbers)
            pprint(my_numbers)
            matches = set(winning_numbers).intersection(set(my_numbers))
            print(f"{matches=}")
            number_of_matches = len(matches)
            print(f"{number_of_matches=}")
            if part == 1:
                points = int(2 ** (number_of_matches - 1))
                print(f"{points=}")
                sum_of_points += points
            else:
                scratchcards[card_number] = {}
                scratchcards[card_number]["copies"] = 1
                scratchcards[card_number]["number_of_matches"] = number_of_matches
                scratchcards[card_number]["winning_numbers"] = winning_numbers
                scratchcards[card_number]["my_numbers"] = my_numbers

    if part == 1:
        print(f"{sum_of_points=}")
        return sum_of_points
    else:
        for id, scratchcard in scratchcards.items():
            pprint(scratchcards)
            print(f"Card {id} has {scratchcard['number_of_matches']} matching numbers, so you win one copy each of the next {scratchcard['number_of_matches']} cards: ")
            for i in range(scratchcard["number_of_matches"]):
                print(f"trying to increment scratchcards[{id+i+1}][copies]")
                scratchcards[id + i + 1]["copies"] += scratchcard["copies"]
                print(id + i + 1, end="")
            print()

        number_of_scratchcards = 0
        for id, scratchcard in scratchcards.items():
            number_of_scratchcards += scratchcard["copies"]
        print(f"{number_of_scratchcards=}")
        return number_of_scratchcards


def test_solutions():
    sum = solve_puzzle_part("day_04/example_1.txt", 1)
    assert sum == 13

    sum = solve_puzzle_part("day_04/input.txt", 1)
    assert sum == 18519

    sum = solve_puzzle_part("day_04/example_1.txt", 2)
    assert sum == 30

    sum = solve_puzzle_part("day_04/input.txt", 2)
    assert sum == 11787590


if __name__ == "__main__":
    test_solutions()
