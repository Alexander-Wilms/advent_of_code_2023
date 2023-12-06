import re
from pprint import pprint


def solve_puzzle_part(file_name: str, part: int) -> int:
    with open(file_name) as f:
        line = f.readline()
        time = re.findall(r"\d+", line)
        time = [int(x) for x in time]
        line = f.readline()
        distances = re.findall(r"\d+", line)
        distances = [int(x) for x in distances]

        pprint(time)
        pprint(distances)

    margin_of_error = 1
    for race_idx in range(len(time)):
        print(f"> Race {race_idx}:")
        possible_distances = []

        possible_ways_to_win = []
        for option in range(time[race_idx] + 1):
            button_hold_time = option
            speed = option
            time_in_motion = time[race_idx] - option
            distance = option * (time[race_idx] - option)
            print(f"Hold the button for {button_hold_time} millisecond at the start of the race. Then, the \nboat will travel at a speed of {speed} millimeter per millisecond for {time_in_motion} \nmilliseconds, reaching a total distance traveled of {distance} millimeters.")
            print()

            possible_distances.append(distance)

            if distance > distances[race_idx]:
                possible_ways_to_win.append(button_hold_time)

        print("Possible distances for this race:")
        pprint(possible_distances)

        print("Possible hold times to win this race:")
        pprint(possible_ways_to_win)

        number_of_ways_to_win = len(possible_ways_to_win)
        print(f"{number_of_ways_to_win=}")

        margin_of_error *= number_of_ways_to_win
    print(f"{margin_of_error=}")
    return margin_of_error


def test_solutions():
    sum = solve_puzzle_part("day_06/example_1.txt", 1)
    assert sum == 288

    sum = solve_puzzle_part("day_06/input.txt", 1)
    assert sum == 2065338


if __name__ == "__main__":
    test_solutions()
