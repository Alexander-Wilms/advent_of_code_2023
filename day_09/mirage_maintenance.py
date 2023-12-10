import re


def solve_puzzle_part(file_name: str, part: int) -> int:
    report = []
    with open(file_name) as f:
        for line in f.readlines():
            history = re.findall(r"\-*\d+", line)
            history = [int(x) for x in history]
            report.append([history])
    # print("report:")
    # pprint(report)

    sum_next = 0
    sum_prev = 0

    next_value = 0
    idx = 0
    for histories_idx in range(len(report)):
        print(f"{histories_idx+1}/{len(report)}")
        all_deltas_zeros = False
        indent = ""
        idx = 0
        next_value = 0
        next_value_addends = []
        histories = []
        while not all_deltas_zeros:
            history = report[histories_idx][idx]
            histories.append(history)

            next_value += report[histories_idx][-1][-1]
            next_value_addends.append(report[histories_idx][-1][-1])

            if report[histories_idx][-1].count(0) == len(report[histories_idx][-1]):
                all_deltas_zeros = True

            differences = []
            for history_idx in range(len(history)):
                try:
                    differences.append(history[history_idx + 1] - history[history_idx])
                except:
                    pass

            report[histories_idx].append(differences)
            if differences.count(0) == len(differences):
                all_deltas_zeros = True

            # pprint(report)
            idx += 1
        # print()

        print("last values")
        last_values = []
        first_values = []
        for idx in range(len(histories)):
            last_values.append(histories[idx][-1])
            first_values.append(histories[idx][0])
            # print(last_values[-1])

        last_values.append(0)
        print(f"{last_values=}")

        first_values.append(0)
        print(f"{first_values=}")

        print_triangle(report, histories_idx, first_values, last_values)

        tmp_last = 0
        tmp_first = 0
        for idx in range(len(last_values) - 1, 0 - 1, -1):
            # print(f"{tmp} += {last_values[idx]}")
            tmp_last += last_values[idx]
            last_values[idx] = tmp_last

            if idx < len(last_values) - 1:
                print(f"{report[histories_idx][idx]}")
                print("first entry of history - first entry of first_values of previous row = ?")
                a = report[histories_idx][idx][0]
                b = first_values[idx + 1]
                c = a - b
                first_values[idx] = c
                print(f"{a} - {b} = {c}")

        print(f"{last_values=}")
        print(f"{first_values=}")

        tmp_last = 0
        for idx in range(len(next_value_addends)):
            tmp_last += next_value_addends[idx]
            next_value_addends[idx] = tmp_last

        print_triangle(report, histories_idx, first_values, last_values)

        # last row
        # history = report[histories_idx][-1]
        # print(indent, end="")
        # print(f"{first_values[idx]} |", end="")
        # for value in history:
        #     print(f"{value:=3} ", end="")
        # print(f"| {last_values[-1]}")
        # print()

        # print(f"{next_value=}")
        sum_next += next_value
        sum_prev += first_values[0]

    print(f"{next_value=} -> {sum_next}")

    print(f"{first_values=} -> {sum_prev}")

    if part == 1:
        return sum_next
    else:
        return sum_prev


def print_triangle(report, histories_idx, first_values, last_values):
    indent = "  "
    # pprint(histories)
    for idx in range(len(report[histories_idx])):
        history = report[histories_idx][idx]
        print(indent, end="")
        print(f"{first_values[idx]} |", end="")
        for value in history:
            print(f"{value:=3} ", end="")
        print(f"| {last_values[idx]}")
        indent += "  "


def test_solutions() -> None:
    sum = solve_puzzle_part("day_09/example_1.txt", 1)
    assert sum == 114

    sum = solve_puzzle_part("day_09/input.txt", 1)
    assert sum == 2043183816

    sum = solve_puzzle_part("day_09/example_1.txt", 2)
    assert sum == 2

    sum = solve_puzzle_part("day_09/input.txt", 2)
    assert sum == 1118


if __name__ == "__main__":
    test_solutions()
