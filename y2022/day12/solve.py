from AoC import AoC
from queue import PriorityQueue
import numpy as np
import matplotlib.pyplot as plt

class Solver(AoC):
    example_data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

    def iter_neighbors(self, source):
        max_y, max_x = self.grid.shape
        max_y -= 1
        max_x -= 1
        if source[0] > 0:
            # up
            new = source[0]-1, source[1]
            if self.grid[new] - self.grid[source] <= 1:
                yield new
        if source[1] > 0:
            # left
            new = source[0], source[1]-1
            if self.grid[new] - self.grid[source] <= 1:
                yield new
        if source[0] < max_y:
            # down
            new = source[0]+1, source[1]
            if self.grid[new] - self.grid[source] <= 1:
                yield new
        if source[1] < max_x:
            # right
            new = source[0], source[1]+1
            if self.grid[new] - self.grid[source] <= 1:
                yield new


    def my_first_dijkstra(self, source):
        dist = np.ones(self.grid.shape, dtype=np.uint16) * 0xFFFF
        dist[source] = 0
        pq = PriorityQueue()
        pq.put((0, source))

        # shortest path set
        to_visit = {}
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                to_visit[(y,x)] = 0
        while not pq.empty():
            # vertex in spt with min dist
            (_, u) = pq.get()
            to_visit.pop(u)
            #print(u)
            #plt.imshow(dist)
            #plt.show()

            for v in self.iter_neighbors(u):
                #if v not in to_visit:
                #    continue
                alt = dist[u] + 1
                #if v == self.end:
                #    print(f'END: {v}, {alt}')
                if alt < dist[v]:
                    dist[v] = alt
                    pq.put((alt, v))

        return dist

    def parse(self):
        raw = self.read_input_txt(split=True)
        self.grid = []
        self.start = None
        self.end = None
        for (row, line) in enumerate(raw):
            line = line.strip()
            self.grid.append([])
            for (col, c) in enumerate(line):
                if c == 'S':
                    self.start = (row, col)
                    val = ord('a')
                elif c == 'E':
                    self.end = (row, col)
                    val = ord('z')
                else:
                    val = ord(c)
                self.grid[-1].append(val)

        self.grid = np.array(self.grid, dtype=np.int64)
        plt.imshow(self.grid)
        plt.show()

    def part1(self):
        dist = self.my_first_dijkstra(self.start)
        dist[dist==0xFFFF] = dist[dist!=0xFFFF].max()
        plt.imshow(dist)
        plt.show()

        return dist[self.end]

    def part2(self):

        min_dist = 0xFFFF

        print(np.sum(self.grid[:,0]==ord('a')))
        candidates = []
        # need to find viable starting positions
        # uh, just use left 8 columns

        for start in list(zip(*np.where(self.grid[:,:8]==ord('a')))):
            dist = self.my_first_dijkstra(start)
            if dist[self.end] < min_dist:
                min_dist = dist[self.end]

        return min_dist