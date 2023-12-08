# comment out networkx to compile code with Cython
import re
from math import lcm
from pprint import pprint
from typing import Dict

import matplotlib.pyplot as plt
import networkx as nx

map: Dict[str, Dict[str, str]] = {}


def solve_puzzle_part(file_name: str, part: int) -> int:
    global map
    map = {}
    with open(file_name) as f:
        left_right_instructions = f.readline().strip()
        f.readline()
        G = nx.DiGraph()
        first_node_found = False
        color_map = []
        lines = f.readlines()
    for line in lines:
        nodes = re.findall(r"[0-9A-Z]+", line)
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
        nodes = re.findall(r"[0-9A-Z]+", line)
        if not nodes:
            continue
        print(f"Adding edge '{nodes[1]}' -> '{nodes[0]}'")
        G.add_edge(nodes[0], nodes[1])
        print(f"Adding edge '{nodes[0]}' -> '{nodes[2]}'")
        G.add_edge(nodes[0], nodes[2])
        map[nodes[0]] = {}
        map[nodes[0]]["L"] = nodes[1]
        map[nodes[0]]["R"] = nodes[2]

    # pprint(G.__dict__)

    if part == 1:
        start_node = "AAA"
    else:
        start_nodes = []
        end_nodes = []

    G_undirected = G.to_undirected()

    # graph connectivity can only be determined for undirected graphs
    # but since we need the directed to traverse the graph, we need to
    # recreate it using the reduced set of nodes afterwards
    # https://stackoverflow.com/a/61537932/2278742
    graph_could_be_reduced = False
    components = [G_undirected.subgraph(c).copy() for c in nx.connected_components(G_undirected)]
    subgraphs = []
    for subgraph_idx, G_undirected in enumerate(components, start=1):
        list_of_nodes_of_subgraph = sorted(G_undirected.nodes())

        print(f"Component {subgraph_idx}: Nodes: {list_of_nodes_of_subgraph}")

        is_a_subgraph = False
        if part == 1:
            if "AAA" in list_of_nodes_of_subgraph and "ZZZ" in list_of_nodes_of_subgraph:
                is_a_subgraph = True
                print("AAA and ZZZ in subgraph")
        else:
            xxA_found = False
            xxZ_found = False
            for node in list_of_nodes_of_subgraph:
                if node.endswith("A"):
                    xxA_found = True
                    start_nodes.append(node)
                if node.endswith("Z"):
                    xxZ_found = True
                    end_nodes.append(node)
            if xxA_found and xxZ_found:
                is_a_subgraph = True
                print("(xxA and xxZ) NOT in subgraph")

        if is_a_subgraph:
            nodes_in_subgraph = list_of_nodes_of_subgraph
            subgraphs.append(nodes_in_subgraph)
            graph_could_be_reduced = True

    if part == 2:
        print(f"{start_nodes=}")
        print(f"{end_nodes=}")

    # https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html
    nx.draw_networkx(G, nx.kamada_kawai_layout(G))
    plt.show(block=False)
    pprint(f"{subgraphs=}")

    if part == 1:
        current_node = start_node
    else:
        current_nodes = start_nodes

    pprint(left_right_instructions)
    step_count = 0
    done = False

    map_reduced_of_subgraphs: list[list[str]] = [[""]] * len(subgraphs)

    print("extract subgraphs")
    for subgraph_idx in range(len(subgraphs)):
        if graph_could_be_reduced:
            G_reduced, map_reduced_of_subgraphs[subgraph_idx] = reduce_graph(subgraphs[subgraph_idx], lines)
        else:
            G_reduced = G

    nx.draw_networkx(G_reduced, nx.kamada_kawai_layout(G_reduced))
    plt.show(block=True)
    print("extracting subgraphs complete")

    turns_to_z = [-1] * len(subgraphs)
    while not done:
        for instruction_idx in range(len(left_right_instructions)):
            # time.sleep(1)
            instruction = left_right_instructions[instruction_idx]
            # print(left_right_instructions[0:instruction_idx])
            step_count += 1
            if part == 1:
                # pprint(map[current_node])
                next_node = map_reduced_of_subgraphs[0][current_node][instruction]
                # print(f"{current_node} -{instruction}-> {next_node}")
                current_node = next_node
                if current_node == "ZZZ":
                    done = True
                    break
            else:
                all_current_nodes_end_with_Z = True
                next_nodes = [""] * len(subgraphs)
                print(f"{current_nodes=}")
                print(f" |\n {instruction}\n\\|/")
                # print(f"{len(subgraphs)}")

                if len(subgraphs) > 1:
                    for subgraph_idx in range(len(subgraphs)):
                        current_node = current_nodes[subgraph_idx]
                        # print(f"\t{current_node=}")
                        next_node = map_reduced_of_subgraphs[subgraph_idx][current_node][instruction]
                        next_nodes[subgraph_idx] = next_node

                        # print(f"\t\t{current_node} -{instruction}-> {next_node}")
                        # print(f"\t\t\t{next_nodes=}")
                        this_node_ends_with_z = next_node.endswith("Z")
                        if this_node_ends_with_z:
                            turns_to_z[subgraph_idx] = step_count
                            print(f"{turns_to_z[subgraph_idx]=}")
                            if -1 not in turns_to_z:
                                pprint(f"{turns_to_z=}")
                                step_count = lcm(*turns_to_z)
                                print(step_count)
                                done = True
                                break
                        # print(f"{this_node_ends_with_z=}")
                        all_current_nodes_end_with_Z &= this_node_ends_with_z
                        # print(f"{all_current_nodes_end_with_Z=}")

                else:
                    next_nodes = []
                    for current_node in current_nodes:
                        # print(current_node)
                        next_node = map[current_node][instruction]
                        next_nodes.append(next_node)
                        print(f"{current_node} -{instruction}-> {next_node}")
                        this_node_ends_with_z = next_node.endswith("Z")
                        print(f"{this_node_ends_with_z=}")
                        all_current_nodes_end_with_Z &= this_node_ends_with_z
                        print(f"{all_current_nodes_end_with_Z=}")
                    if all_current_nodes_end_with_Z:
                        done = True
                        break
                current_nodes = next_nodes

    print(f"{step_count=}")
    return step_count


