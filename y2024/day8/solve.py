from AoC import AoC
from itertools import combinations
from tqdm import tqdm

class Solver(AoC):
    example_data = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

    def show_grid(self, antinodes):
        for y in range(self.size[1] + 1):
            for x in range(self.size[0] + 1):
                if (y,x ) in antinodes:
                    print('X', end='')
                else:
                    print('.', end='')
            print()
        print('======================================')
        for y in range(self.size[1] + 1):
            for x in range(self.size[0] + 1):
                a = False
                for (ant_type, antennas) in self.antennas.items():
                    if (y,x ) in antennas:
                        print(ant_type, end='')
                        a = True
                if not a:
                    print('.', end='')
            print()


    def parse(self):
        self.tqdm_total = 0
        self.antennas = {}
        raw = self.read_input_txt()
        for y, line in enumerate(raw):
            for x, char in enumerate(line.strip()):
                if char != '.':
                    if char not in self.antennas:
                        self.antennas[char] = []
                    self.antennas[char].append((y,x))
        for char in self.antennas:
            self.tqdm_total += len(list(combinations(self.antennas[char], r=2)))

        self.size = (y,x)

    def is_in_bounds(self, y, x):
        return y >= 0 and x >=0 and y <= self.size[0] and x <= self.size[1]
    def part1(self):
        """
        count unique antinodes
        """
        antinodes = set()
        #pbar = tqdm(total=self.tqdm_total)
        for antenna_type, antennas in self.antennas.items():
            for ((y1, x1),(y2, x2)) in combinations(antennas, r=2):
                # compute antinodes
                self.debug(f'combo {antenna_type} {y1, x1}, {y2, x2}')
                dy, dx = y2-y1, x2-x1
                ay, ax = y1-dy, x1-dx
                self.debug(f'dydx {dy, dx}')
                if self.is_in_bounds(ay, ax):
                    antinodes.add((ay, ax))
                ay, ax = y2+dy, x2+dx
                if self.is_in_bounds(ay, ax):
                    antinodes.add((ay, ax))
                #pbar.update(1)
        #pbar.close()

        self.show_grid(antinodes)
        return len(antinodes)

    def part2(self):
        """
        """
        antinodes = set()
        #pbar = tqdm(total=self.tqdm_total)
        for antenna_type, antennas in self.antennas.items():
            for ((y1, x1),(y2, x2)) in combinations(antennas, r=2):
                # compute antinodes
                self.debug(f'combo {antenna_type} {y1, x1}, {y2, x2}')
                antinodes.add((y1, x1))
                antinodes.add((y2, x2))
                dy, dx = y2-y1, x2-x1
                ay, ax = y1-dy, x1-dx
                self.debug(f'dydx {dy, dx}')
                while self.is_in_bounds(ay, ax):
                    antinodes.add((ay, ax))
                    ay, ax = ay-dy, ax-dx
                ay, ax = y2+dy, x2+dx
                while self.is_in_bounds(ay, ax):
                    antinodes.add((ay, ax))
                    ay, ax = ay+dy, ax+dx
                #pbar.update(1)
        #pbar.close()
        self.show_grid(antinodes)

        return len(antinodes)
