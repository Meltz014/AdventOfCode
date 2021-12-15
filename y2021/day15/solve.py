from AoC import AoC
from queue import PriorityQueue
from collections import defaultdict
import numpy as np

class Solver(AoC):
    example_data = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

    def parse(self):
        raw = self.read_input_txt()
        grid_list = []
        for line in raw:
            grid_list.append([])
            for c in line.strip('\n'):
                grid_list[-1].append(int(c))

        self.grid = np.array(grid_list, dtype=np.uint8)

    def iter_neighbors(self, source):
        max_y, max_x = self.grid.shape
        max_y -= 1
        max_x -= 1
        if source[0] > 0:
            # up
            yield source[0]-1, source[1]
        if source[1] > 0:
            # left
            yield source[0], source[1]-1
        if source[0] < max_y:
            # down
            yield source[0]+1, source[1]
        if source[1] < max_x:
            # right
            yield source[0], source[1]+1
            

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
            for v in self.iter_neighbors(u):
                if v not in to_visit:
                    continue
                alt = dist[u] + self.grid[v]
                if alt < dist[v]:
                    dist[v] = alt
                    pq.put((alt, v))

        return dist


    def part1(self):
        dist = self.my_first_dijkstra((0,0))
        return dist[-1, -1]

    def part2(self):
        # need to tile grid 5x5
        # all dist values increase by 1, then x%10 sorta
        new_grid = self.grid.copy()
        tile = self.grid.copy()
        for i in range(4):
            tile += 1
            tile %= 10
            tile[tile==0] = 1
            new_grid = np.concatenate((new_grid, tile), axis=1)
        tile = new_grid.copy()
        for i in range(4):
            tile += 1
            tile %= 10
            tile[tile==0] = 1
            new_grid = np.concatenate((new_grid, tile), axis=0)

        self.grid = new_grid
        dist = self.my_first_dijkstra((0,0))
        return dist[-1, -1]
