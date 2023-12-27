
from time import time


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


Node = str
Edge = tuple[Node, Node]
Graph = dict[Node, list[Node]]


def parse_input(lines: list[str]) -> Graph:
    # "jqt: rhn xhk nvd"
    graph = {}
    for line in lines:
        s, ts = line.split(": ")
        if s not in graph:
            graph[s] = []
        for t in ts.split(" "):
            if t not in graph:
                graph[t] = []
            graph[s].append(t)
            graph[t].append(s)
    return graph


def edges(graph: Graph) -> list[Edge]:
    # Returns both (s, t) and (t, s) for each edge.
    return [(s, t) for s in graph.keys() for t in graph[s]]


Flow = dict[Edge, int]


def find_flow(graph: Graph, start: Node, goal: Node) -> tuple[int, Flow]:
    flow = {edge: 0 for edge in edges(graph)}
    max_flow = 0

    while True:
        path = find_path_with_capacity(graph, flow, start, goal)

        if path is None:
            return max_flow, flow

        max_flow += 1
        for (s, t) in path:
            flow[(s, t)] += 1
            flow[(t, s)] -= 1


def find_path_with_capacity(graph: Graph, flow: Flow, start: Node, goal: Node
                            ) -> Optional[list[Edge]]:
    previous_node = {start: None}
    queue = [start]
    while len(queue) > 0:
        s = queue.pop(0)

        if s == goal:
            reverse_path = []
            while s != start:
                reverse_path.append((previous_node[s], s))
                s = previous_node[s]
            return list(reversed(reverse_path))

        for t in graph[s]:
            if t not in previous_node and flow[(s, t)] < 1:
                previous_node[t] = s
                queue.append(t)

    return None


def solve(lines: list[str]) -> int:
    graph = parse_input(lines)
    for try_s in graph.keys():
        for try_t in graph.keys():
            if try_s == try_t:
                continue

            print(f"{try_s = }, {try_t = }")
            max_flow, flow_dict = find_flow(graph, try_s, try_t)
            if max_flow == 3:
                cut = find_cut(graph, flow_dict, try_s)
                size1 = len(cut)
                size2 = len(graph) - size1
                print(f"{size1 = }, {size2 = }")
                return size1 * size2


def find_cut(graph: Graph, flow: dict[Edge, int], start: str) -> set[str]:
    visited = {start}
    queue = [start]
    while len(queue) > 0:
        s = queue.pop(0)
        for t in graph[s]:
            if t not in visited and flow[(s, t)] < 1:
                visited.add(t)
                queue.append(t)

    return visited


def main():
    lines = read_input()
    if len(lines) == 0:
        raise ValueError("Input is empty")

    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    start_time = time()
    main()
    print(f"Solved in about {time() - start_time:.4f} seconds")
