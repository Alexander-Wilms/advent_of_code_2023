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

    sum = 0
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
            for history_idx in range(len(history) - 1):
                differences.append(history[history_idx + 1] - history[history_idx])

            report[histories_idx].append(differences)
            if differences.count(0) == len(differences):
                all_deltas_zeros = True

            # pprint(report)
            idx += 1
        # print()

        print("last values")
        last_values = []
        for idx in range(len(histories)):
            last_values.append(histories[idx][-1])
            # print(last_values[-1])

        last_values.append(0)
        print(f"{last_values=}")

        tmp = 0
        for idx in range(len(last_values) - 1, 0 - 1, -1):
            # print(f"{tmp} += {last_values[idx]}")
            tmp += last_values[idx]
            last_values[idx] = tmp

        print(f"{last_values=}")

        tmp = 0
        for idx in range(len(next_value_addends)):
            tmp += next_value_addends[idx]
            next_value_addends[idx] = tmp

        # pprint(histories)
        for idx in range(len(histories)):
            history = histories[idx]
            print(indent, end="")
            for value in history:
                print(f"{value:=3} ", end="")
            print(f"{value:=3} ", end="")
            print(f"| {last_values[idx]}")
            indent += "  "

        # last row
        history = report[histories_idx][-1]
        print(indent, end="")
        for value in history:
            print(f"{value:=3} ", end="")
        print(f"| {last_values[-1]}")
        print()

        print(f"{next_value=}")
        sum += next_value

    print(f"{sum=}")

    return sum


def test_solutions() -> None:
    sum = solve_puzzle_part("day_09/example_1.txt", 1)
    assert sum == 114

    sum = solve_puzzle_part("day_09/input.txt", 1)
    assert sum == 2043183816


if __name__ == "__main__":
    test_solutions()
