from abc import abstractmethod

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
    def __init__(self, name) -> None:
        self.parents = dict()
        self.next: list[Node] = list()
        self.name = name
        self.transmission_buffer = []

    @abstractmethod
    def input(self, parent, high):
        pass

    def add_parent(self, parent: "Node"):
        self.parents[parent] = False

    def set_next(self, node: "Node"):
        if node not in self.next:
            self.next.append(node)


class FlipFlop(Node):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.status = False

    def input(self, parent, high):
        if not high:
            self.status = not self.status
            self.transmission_buffer += [self.status]


class Conjunction(Node):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.parents: dict[Node, bool] = dict()

    def input(self, parent, high):
        self.parents[parent] = high
        if all(self.parents.values()):
            self.transmission_buffer.append(False)
        else:
            self.transmission_buffer.append(True)


class UnTyped(Node):
    def __init__(self, name) -> None:
        super().__init__(name)

    def input(self, parent, high):
        pass

    def add_parent(self, parent: "Node"):
        pass

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

for s, d in edges:
    if d in modules:
        modules[s].set_next(modules[d])
        modules[d].add_parent(modules[s])
    else:
        modules[s].set_next(UnTyped(d))


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


low = 0
high = 0
for _ in range(1000):
    l, h = press(broadcaster)
    low += l
    high += h
    print()
print(low, high, low * high)