def reduce_graph(nodes_in_subgraph: list[str], lines: list[str]) -> tuple[nx.DiGraph, dict]:
    G_reduced = nx.DiGraph()
    for node in nodes_in_subgraph:
        G_reduced.add_node(node)

    for line in lines:
        nodes = re.findall(r"[0-9A-Z]+", line)
        if not nodes:
            continue
        if nodes[0] not in nodes_in_subgraph:
            continue
        # print(f"Adding edge '{nodes[1]}' -> '{nodes[0]}'")
        G_reduced.add_edge(nodes[0], nodes[1])
        # print(f"Adding edge '{nodes[0]}' -> '{nodes[2]}'")
        G_reduced.add_edge(nodes[0], nodes[2])

    map_reduced = {}
    for node in nodes_in_subgraph:
        map_reduced[node] = map[node]

    return G_reduced, map_reduced


def test_solutions():
    sum = solve_puzzle_part("day_08/example_1.txt", 1)
    assert sum == 2

    sum = solve_puzzle_part("day_08/example_2.txt", 1)
    assert sum == 6

    sum = solve_puzzle_part("day_08/input.txt", 1)
    assert sum == 12599

    sum = solve_puzzle_part("day_08/example_3.txt", 2)
    assert sum == 6

    sum = solve_puzzle_part("day_08/input.txt", 2)
    assert sum > 15529
    assert sum > 21389
    assert sum == 8245452805243


if __name__ == "__main__":
    test_solutions()
