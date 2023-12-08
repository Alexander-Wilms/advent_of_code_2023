import re
from pprint import pprint
from typing import Dict

import matplotlib.pyplot as plt
import networkx as nx


def solve_puzzle_part(file_name: str, part_selection: int) -> int:
    with open(file_name) as f:
        left_right_instructions = f.readline().strip()
        f.readline()
        G = nx.DiGraph()
        map: Dict[str, Dict[str, str]] = {}
        first_node_found = False
        color_map = []
        lines = f.readlines()
        for line in lines:
            nodes = re.findall(r"[A-Z]+", line)
            if not nodes:
                continue
            if not first_node_found:
                nodes[0]
                first_node_found = True
            G.add_node(nodes[0])
            print(f"Adding node '{nodes[0]}'")
            if nodes[0] == "AAA":
                color_map.append("green")
            if nodes[0] == "ZZZ":
                color_map.append("red")
            else:
                color_map.append("white")

        pprint(G.__dict__)

        for line in lines:
            nodes = re.findall(r"[A-Z]+", line)
            if not nodes:
                continue
            print(f"Adding edge '{nodes[1]}' -> '{nodes[0]}'")
            G.add_edge(nodes[0], nodes[1])
            print(f"Adding edge '{nodes[0]}' -> '{nodes[2]}'")
            G.add_edge(nodes[0], nodes[2])
            map[nodes[0]] = {}
            map[nodes[0]]["L"] = nodes[1]
            map[nodes[0]]["R"] = nodes[2]

        pprint(G.__dict__)

        nx.draw_networkx(G, nx.kamada_kawai_layout(G))
        plt.show()

        G_undirected = G.to_undirected()

        # https://stackoverflow.com/a/61537932/2278742
        components = [G_undirected.subgraph(c).copy() for c in nx.connected_components(G_undirected)]
        for idx, G_undirected in enumerate(components, start=1):
            print(f"Component {idx}: Nodes: {G_undirected.nodes()} Edges: {G_undirected.edges()}")

    current_node = "AAA"

    pprint(left_right_instructions)
    step_count = 0
    done = False
    while not done:
        for instruction in left_right_instructions:
            # pprint(map[current_node])
            step_count += 1
            next_node = map[current_node][instruction]
            # print(f"{current_node} -{instruction}-> {next_node}")
            current_node = next_node
            if current_node == "ZZZ":
                done = True
                break

    print(f"{step_count=}")
    return step_count


def test_solutions():
    sum = solve_puzzle_part("day_08/example_1.txt", 1)
    assert sum == 2

    sum = solve_puzzle_part("day_08/example_2.txt", 1)
    assert sum == 6

    sum = solve_puzzle_part("day_08/input.txt", 1)
    assert sum == 12599


if __name__ == "__main__":
    test_solutions()
