from abc import abstractmethod
import networkx as nx
import matplotlib.pyplot as plt

data = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

data = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

data = open("20.txt").read()


class Node:
    def __init__(self, name, kind) -> None:
        self.parents: list["Node"] = []
        self.next: list[Node] = list()
        self.name = name
        self.kind = kind
        self.transmission_buffer = []

    @abstractmethod
    def input(self, parent, high):
        pass

    def add_parent(self, parent: "Node"):
        if parent not in self.parents:
            self.parents.append(parent)

    def set_next(self, node: "Node"):
        if node not in self.next:
            self.next.append(node)


class FlipFlop(Node):
    def __init__(self, name) -> None:
        super().__init__(name, "FLP")
        self.status = False

    def input(self, parent, high):
        if not high:
            self.status = not self.status
            self.transmission_buffer += [self.status]


class Conjunction(Node):
    def __init__(self, name) -> None:
        super().__init__(name, "CON")
        self.incoming: dict[Node, bool] = dict()

    def add_parent(self, parent: "Node"):
        super().add_parent(parent)
        self.incoming[parent] = False

    def input(self, parent, high):
        self.incoming[parent] = high
        if all(self.incoming.values()):
            self.transmission_buffer.append(False)
        else:
            self.transmission_buffer.append(True)


class UnTyped(Node):
    def __init__(self, name) -> None:
        super().__init__(name, "END")

    def set_next(self, node: "Node"):
        pass


broadcaster = []
modules: dict[str, Node] = dict()
edges = []

for line in data.strip().split("\n"):
    if line.startswith("broadcaster"):
        broadcaster = line.split("->")[-1].strip().split(", ")
    if line.startswith("%"):
        source, destination_str = line[1:].strip().split(" -> ")
        destinations = destination_str.split(", ")
        modules[source] = FlipFlop(source)
        for d in destinations:
            edges.append((source, d))
    if line.startswith("&"):
        source, destination_str = line[1:].strip().split(" -> ")
        destinations = destination_str.split(", ")
        modules[source] = Conjunction(source)
        for d in destinations:
            edges.append((source, d))

end_node = None
for s, d in edges:
    if d not in modules:
        modules[d] = UnTyped(d)
        end_node = d
    modules[s].set_next(modules[d])
    modules[d].add_parent(modules[s])


def press(broadcaster):
    queue = list(broadcaster)
    low, high = 1, 0

    while len(queue) > 0:
        signal = queue.pop(0)
        if isinstance(signal, str):
            print(f"broadcaster -low -> {signal}")
            low += 1
            modules[signal].input(None, False)
            queue.append(modules[signal])
        elif isinstance(signal, FlipFlop):
            # flush the buffer to next states
            for n in signal.next:
                for status in signal.transmission_buffer:
                    print(
                        f"pub {signal.name} -{'high' if status else 'low'} -> {n.name}"
                    )
                    high += 1 if status else 0
                    low += 1 if not status else 0
                    n.input(signal, status)
                    queue.append(n)
            signal.transmission_buffer = []
        elif isinstance(signal, Conjunction):
            # flush the buffer to next states
            for n in signal.next:
                for status in signal.transmission_buffer:
                    print(
                        f"pub {signal.name} -{'high' if status else 'low'} -> {n.name}"
                    )
                    high += 1 if status else 0
                    low += 1 if not status else 0
                    n.input(signal, status)
                    queue.append(n)
            signal.transmission_buffer = []

    return low, high


# low = 0
# high = 0
# for _ in range(3):
#     l, h = press(broadcaster)
#     low += l
#     high += h
#     print(l, h)
# print(low, high, low * high)

label_dict = dict()
label_dict["BROAD"] = "BROAD"
node_values = {n: 1 for n in modules.keys()}
node_values["BROAD"] = 1

for k, v in modules.items():
    label_dict[k] = v.name + "_" + v.kind
G = nx.DiGraph()
G.add_edges_from([("BROAD", n) for n in broadcaster] + edges)
nx.draw(G, labels=label_dict, with_labels=True)

paths = list(nx.all_simple_paths(G, "BROAD", end_node))

for path in paths:
    path = list(path)
    path.pop(0)
    s = path.pop(0)

    for d in path:
        print(s, d)
        # FLP to FLP -> 2X
        if modules[s].kind == "FLP" and modules[d].kind == "FLP":
            node_values[d] *= 2 * node_values[s]
        # CON to CON -> 2X
        elif modules[s].kind == "CON" and modules[d].kind == "CON":
            node_values[d] *= 2 * node_values[s]
        else:
            node_values[d] *= node_values[s]
        s = d
    # break
print(node_values)
# print(node_values[end_node])

plt.show()
