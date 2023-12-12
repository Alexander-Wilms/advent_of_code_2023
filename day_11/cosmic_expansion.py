# comment out networkx to compile code with Cython
import os
from itertools import combinations
from pprint import pprint
from typing import Dict

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from numba import prange
from pandas import DataFrame

map: Dict[str, Dict[str, str]] = {}

possible_combinations: list = []
galaxies_expanded: Dict = {}
G_expanded: nx.Graph = {}


def find_empty_cols_and_rows(map: DataFrame) -> tuple[list, list, dict]:
    print("Find rows and columns without galaxies")
    (rows, cols) = map.shape
    cols_empty = [True] * cols
    rows_empty = [True] * rows

    galaxies = {}
    galaxy_count = 1

    # https://stackoverflow.com/a/59413206/2278742
    row_count = 0
    for row in map.itertuples(index=False):
        col_count = 0
        for val in row:
            if val != ".":
                rows_empty[row_count] = False
                cols_empty[col_count] = False
                galaxies[galaxy_count] = [row_count, col_count]
                galaxy_count += 1
            col_count += 1
        row_count += 1

    rows_empty_idx = list(np.where(rows_empty)[0])
    cols_empty_idx = list(np.where(cols_empty)[0])

    pprint(f"{rows_empty_idx=}")
    pprint(f"{cols_empty_idx=}")

    return rows_empty_idx, cols_empty_idx, galaxies


def expand_universe(map: DataFrame) -> tuple[DataFrame, list, list]:
    global factor
    number_of_copies = factor - 1
    print("Expanding universe")
    (rows, cols) = map.shape
    rows_empty, cols_empty, _ = find_empty_cols_and_rows(map)

    empty_col = pd.DataFrame({"V": ["."] * rows})
    for idx in range(len(cols_empty) - 1, 0 - 1, -1):
        for tmp in range(number_of_copies):
            col_idx = cols_empty[idx]
            # print(f"inserting empty col at index {col_idx}")
            map = pd.concat([map.iloc[:, :col_idx], empty_col, map.iloc[:, col_idx:]], axis=1)
            # print(map)
            map.columns = range(map.columns.size)

    (rows, cols) = map.shape

    for idx in range(len(rows_empty) - 1, 0 - 1, -1):
        for tmp in range(number_of_copies):
            row_idx = rows_empty[idx]
            # print(f"inserting empty row at index {row_idx}")
            # map.loc[row_idx - 0.5] = ["."] * cols
            empty_row = pd.DataFrame(columns=range(cols))
            empty_row.loc[0] = ["."] * cols
            # print(empty_row)
            map = pd.concat([map.iloc[:row_idx, :], empty_row, map.iloc[row_idx:, :]], axis=0)
            map.index = range(map.index.size)
            # print(map)

    print("Expanded universe:")
    print(map)

    return map, rows_empty, cols_empty


def map_to_graph(map: DataFrame) -> tuple[nx.Graph, dict, dict]:
    (rows, cols) = map.shape

    positions = {}
    labels = {}

    print("Creating graph")
    G = nx.Graph()

    for row in range(rows):
        for col in range(cols):
            node_name = f"{row},{col}"
            G.add_node(node_name)
            positions[node_name] = [col, -row]
            labels[node_name] = f"{node_name}: {map.at[row, col]}"
            if col + 1 < cols:
                G.add_edge(f"{row},{col}", f"{row},{col+1}")
            if row + 1 < rows:
                G.add_edge(f"{row},{col}", f"{row+1},{col}")
    print("Graph created")

    return G, positions, labels


# see example on https://numba.pydata.org/
# but numba decorator doesn't seem to work with Cython
# TypeError: The decorated object is not a function (got type <class '_cython_3_0_6.cython_function_or_method'>).
# @njit(parallel=True)
def numba_example() -> np.ndarray:
    out = np.arange(1000)

    for i in prange(out.shape[0]):
        out[i] = 42

    return out


