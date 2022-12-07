from AoC import AoC
import os

class Node():
    def __init__(self, name, parent, size=0):
        self.name = name
        self.parent = parent
        self.children = []
        self.size = size
        self.update_size()

    def update_size(self):
        parent = self.parent
        while parent:
            parent.size += self.size
            parent = parent.parent

    @property
    def path(self):
        # recurse to root
        if not self.parent:
            return '/'
        return f'{self.parent.path}/{self.name}'

    def __str__(self):
        _str = f'{self.path}: {self.size}'
        for c in self.children:
            _str += '\n' + str(c)
        return _str


class Solver(AoC):
    example_data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        tree = Node('/', None, 0)
        cwd = tree
        for line in raw:
            line = line.strip()
            if line[0] == '$':
                if 'cd' in line:
                    if '..' in line:
                        cwd = cwd.parent
                    else:
                        dirname = line.split('cd ')[1]
                        if dirname == '/':
                            cwd = tree
                        else:
                            new = Node(dirname, cwd, 0)
                            cwd.children.append(new)
                            cwd = new
            else:
                if 'dir' in line:
                    continue
                (size, fname) = line.split(' ')
                cwd.children.append(Node(fname, cwd, int(size)))

        self.tree = tree

    def part1(self):
        """
        find dirs at MOST 100000
        find sum of those
        """
        tot = 0

        def summit(tree):
            nonlocal tot
            if tree.size <= 100000:
                tot += tree.size
            for sub in tree.children:
                if sub.children:
                    # only count dirs (where children are non-empty)
                    summit(sub)
        summit(self.tree)
        return tot


    def part2(self):
        """
        Smallest dir to free up at least 30000000
        """
        # ok, need to recalculate root size
        #self.tree[0] = 0
        #for (name, thing) in self.tree[1].items():
        #    if isinstance(thing, list):
        #        self.tree[0] += thing[0]
        #    else:
        #        self.tree[0] += thing
        print(f'Used space: {self.tree.size}')
        free = 70000000 - self.tree.size
        print(f'Free space: {free}')
        enough = 30000000 - free
        print(f'Needed space = {enough}')
        cur_min = 70000000
        def search(tree):
            nonlocal cur_min
            if tree.size >= enough and tree.size < cur_min:
                cur_min = tree.size
            for sub in tree.children:
                if sub.children:
                    # only count dirs (where children are non-empty)
                    search(sub)
        search(self.tree)
        return cur_min