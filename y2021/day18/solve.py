from AoC import AoC
import numpy as np
from math import ceil, floor

class SnailFish:
    def __init__(self, line_list, root=None):
        self.root = root
        if isinstance(line_list[0], list):
            self.left = SnailFish(line_list[0], root=self)
        else:
            self.left = line_list[0]
        if isinstance(line_list[1], list):
            self.right = SnailFish(line_list[1], root=self)
        else:
            self.right = line_list[1]

    def to_list(self):
        l = []
        if isinstance(self.left, int):
            l.append(self.left)
        else:
            l.append(self.left.to_list())
        if isinstance(self.right, int):
            l.append(self.right)
        else:
            l.append(self.right.to_list())
        return l

    def __add__(self, other):
        return SnailFish([self.to_list(), other.to_list()])

    @property
    def depth(self):
        if not self.root:
            return 0
        else:
            return self.root.depth + 1

    @property
    def magnitude(self):
        if isinstance(self.left, int):
            l = self.left
        else:
            l = self.left.magnitude
        if isinstance(self.right, int):
            r = self.right
        else:
            r = self.right.magnitude
        return l*3 + r*2

    def is_reduced(self):
        if self.depth >= 4:
            return False
        l = True
        r = True
        if isinstance(self.left, int):
            if self.left >= 10:
                l = False
        else:
            l = self.left.is_reduced()
        if isinstance(self.right, int):
            if self.right >= 10:
                r = False
        else:
            r = self.right.is_reduced()
        return l and r

def explode(sf):
    # explode to left
    cur = sf.root
    last = sf
    up = True
    while cur:
        if up:
            if cur.left is last:
                last = cur
                cur = cur.root
            elif isinstance(cur.left, int):
                cur.left += sf.left
                break
            else: # cur.right is last
                cur = cur.left
                up = False
        else:
            # first node on the right
            if isinstance(cur.right, int):
                cur.right += sf.left
                break
            else:
                cur = cur.right
    # explode to right
    cur = sf.root
    last = sf
    up = True
    while cur:
        if up:
            if cur.right is last:
                last = cur
                cur = cur.root
            elif isinstance(cur.right, int):
                cur.right += sf.right
                break
            else: # cur.left is last
                cur = cur.right
                up = False
        else:
            # first node on the left
            if isinstance(cur.left, int):
                cur.left += sf.right
                break
            else:
                cur = cur.left
    # replace with 0
    root = sf.root
    if root.right is sf:
        root.right = 0
    else:
        root.left = 0
    del sf

def split(num, root):
    return SnailFish([floor(num/2), ceil(num/2)], root=root)

def reduce(sf):
    while not sf.is_reduced():
        if not reduce_explode(sf):
            reduce_split(sf)

def reduce_explode(sf):
    if isinstance(sf.left, int) and isinstance(sf.right, int) and sf.depth >= 4:
        explode(sf)
        return True
    else:
        r = False
        if isinstance(sf.left, SnailFish):
            if reduce_explode(sf.left):
                return True
        if isinstance(sf.right, SnailFish):
            r = reduce_explode(sf.right)
        return r

def reduce_split(sf):
    l = False
    if isinstance(sf.left, int):
        if sf.left >= 10:
            sf.left = split(sf.left, sf)
            l = True
    else:
        l = reduce_split(sf.left)
    if l:
        return True
    r = False
    if isinstance(sf.right, int):
        if sf.right >= 10:
            sf.right = split(sf.right, sf)
            r = True
    else:
        r = reduce_split(sf.right)
    return r


class Solver(AoC):
    example_data = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

    example_datax = """[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]"""

    def parse(self):
        raw = self.read_input_txt()
        self.snail_fish = []
        for line in raw:
            line_list = eval(line)
            self.snail_fish.append(SnailFish(line_list))

    def part1(self):
        root = self.snail_fish[0]
        for sf in self.snail_fish[1:]:
            root = root + sf
            reduce(root)
            #input()

        return root.magnitude

    def part2(self):
        # get max mag by adding 2 sf's
        ans = 0
        for sf in self.snail_fish:
            for sf2 in self.snail_fish:
                if sf is not sf2:
                    the_sum = sf + sf2
                    reduce(the_sum)
                    m = the_sum.magnitude
                    if m > ans:
                        ans = m
        return ans