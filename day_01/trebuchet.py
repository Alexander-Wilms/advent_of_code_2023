import re
from pprint import pprint
from typing import List, Tuple


def solve_puzzle_part(input_file: str, part: int) -> Tuple[List[int], int]:
    calibration_values = list()
    sum = 0
    mapping = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}

    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            print(line)
            if part == 2:
                found_spelled_out_numbers = {}
                for key in mapping.keys():
                    # print(f"searching for '{key}' in '{line}'")
                    index = line.find(key)
                    # print(f"index: {index}")
                    if index != -1:
                        found_spelled_out_numbers[index] = key
                if found_spelled_out_numbers:
                    pprint(found_spelled_out_numbers)
                    # for key, val in found_spelled_out_numbers.items():
                    first = sorted(list(found_spelled_out_numbers.keys()))[0]
                    first_part = line[0:first]
                    second_part = mapping[found_spelled_out_numbers[first]]
                    third_part = line[first + len(found_spelled_out_numbers[first]) :]

                    print(f"{first_part=}")
                    print(f"{second_part=}")
                    print(f"{third_part=}")
                    line = first_part + second_part + third_part

                print(f"replaced first: {line}")

                found_spelled_out_numbers = {}
                for key in mapping.keys():
                    # print(f"searching for '{key}' in '{line}'")
                    index = line.find(key)
                    # print(f"index: {index}")
                    if index != -1:
                        found_spelled_out_numbers[index] = key
                if found_spelled_out_numbers:
                    pprint(found_spelled_out_numbers)
                    # for key, val in found_spelled_out_numbers.items():
                    first = sorted(list(found_spelled_out_numbers.keys()))[-1]
                    first_part = line[0:first]
                    second_part = mapping[found_spelled_out_numbers[first]]
                    third_part = line[first + len(found_spelled_out_numbers[first]) :]

                    print(f"{first_part=}")
                    print(f"{second_part=}")
                    print(f"{third_part=}")
                    line = first_part + second_part + third_part

                    print(line)
                print(f"replaced second: {line}")
            digits = re.findall(r"\d", line)
            pprint(digits)
            calibration_value = int(f"{digits[0]}{digits[-1]}")
            print(calibration_value)
            calibration_values.append(calibration_value)
            sum += calibration_value
            print()

    pprint(calibration_values)
    print(sum)
    print("---")
    return (calibration_values, sum)


calibration_values, sum = solve_puzzle_part("day_01/example.txt", 1)
assert calibration_values == [12, 38, 15, 77]
assert sum == 142

calibration_values, sum = solve_puzzle_part("day_01/input.txt", 1)
assert sum == 55130

calibration_values, sum = solve_puzzle_part("day_01/example_2.txt", 2)
assert calibration_values == [29, 83, 13, 24, 42, 14, 76]
assert sum == 281

calibration_values, sum = solve_puzzle_part("day_01/input.txt", 2)
pprint(calibration_values)
assert sum < 54999
assert sum < 54996
