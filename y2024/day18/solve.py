from AoC import AoC
from itertools import zip_longest
from tqdm import tqdm
import numpy as np
from queue import PriorityQueue


class Solver(AoC):
    example_data = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

    def show_grid(self, grid):
        if self._debug:
            for y, row in enumerate(grid):
                for x, char in enumerate(row):
                    print(f" {char}", end="")
                print()

    def parse(self):
        self.tqdm_total = 0
        self.bytes = []
        raw = self.read_input_txt()
        for line in raw:
            xx, yy = line.strip().split(',')
            self.bytes.append((int(yy), int(xx)))

    def iter_neighbors(self, grid, source):
        max_y, max_x = grid.shape
        max_y -= 1
        max_x -= 1
        if source[0] > 0:
            # up
            if grid[source[0]-1, source[1]] == 0:
                yield source[0]-1, source[1]
        if source[1] > 0:
            # left
            if grid[source[0], source[1]-1] == 0:
                yield source[0], source[1]-1
        if source[0] < max_y:
            # down
            if grid[source[0]+1, source[1]] == 0:
                yield source[0]+1, source[1]
        if source[1] < max_x:
            # right
            if grid[source[0], source[1]+1] == 0:
                yield source[0], source[1]+1


    def dijkstra(self, grid, source):
        dist = np.ones(grid.shape, dtype=np.uint16) * 0xFFFF
        dist[source] = 0
        pq = PriorityQueue()
        pq.put((0, source))

        # shortest path set
        to_visit = {}
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                to_visit[(y,x)] = 0
        while not pq.empty():
            # vertex in spt with min dist
            (_, u) = pq.get()
            to_visit.pop(u)
            for v in self.iter_neighbors(grid, u):
                if v not in to_visit:
                    continue
                alt = dist[u] +1
                if alt < dist[v]:
                    dist[v] = alt
                    pq.put((alt, v))

        return dist


    def part1(self):
        """
        BFS to find number of 9's reachable by each 0
        """
        if self._use_example:
            shape = (7,7)
            keep_bytes = 12
        else:
            shape = (71, 71)
            keep_bytes = 1024

        grid = np.zeros(shape, np.uint8)
        self.debug(grid)
        for i in range(keep_bytes):
            self.debug(self.bytes[i])
            grid[self.bytes[i]] = 1

        dist = self.dijkstra(grid, (0,0))

        return dist[-1,-1]

    def does_path_exist(self, byte_i):
        if self._use_example:
            shape = (7,7)
            keep_bytes = byte_i
        else:
            shape = (71, 71)
            keep_bytes = byte_i

        grid = np.zeros(shape, np.uint8)
        self.debug(grid)
        for i in range(keep_bytes):
            self.debug(self.bytes[i])
            grid[self.bytes[i]] = 1

        dist = self.dijkstra(grid, (0,0))
        return dist[-1,-1] < 0xFFFF

    def part2(self):
        """
        """
        total_score = 0
        # Need to binary search through all coords to find the byte that kills it
        start = 1024
        end = len(self.bytes) - 1
        points_tried = set()
        while True:
            next_byte = start + (end - start) // 2
            if next_byte in points_tried:
                break
            points_tried.add(next_byte)
            if self.does_path_exist(next_byte):
                start = next_byte
            else:
                end = next_byte

        return self.bytes[next_byte][1], self.bytes[next_byte][0]
