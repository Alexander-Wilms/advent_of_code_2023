import math
import re
from pprint import pprint


def solve_puzzle_part(file_name: str, part: int, efficient: bool) -> int:
    with open(file_name) as f:
        line = f.readline()
        if part == 2:
            line = line.replace(" ", "")
        time = re.findall(r"\d+", line)
        time = [int(x) for x in time]

        line = f.readline()
        if part == 2:
            line = line.replace(" ", "")
        distances = re.findall(r"\d+", line)
        distances = [int(x) for x in distances]

        pprint(time)
        pprint(distances)

    # both ways work, but the first approach is too slow
    if not efficient:
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
    else:
        margin_of_error = 1
        for race_idx in range(len(time)):
            # print("(t_total-t_hold)*t_hold = dist")
            # print(f"({time[race_idx]}-t_hold)*t_hold = {distances[race_idx]}")
            # print(f"(-t_hold^2 + {time[race_idx]}*t_hold - {distances[race_idx]} = 0")
            # print("Solve quadratic equation ax^2+bx+c = 0")
            a = -1
            b = time[race_idx]
            # distance must be greater than the record, thus add a small constant
            c = -(distances[race_idx] + 0.00000000001)
            root_of_discriminant = math.sqrt(b**2 - 4 * a * c)
            x_1 = (-b + root_of_discriminant) / 2 * a
            x_2 = (-b - root_of_discriminant) / 2 * a
            # print(f"roots: {x_1}, {x_2}")
            lower_bound = x_1
            upper_bound = math.floor(x_2)
            # print(f"{lower_bound=}")
            # print(f"{upper_bound=}")

            hold_time_options = list(range(time[race_idx] + 1))
            # print(hold_time_options)

            reduced_hold_time_options = [num for num in hold_time_options if num >= lower_bound and num <= upper_bound]
            # print(reduced_hold_time_options)

            number_of_ways_to_win = len(reduced_hold_time_options)
            # print(f"{number_of_ways_to_win=}")

            margin_of_error *= number_of_ways_to_win

    print(f"{margin_of_error=}")
    return margin_of_error


def test_solutions():
    sum = solve_puzzle_part("day_06/example_1.txt", 1, False)
    assert sum == 288

    sum = solve_puzzle_part("day_06/input.txt", 1, False)
    assert sum == 2065338

    sum = solve_puzzle_part("day_06/example_1.txt", 2, False)
    assert sum == 71503

    # verify the solution using a quadratic equation works with the example input
    sum = solve_puzzle_part("day_06/example_1.txt", 1, True)
    assert sum == 288

    sum = solve_puzzle_part("day_06/example_1.txt", 2, True)
    assert sum == 71503

    # solve part 2 with the actual input
    sum = solve_puzzle_part("day_06/input.txt", 2, True)
    assert sum == 34934171


if __name__ == "__main__":
    test_solutions()
