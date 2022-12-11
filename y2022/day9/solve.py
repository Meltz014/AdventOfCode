from AoC import AoC
import re

def move_head(hpos, d):
    if d == 'R':
        hpos[0] += 1
    elif d == 'L':
        hpos[0] -= 1
    if d == 'U':
        hpos[1] += 1
    if d == 'D':
        hpos[1] -= 1


def move_tail(hpos, tpos):
    dx = hpos[0] - tpos[0]
    dy = hpos[1] - tpos[1]

    mx = False
    my = False
    if (abs(dx) + abs(dy)) > 2:
        mx = True
        my = True
    elif abs(dx) > 1:
        mx = True
    elif abs(dy) > 1:
        my = True
    if mx:
        if dx > 0:
            tpos[0] += 1
        else:
            tpos[0] -= 1
    if my:
        if dy > 0:
            tpos[1] += 1
        else:
            tpos[1] -= 1

class Solver(AoC):
    example_data = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        self.inst = []
        for line in raw:
            (d,x) = line.strip().split()
            self.inst.append((d,int(x)))

    def part1(self):
        tot = 0
        visited = set()
        hpos = [0,0]
        tpos = [0,0]
        for (d, dist) in self.inst:
            for i in range(dist):
                move_head(hpos, d)
                move_tail(hpos, tpos)
                visited.add(tuple(tpos))
        return len(visited)

    def part2(self):
        tot = 0
        visited = set()
        knots = [
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0]
        ]
        for (d, dist) in self.inst:
            for i in range(dist):
                move_head(knots[0], d)
                for i in range(len(knots[:-1])):
                    move_tail(knots[i], knots[i+1])
                visited.add(tuple(knots[-1]))

        return len(visited)