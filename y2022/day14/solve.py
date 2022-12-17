from AoC import AoC
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

minx, maxx, miny, maxy = (None, None, None, None)

def disp(grid):
    global minx, maxx, miny, maxy
    minx = min(grid.keys(), key=lambda k: k[0])[0]
    maxx = max(grid.keys(), key=lambda k: k[0])[0]+1
    miny = min(grid.keys(), key=lambda k: k[1])[1]
    maxy = max(grid.keys(), key=lambda k: k[1])[1]+1
    print(f'{minx, maxx, miny, maxy}')
    agrid = np.zeros((maxy-miny, maxx-minx), dtype=np.uint8)
    for ((x,y), z) in grid.items():
        agrid[y-miny,x-minx] = 1 if z == '#' else 2

    plt.imshow(agrid)

    x_positions = np.arange(0,agrid.shape[1])
    x_labels = np.arange(minx, maxx)
    plt.xticks(x_positions, x_labels)
    y_positions = np.arange(0,agrid.shape[0])
    y_labels = np.arange(miny, maxy)
    plt.yticks(y_positions, y_labels)

    plt.show()

def p1sand(grid, x, y):
    if y >= maxy:
        # grain fell into abyss
        return False
    elif (x, y+1) not in grid:
        return p1sand(grid, x, y+1)
    elif (x-1, y+1) not in grid:
        return p1sand(grid, x-1, y+1)
    elif (x+1, y+1) not in grid:
        return p1sand(grid, x+1, y+1)
    else:
        # grain at rest
        grid[(x,y)] = 'o'
        return True

def p2sand(grid, x, y):
    if y == maxy:
        # grain at rest on floor
        grid[(x,y)] = 'o'
        return True
    elif (x, y+1) not in grid:
        return p2sand(grid, x, y+1)
    elif (x-1, y+1) not in grid:
        return p2sand(grid, x-1, y+1)
    elif (x+1, y+1) not in grid:
        return p2sand(grid, x+1, y+1)
    else:
        # grain at rest
        grid[(x,y)] = 'o'
        return (x,y) != (500,0)


class Solver(AoC):
    example_data = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

    def parse(self):
        global minx, maxx, miny, maxy
        self.grid = {}
        raw = self.read_input_txt(split=True)
        for line in raw:
            line = line.strip()
            vertices = line.split(' -> ')
            prev = None
            for v in vertices:
                print(f'v: {v}, prev: {prev}')
                x, y = v.split(',')
                x = int(x)
                y = int(y)
                if not prev:
                    prev = (x,y)
                    continue
                if prev[0] != x:
                    d = 1 if x>=prev[0] else -1
                    for xx in range(prev[0], x+d, d):
                        self.grid[(xx,y)] = '#'
                else:
                    d = 1 if y>=prev[1] else -1
                    for yy in range(prev[1], y+d, d):
                        self.grid[(x,yy)] = '#'
                prev = (x,y)

        minx = min(self.grid.keys(), key=lambda k: k[0])[0]
        maxx = max(self.grid.keys(), key=lambda k: k[0])[0]+1
        miny = min(self.grid.keys(), key=lambda k: k[1])[1]
        maxy = max(self.grid.keys(), key=lambda k: k[1])[1]+1

        disp(self.grid)

    def part1(self):
        tot = 0
        start = (500,0)
        grid = deepcopy(self.grid)
        while p1sand(grid, *start):
            tot += 1
        disp(grid)
        return tot

    def part2(self):
        tot = 0
        start = (500,0)
        grid = deepcopy(self.grid)
        while p2sand(grid, *start):
            tot += 1
        disp(grid)
        return tot+1