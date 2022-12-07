from AoC import AoC
import os
from pprint import pprint as print

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
        files = []
        tree = [0, {}]
        cwd = tree
        path = ''
        for (i, line) in enumerate(raw):
            line = line.strip()
            if line[0] == '$':
                if 'cd' in line:
                    print(line)
                    if '..' in line:
                        path = os.path.split(path[:-1])[0]
                        cwd = tree
                        if len(path) > 1:
                            path += '/'
                            print(('cd .. ', path, path.split('/')[1:-1]))
                            for d in path.split('/')[1:-1]:
                                cwd = cwd[1][d]
                    else:
                        dirname = line.split('cd ')[1]
                        print(dirname)
                        if dirname == '/':
                            path = '/'
                        else:
                            cwd[1][dirname] = [0, {}]
                            cwd = cwd[1][dirname]
                            path = path + f'{dirname}/'
                    print(f'>> {path}')
            else:
                if 'dir' in line:
                    continue
                (size, fname) = line.split(' ')
                cwd[1][fname] = int(size)
                cwd[0] += int(size)
                # need to update parents too
                if len(path) > 1:
                    c = tree
                    for d in path.split('/')[1:-2]:
                        c = c[1][d]
                        c[0] += int(size)


        print(tree)
        self.tree = tree

    def part1(self):
        """
        find dirs at MOST 100000
        find sum of those
        """
        tot = 0

        def summit(tree):
            nonlocal tot
            if tree[0] <= 100000:
                tot += tree[0]
            for (name, sub) in tree[1].items():
                if isinstance(sub, list):
                    summit(sub)
        summit(self.tree)
        return tot


    def part2(self):
        """
        Smallest dir to free up at least 30000000
        """
        # ok, need to recalculate root size
        self.tree[0] = 0
        for (name, thing) in self.tree[1].items():
            if isinstance(thing, list):
                self.tree[0] += thing[0]
            else:
                self.tree[0] += thing
        print(f'Used space: {self.tree[0]}')
        free = 70000000 - self.tree[0]
        print(f'Free space: {free}')
        enough = 30000000 - free
        print(f'Needed space = {enough}')
        cur_min = 70000000
        def search(tree):
            nonlocal cur_min
            if tree[0] >= enough and tree[0] < cur_min:
                cur_min = tree[0]
            for (name, sub) in tree[1].items():
                if isinstance(sub, list):
                    search(sub)
        search(self.tree)
        return cur_min