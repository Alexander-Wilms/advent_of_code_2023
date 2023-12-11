# comment out networkx to compile code with Cython
import os
from pprint import pprint
from typing import Dict

import numpy as np
import pandas as pd
from pandas import DataFrame

map: Dict[str, Dict[str, str]] = {}


def find_empty_cols_and_rows(map: DataFrame) -> tuple[list, list]:
    (rows, cols) = map.shape
    cols_empty = [True] * cols
    rows_empty = [True] * rows

    # https://stackoverflow.com/a/59413206/2278742
    row_count = 0
    for row in map.itertuples(index=False):
        col_count = 0
        for val in row:
            if val != ".":
                rows_empty[row_count] = False
                cols_empty[col_count] = False
            col_count += 1
        row_count += 1

    rows_empty_idx = np.where(rows_empty)[0]
    cols_empty_idx = np.where(cols_empty)[0]

    pprint(f"{rows_empty_idx=}")
    pprint(f"{cols_empty_idx=}")

    return rows_empty_idx, cols_empty_idx


def expand_universe(map: DataFrame) -> DataFrame:
    print("Expanding universe")
    (rows, cols) = map.shape
    rows_empty, cols_empty = find_empty_cols_and_rows(map)

    empty_col = pd.DataFrame({"V": ["."] * rows})
    for idx in range(len(cols_empty) - 1, 0 - 1, -1):
        col_idx = cols_empty[idx]
        print(f"inserting empty col at index {col_idx}")
        map = pd.concat([map.iloc[:, :col_idx], empty_col, map.iloc[:, col_idx:]], axis=1)
        print(map)
        map.columns = range(map.columns.size)

    (rows, cols) = map.shape

    for idx in range(len(rows_empty) - 1, 0 - 1, -1):
        row_idx = rows_empty[idx]
        print(f"inserting empty row at index {row_idx}")
        map.loc[row_idx + 0.5] = ["."] * cols
        empty_row = pd.DataFrame(columns=range(cols))
        empty_row.loc[0] = ["."] * cols
        print(empty_row)
        map = pd.concat([map.iloc[:row_idx, :], empty_row, map.iloc[row_idx:, :]], axis=0)
        map.index = range(map.index.size)
        print(map)

    print("Expanded universe:")
    print(map)


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

    map: DataFrame = pd.read_csv(f"{file_name}.csv", header=None)
    os.remove(f"{file_name}.csv")

    print(map)

    expand_universe(map)

    print("Find rows and columns without galaxies")

    return 0


def test_solutions():
    steps = solve_puzzle_part("day_11/example_1.txt", 1)
    print(steps)
    #assert steps == 374


if __name__ == "__main__":
    test_solutions()
