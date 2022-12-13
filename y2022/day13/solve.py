from AoC import AoC
from itertools import zip_longest
import re

class StupidWrapperClass():
    def __init__(self, data):
        self.data = data

    def __lt__(self, other):
        return compare(self.data, other.data)

    def __eq__(self, other):
        if isinstance(other, list):
            return self.data == other
        else:
            return self.data == other.data


def compare(left, right, debug=False):
    if debug:
        print(f'L: {left}\nR: {right}')
    if isinstance(left, int) and isinstance(right, int):
        # both ints
        return left < right
    elif left is None:
        # left runs out first
        return True
    elif right is None:
        # right runs out first
        return False
    elif isinstance(left, int):
        left = [left]
    elif isinstance(right, int):
        right = [right]

    for (l, r) in zip_longest(left, right):
        if l != r:
            return compare(l, r, debug=debug)

class Solver(AoC):
    example_data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        self.packets = []
        while raw:
            l = raw.pop(0).strip()
            r = raw.pop(0).strip()
            left = eval(l)
            right = eval(r)
            self.packets.append((left, right))
            if raw:
                raw.pop(0)

    def part1(self):
        tot = 0
        for (i, (left, right)) in enumerate(self.packets):
            if compare(left, right, debug=False):
                tot += (i+1)
        return tot

    def part2(self):
        flat_packets = [[[2]],[[6]]]
        for left, right in self.packets:
            flat_packets.append(left)
            flat_packets.append(right)

        wrapped_packets = [StupidWrapperClass(packet) for packet in flat_packets]

        s = sorted(wrapped_packets)
        i0 = s.index([[2]])+1
        i1 = s.index([[6]])+1
        return i0*i1