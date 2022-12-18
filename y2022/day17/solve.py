from AoC import AoC
import numpy as np
import itertools
import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
#fig, ax = plt.subplots()


"""
####
"""
a = (np.array([0,0,0,0], dtype=np.int32), np.array([2,3,4,5], dtype=np.int32))
"""
.#.
###
.#.
"""
b = (np.array([0,1,1,1,2], dtype=np.int32), np.array([3,2,3,4,3], dtype=np.int32))
"""
..#
..#
###
"""
c = (np.array([0,0,0,1,2], dtype=np.int32), np.array([2,3,4,4,4], dtype=np.int32))
"""
#
#
#
#
"""
d = (np.array([0,1,2,3], dtype=np.int32), np.array([2,2,2,2], dtype=np.int32))
"""
##
## 
"""
e = (np.array([0,0,1,1], dtype=np.int32), np.array([2,3,2,3], dtype=np.int32))

pieces = itertools.cycle([a,b,c,d,e])
chunk = 1024

def draw(grid, piece=None, dx=None, dy=None):
    gc = grid.copy()
    if piece:
        gc[piece[0]+dy, piece[1]+dx] = 1
    rocks = np.where(gc)
    maxy = max(rocks[0])+1
    #print()
    plt.imshow(np.flip(gc[0:maxy,:], axis=0))
    plt.show()

def get_heights(grid, h):
    dh = []
    for i in range(grid.shape[1]):
        where = np.where(grid[:,i])[0]
        if where.size:
            dh.append(h-np.max(where))
        else:
            dh.append(h)
    return dh

class Solver(AoC):
    example_data = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        self.inst = list(raw[0].strip())
        self.grid = np.zeros((chunk,7), dtype=bool)

    def calc_height(self, n):
        ((h0, n0), (h1, n1)) = self.repeat

        (repititions, rem) = divmod((n - n0), (n1 - n0))
        h = (h1 - h0) * repititions + h0
        h += sum(self.dh[n0:n0+rem])
        return h

    def push(self, piece, jet, dx, dy):
        if jet == '<':
            ddx = -1
        else:
            ddx = 1
        if self._debug:
            print(f'push {jet}')
        if np.any((piece[1]+dx+ddx)<0) or np.any((piece[1]+dx+ddx)>6) or np.any(self.grid[piece[0]+dy, piece[1]+dx+ddx]):
            return dx
        return dx + ddx

    def fall(self, piece, dy, dx):
        if np.any(piece[0]+dy-1<0) or np.any(self.grid[piece[0]+dy-1, piece[1]+dx]):
            return False
        if self._debug:
            print('Fall')
        return True

    def part1(self):
        jets = itertools.cycle(self.inst)
        lj = len(self.inst)
        ji = 0
        dh = []
        h = 0
        prevh = 0
        states = {} # (ji, pi, dh0,...dh6): (h, n)
        self.repeat = None
        for i in range(100000):
            piece = next(pieces)
            pi = i % 5

            # check if state has been visited
            if h > 0:
                state = (ji, pi, *get_heights(self.grid, h))
                if state in states:
                    # repeat was found.  Log repeat start and end locations
                    self.repeat = (states[state], (h, i))
                    break
                else:
                    states[state] = (h, i)

            # add 3 to height
            dy = 3 + h
            dx = 0
            while True:
                jet = next(jets)
                ji += 1
                ji %= lj
                dx = self.push(piece, jet, dx, dy)
                if self._debug:
                    draw(self.grid, piece, dx, dy)
                if self.fall(piece, dy, dx):
                    dy -= 1
                    if self._debug:
                        draw(self.grid, piece, dx, dy)
                else:
                    break

            self.grid[piece[0] + dy, piece[1] + dx] = 1
            if self._debug:
                print('stop')
                draw(self.grid)
            h = np.max(np.where(self.grid)[0])+1

            if i==0:
                dh.append(h)
            else:
                dh.append(h-prevh)
            prevh = h

            if h > self.grid.shape[0]-15:
                self.grid = np.concatenate((self.grid, np.zeros_like(self.grid)), axis=0)
                print(f'New alloc {self.grid.shape}')
        self.dh = dh
        return self.calc_height(2022)

    def part2(self):
        return self.calc_height(1000000000000)