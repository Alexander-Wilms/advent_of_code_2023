import pandas as pd
from pandas import DataFrame
from pprint import pprint
import re
import os


def solve_puzzle_part(file_name: str, part: int) -> int:
    # add commas between values so we can use pd.read_csv() and
    # nicely display the schematic as a DataFrame
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

    # iterate over all cells of the schematic
    for row in range(schematic_size[0]):
        for col in range(schematic_size[1]):
            cell = schematic.at[row, col]

            if re.match(r"\d", cell):
                print("checking ", end="")
                print(cell)
                current_part_number_string += cell

                # iterate over all neighbors
                for col_delta in [-1, 0, 1]:
                    for row_delta in [-1, 0, 1]:
                        # print(f"checking neighbor {row_delta},{col_delta} at {row+row_delta},{col+col_delta}:", end="")
                        try:
                            neighbor = schematic.at[row + row_delta, col + col_delta]
                            # print(neighbor)

                            if not re.match(r"[\d\.]", neighbor):
                                adjacent_symbol_found = True

                            if re.match(r"\*", neighbor):
                                adjacent_gear_found = True
                                gear_row = row + row_delta
                                gear_col = col + col_delta
                        except Exception:
                            # print("inaccessible")
                            pass

                print(adjacent_symbol_found)

                # check if we've read the complete number
                number_complete = False

                try:
                    next_cell = schematic.at[row, col + 1]
                    if not re.match(r"\d", next_cell):
                        number_complete = True
                except Exception:
                    # line break
                    number_complete = True

                if number_complete:
                    current_part_number = int(current_part_number_string)
                    current_part_number_string = ""
                    print(f"number complete: {current_part_number}")
                    print(f"{adjacent_symbol_found=}")

                    if current_part_number != -1:
                        numbers[count] = {}
                        numbers[count]["number"] = current_part_number
                        numbers[count]["is_part"] = adjacent_symbol_found
                        numbers[count]["touches_gear"] = adjacent_gear_found
                        if adjacent_gear_found:
                            numbers[count]["gear_row"] = gear_row
                            numbers[count]["gear_col"] = gear_col
                        count += 1

                    adjacent_symbol_found = False
                    adjacent_gear_found = False

                    # pprint(numbers)

        print()

    pprint(numbers)

    print()
    sum_of_part_numbers = 0
    sum_of_gear_ratios = 0
    # use list() to copy keys, since we delete dict entries during the loop
    # https://stackoverflow.com/a/11941855/2278742
    for id in list(numbers.keys()):
        if id not in numbers.keys():
            continue

        if part == 1:
            if numbers[id]["is_part"]:
                sum_of_part_numbers += numbers[id]["number"]

        if part == 2:
            if numbers[id]["touches_gear"]:
                gear_1 = numbers[id]["number"]
                gear_2 = 0
                # use list() to copy keys, since we delete dict entries during the loop
                for id_potential_second_gear in list(numbers.keys()):
                    if numbers[id_potential_second_gear]["touches_gear"]:
                        if id_potential_second_gear != id:
                            if (
                                numbers[id_potential_second_gear]["gear_col"]
                                == numbers[id]["gear_col"]
                                and numbers[id_potential_second_gear]["gear_row"]
                                == numbers[id]["gear_row"]
                            ):
                                gear_2 = numbers[id_potential_second_gear]["number"]
                                numbers.pop(id_potential_second_gear)
                gear_ratio = gear_1 * gear_2
                sum_of_gear_ratios += gear_ratio

    if part == 1:
        print(f"{sum_of_part_numbers=}")
        return sum_of_part_numbers
    else:
        print(f"{sum_of_gear_ratios=}")
        return sum_of_gear_ratios


def test_solutions():
    sum = solve_puzzle_part("day_03/example_1.txt", 1)
    assert sum == 4361

    sum = solve_puzzle_part("day_03/input.txt", 1)
    assert sum < 3361139
    assert sum > 306612
    assert sum == 509115

    sum = solve_puzzle_part("day_03/example_1.txt", 2)
    assert sum == 467835

    sum = solve_puzzle_part("day_03/input.txt", 2)
    assert sum == 75220503


if __name__ == "__main__":
    test_solutions()
