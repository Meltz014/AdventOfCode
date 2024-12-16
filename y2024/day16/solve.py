from AoC import AoC
from queue import PriorityQueue
from collections import defaultdict
import numpy as np

class Solver(AoC):
    example_data = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

    def show_grid(self, grid):
        if self._debug:
            for y, row in enumerate(grid):
                for x, g in enumerate(row):
                    if g in self.grid_to_char:
                        c = self.grid_to_char[g]
                    else:
                        c = g
                        if c == 0xFFFFFFFF:
                            c = '#'
                    print(f" {c}", end="")
                print()

    def parse(self):
        grid = []
        self.start = None
        self.end = None
        self.dir = '>'
        self.WALL = -1
        self.PATH = 0
        self.END = 0
        self.char_to_grid = {
            '#': self.WALL,
            '.': self.PATH,
            'E': self.END,
        }
        self.grid_to_char = {
            self.WALL: '#',
            self.PATH: '.'
        }
        self.RIGHT = 0
        self.UP = 1
        self.LEFT = 2
        self.DOWN = 3
        self.dir_to_index = {
            '>': self.RIGHT,
            '^': self.UP,
            '<': self.LEFT,
            'v': self.DOWN
        }
        raw = self.read_input_txt()
        for y, line in enumerate(raw):
            grid.append([])
            for x, char in enumerate(line.strip()):
                if char == 'S':
                    self.start = (y, x, self.RIGHT)
                    g = self.PATH
                elif char == 'E':
                    self.end = (y, x)
                    g = self.END
                else:
                    g = self.char_to_grid[char]
                grid[y].append(g)
        self.bounds = (y,x)
        self.grid = np.array(grid, dtype=np.int64)
        #self.show_grid(self.grid)

    def iter_neighbors(self, source):
        max_y, max_x = self.grid.shape
        max_y -= 1
        max_x -= 1
        dir = source[2]
        if source[0] > 0:
            # up
            new_dir = self.UP
            if dir == new_dir:
                if self.grid[(source[0]-1, source[1])] != self.WALL:
                    yield source[0]-1, source[1], new_dir
            else:
                yield source[0], source[1], new_dir
        if source[1] > 0:
            # left
            new_dir = self.LEFT
            if dir == new_dir:
                if self.grid[(source[0], source[1]-1)] != self.WALL:
                    yield source[0], source[1]-1, new_dir
            else:
                yield source[0], source[1], new_dir
        if source[0] < max_y:
            # down
            new_dir = self.DOWN
            if dir == new_dir:
                if self.grid[(source[0]+1, source[1])] != self.WALL:
                    yield source[0]+1, source[1], new_dir
            else:
                yield source[0], source[1], new_dir
        if source[1] < max_x:
            # right
            new_dir = self.RIGHT
            if dir == new_dir:
                if self.grid[(source[0], source[1]+1)] != self.WALL:
                    yield source[0], source[1]+1, new_dir
            else:
                yield source[0], source[1], new_dir


    def dijkstra(self, source):
        dist = np.ones((*self.grid.shape, 4), dtype=np.uint32) * 0xFFFFFFFF
        dist[source] = 0
        pq = PriorityQueue()
        pq.put((0, source))

        # shortest path set
        to_visit = {}
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                if self.grid[y,x] != self.WALL:
                    for i in range(4):
                        to_visit[(y,x,i)] = 0
        prev = defaultdict(list)
        while not pq.empty():
            # vertex in spt with min dist
            (_, u) = pq.get()
            to_visit.pop(u, None)
            for v in self.iter_neighbors(u):
                dir = u[2]
                new_dir = v[2]
                if v not in to_visit:
                    continue
                if new_dir != dir:
                    alt = dist[u] + 1000
                else:
                    alt = dist[u] + 1
                if alt <= dist[v]:
                    dist[v] = alt
                    pq.put((alt, v))
                    prev[v].append(u)

        return dist, prev


    def part1(self):
        """
        BFS to find number of 9's reachable by each 0
        """
        dist, prev = self.dijkstra(self.start)
        self.dist = dist
        self.prev = prev
        #self.show_grid(dist[:10,-10::])
        #self.show_grid(dist)
        self.debug(dist[self.end])

        return min(dist[self.end])

    def part2(self):
        """
        """
        total_score = 0

        # need to iterate through prev to find number of unique cells on all shortest paths
        visited = set()

        def find_prev(u):
            for v in self.prev[u]:
                if v not in visited:
                    visited.add(v)
                    find_prev(v)

        end_dist = min(self.dist[self.end])
        end_dir = list(self.dist[self.end]).index(end_dist)
        print(f'end dir: {end_dir}')
        find_prev((*self.end, end_dir))
        prev_grid = self.grid.copy()
        for v in visited:
            prev_grid[v[0], v[1]] = 1


        self.show_grid(prev_grid)
        actual_visited = set([(v[0], v[1]) for v in visited])

        return len(actual_visited)+1
