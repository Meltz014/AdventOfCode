from AoC import AoC
import numpy as np

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.is_big = self.name.isupper()

    def link(self, child):
        self.children.append(child)
        self.children.sort(key=lambda n: n.name)
        child.children.append(self)
        child.children.sort(key=lambda n: n.name)

    def unlink(self, child):
        self.children.remove(child)
        child.children.remove(self)

    def __repr__(self):
        c_names = ','.join([c.name for c in self.children])
        return f'Node({self.name} -> {c_names})'

class Solver(AoC):

    example_data = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

    example_data_1 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

    def parse(self):
        raw = self.read_input_txt()
        self.root = Node('start')
        self.all_nodes = {'start': self.root}
        for line in raw:
            a,b = line.strip('\n').split('-')
            n_a = self.all_nodes.get(a)
            if not n_a:
                n_a = Node(a)
                self.all_nodes[a] = n_a
            n_b = self.all_nodes.get(b)
            if not n_b:
                n_b = Node(b)
                self.all_nodes[b] = n_b
            n_a.link(n_b)
        self.end = self.all_nodes['end']
        #print(self.all_nodes)

    def path_to_end(self, node, path=None, dupe=None):
        """returns the valid paths from given node to end"""
        path = path if path else []
        paths = []
        if node is self.end:
            return [path + ['end']]
        for child in node.children:
            if child.is_big or child.name not in path or (child is dupe and path.count(child.name) < 2):
                paths += self.path_to_end(child, path + [node.name], dupe=dupe)
        return paths

    def part1(self):
        paths = self.path_to_end(self.root)
        #print(paths)
        return len(paths)

    def part2(self):
        paths_found = []
        for node in self.all_nodes.values():
            if node.is_big or (node in [self.root, self.end]):
                continue
            paths = self.path_to_end(self.root, dupe=node)
            paths_found += ['-'.join(p) for p in paths]

        return len(set(paths_found))