def solve_puzzle_part(file_name: str, show_plot: bool, efficient=False) -> int:
    global G_expanded, galaxies_expanded, possible_combinations

    with open(file_name) as f:
        data_single_string = f.read()

    data = data_single_string.split("\n")
    number_of_galaxies = data_single_string.count("#")
    print(f"Universe contains {number_of_galaxies} galaxies")

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

    rows_empty_idx, cols_empty_idx, galaxies = find_empty_cols_and_rows(map)

    print(f"{galaxies=}")

    if efficient:
        sum_of_shortest_path_lengths = 0

        for galaxy_id, galaxy_coords in galaxies.items():
            print(f"{galaxy_id}: {galaxy_coords}")

            galaxy_row = galaxy_coords[0]
            galaxy_col = galaxy_coords[1]

            empty_rows_so_far = [x for x in rows_empty_idx if x < galaxy_row]
            empty_cols_so_far = [x for x in cols_empty_idx if x < galaxy_col]

            print(f"{empty_rows_so_far=}")
            print(f"{empty_cols_so_far=}")

            row_after_expansion = galaxy_row + (factor - 1) * len(empty_rows_so_far)
            col_after_expansion = galaxy_col + (factor - 1) * len(empty_cols_so_far)

            print(f"{row_after_expansion=}")
            print(f"{col_after_expansion=}")

            galaxies[galaxy_id] = [row_after_expansion, col_after_expansion]

            print()

        pprint(f"{galaxies=}")

        galaxy_ids = list(galaxies.keys())
        possible_combinations = list(combinations(galaxy_ids, 2))

        print(f"In these {number_of_galaxies} galaxies, there are {len(possible_combinations)} pairs.")

        number_of_possible_combinations = len(possible_combinations)
        combination_count = 0
        for combination in possible_combinations:
            print(f"combination {combination_count+1}/{number_of_possible_combinations}")
            combination_count += 1

            g1, g2 = combination

            g1_row = galaxies[g1][0]
            g1_col = galaxies[g1][1]

            g2_row = galaxies[g2][0]
            g2_col = galaxies[g2][1]

            g1_node_name = f"{g1_row},{g1_col}"
            g2_node_name = f"{g2_row},{g2_col}"

            print(f"\tBetween galaxy {g1} (node '{g1_node_name}') and galaxy {g2} (node '{g2_node_name}')")

            shortest_path_len = max(g2_row, g1_row) - min(g2_row, g1_row) + max(g2_col, g1_col) - min(g2_col, g1_col)
            print(f"\t{shortest_path_len=}")

            sum_of_shortest_path_lengths += shortest_path_len
    else:
        G, positions, labels = map_to_graph(map)

        map_expanded, _, _ = expand_universe(map)
        _, _, galaxies_expanded = find_empty_cols_and_rows(map_expanded)
        pprint(f"{galaxies_expanded=}")
        G_expanded, positions_expanded, labels_expanded = map_to_graph(map_expanded)

        if show_plot:
            options = {
                "font_size": 10,
                "node_size": 1000,
                "node_color": "white",
                "edgecolors": "black",
            }

            fig, axes = plt.subplots(nrows=1, ncols=2)
            ax = axes.flatten()

            ax[0].set_title("Original")
            nx.draw_networkx(G, positions, labels=labels, **options, ax=ax[0])

            ax[1].set_title("Expanded")
            nx.draw_networkx(G_expanded, positions_expanded, labels=labels_expanded, **options, ax=ax[1])

        galaxy_ids = list(galaxies_expanded.keys())
        possible_combinations = list(combinations(galaxy_ids, 2))

        print(f"In these {number_of_galaxies} galaxies, there are {len(possible_combinations)} pairs.")

        parallel = False

        if parallel:
            # even running the path searches in parallel might be too slow with 1000 000 inserted cols/rows per empty col/row
            # there is probably a closed-form expression for the solution

            # iterate through loop in parallel
            numba_output = numba_example()
            pprint(numba_output)

            # shortest_path_lengths = find_shortest_path_lengths()
            # sum_of_shortest_path_lengths = sum(shortest_path_lengths)
            sum_of_shortest_path_lengths = 0
        else:
            sum_of_shortest_path_lengths = 0
            combination_count = 1
            number_of_possible_combinations = len(possible_combinations)
            for combination in possible_combinations:
                print(f"combination {combination_count}/{number_of_possible_combinations}")

                combination_count += 1
                g1, g2 = combination

                g1_row = galaxies_expanded[g1][0]
                g1_col = galaxies_expanded[g1][1]

                g2_row = galaxies_expanded[g2][0]
                g2_col = galaxies_expanded[g2][1]

                g1_node_name = f"{g1_row},{g1_col}"
                g2_node_name = f"{g2_row},{g2_col}"

                print(f"\tBetween galaxy {g1} (node '{g1_node_name}') and galaxy {g2} (node '{g2_node_name}')")

                shortest_path = nx.shortest_path(G_expanded, g1_node_name, g2_node_name)

                shortest_path = shortest_path[1:]
                # print(f"\t{shortest_path=}")
                shortest_path_len = len(shortest_path)
                print(f"\t{shortest_path_len=}")

                sum_of_shortest_path_lengths += shortest_path_len

        if show_plot:
            plt.show(block=True)

    print(f"{sum_of_shortest_path_lengths=}")

    return sum_of_shortest_path_lengths


factor = 0


def test_solutions():
    global factor

    # inefficient algorithm
    factor = 2
    steps = solve_puzzle_part("day_11/example_1.txt", False)
    assert steps == 374

    factor = 2
    steps = solve_puzzle_part("day_11/input.txt", False)
    assert steps == 10494813

    factor = 10
    steps = solve_puzzle_part("day_11/example_1.txt", False)
    assert steps == 1030

    factor = 100
    steps = solve_puzzle_part("day_11/example_1.txt", False)
    assert steps == 8410

    # efficient algorithm
    factor = 2
    steps = solve_puzzle_part("day_11/example_1.txt", False, True)
    assert steps == 374

    factor = 10
    steps = solve_puzzle_part("day_11/example_1.txt", False, True)
    assert steps == 1030

    factor = 100
    steps = solve_puzzle_part("day_11/example_1.txt", False, True)
    assert steps == 8410

    factor = 1000000
    steps = solve_puzzle_part("day_11/input.txt", False, True)
    assert steps == 840988812853


if __name__ == "__main__":
    test_solutions()
