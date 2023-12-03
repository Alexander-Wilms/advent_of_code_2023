import pandas as pd
from pandas import DataFrame
from pprint import pprint
import re
import os


def solve_puzzle_part(file_name: str, part: int) -> int:
    with open(file_name) as f:
        data = f.readlines()
    with open(f"{file_name}.csv", "w") as f:
        for line in data:
            start_of_line = True
            for char in line:
                if char != "\n":
                    if not start_of_line:
                        f.write(",")
                    f.write(f"{char}")
                start_of_line = False
            f.write("\n")
    schematic: DataFrame = pd.read_csv(f"{file_name}.csv", header=None)
    os.remove(f"{file_name}.csv")
    pprint(schematic)

    schematic_size = schematic.shape
    pprint(schematic_size)

    adjacent_symbol_found = False
    current_part_number_string = ""
    current_part_number = -1
    numbers = {}
    count = 0
    for row in range(schematic_size[0]):
        for col in range(schematic_size[1]):
            cell = schematic.at[row, col]

            if re.match(r"\d", cell):
                print("checking ", end="")
                print(cell)
                current_part_number_string += cell

                for col_delta in [-1, 0, 1]:
                    for row_delta in [-1, 0, 1]:
                        # print(f"checking neighbor {row_delta},{col_delta} at {row+row_delta},{col+col_delta}:", end="")
                        try:
                            neighbor = schematic.at[row + row_delta, col + col_delta]
                            # print(neighbor)

                            if not re.match(r"[\d\.]", neighbor):
                                adjacent_symbol_found = True
                        except:
                            # print("inaccessible")
                            pass

                print(adjacent_symbol_found)

                number_complete = False

                try:
                    next_cell = schematic.at[row, col + 1]
                    if not re.match(r"\d", next_cell):
                        number_complete = True
                except:
                    # line break
                    number_complete = True

                if number_complete == True:
                    current_part_number = int(current_part_number_string)
                    current_part_number_string = ""
                    print(f"number complete: {current_part_number}")
                    print(f"{adjacent_symbol_found=}")

                    if current_part_number != -1:
                        numbers[count] = {}
                        numbers[count]["number"] = current_part_number
                        numbers[count]["is_part"] = adjacent_symbol_found
                        count += 1

                    adjacent_symbol_found = False

                    pprint(numbers)

        print()

    pprint(numbers)

    print()
    sum = 0
    for id in numbers.keys():
        if numbers[id]["is_part"]:
            sum += numbers[id]["number"]

    print(f"{sum=}")

    return sum


def test_solutions():
    sum = solve_puzzle_part("day_03/example_1.txt", 1)
    assert sum == 4361

    sum = solve_puzzle_part("day_03/input.txt", 1)
    print(sum)
    assert sum < 3361139
    assert sum > 306612
    assert sum == 509115


if __name__ == "__main__":
    test_solutions()
