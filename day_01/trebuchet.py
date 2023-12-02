import re
from pprint import pprint
from typing import List, Tuple

# https://stackoverflow.com/a/4665027/2278742
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


def get_digits(line: str):
    mapping = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}

    # search spelled out numbers and save them together with their indices in a dict
    found_spelled_out_numbers = {}

    for key in mapping.keys():
        indices = list(find_all(line, key))
        if indices != -1:
            for index in indices:
                found_spelled_out_numbers[index] = key
    pprint(found_spelled_out_numbers)

    # search actual digits and save them together with their indices in a dict
    all_found_numbers = found_spelled_out_numbers
    count = 0
    for char in line:
        if re.match(r"\d", char):
            print(char)
            all_found_numbers[count] = char
        count += 1

    # replace spelled out numbers in dict with actual digits
    for key, val in all_found_numbers.items():
        print(f"checking if {val} in")
        pprint(mapping.keys())
        if val in mapping.keys():
            all_found_numbers[key] = mapping[val]

    print(f"{all_found_numbers=}")

    # create list with the two digits that have the lowest and highest index
    digits = [all_found_numbers[sorted(all_found_numbers.keys())[0]], all_found_numbers[sorted(all_found_numbers.keys())[-1]]]
    print(f"{digits=}")

    return digits


def solve_puzzle_part(input_file: str, part: int) -> Tuple[List[int], int]:
    calibration_values = list()
    sum = 0

    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            print(line)
            if part == 2:
                digits = get_digits(line)
            else:
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
print(sum)

assert calibration_values[0] == 88
assert calibration_values[1] == 55
assert calibration_values[2] == 86
assert calibration_values[3] == 79
assert calibration_values[4] == 16
assert calibration_values[5] == 32
assert calibration_values[6] == 14
assert calibration_values[7] == 49
assert calibration_values[8] == 87
assert calibration_values[9] == 68
assert calibration_values[10] == 71
assert calibration_values[11] == 33
assert calibration_values[12] == 73
assert calibration_values[13] == 39
assert calibration_values[14] == 42
assert calibration_values[15] == 58
assert calibration_values[16] == 62
assert calibration_values[17] == 35
assert calibration_values[18] == 65

assert sum < 54999
assert sum < 54996
assert sum != 54978
assert sum != 55001
assert sum != 324
assert sum == 54985
