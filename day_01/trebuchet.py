import re
from pprint import pprint

def solve(input_file: str) -> int:
    sum = 0

    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            print(line)
            digits = re.findall(r"\d", line)
            pprint(digits)
            calibration_value = f"{digits[0]}{digits[-1]}"
            print(calibration_value)
            sum += int(calibration_value)
            print()

    print(sum)
    return sum

solve("day_01/example.txt")
solve("day_01/input.txt")