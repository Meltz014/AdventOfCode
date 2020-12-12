from AoC import AoC

class Solver(AoC):
    example_data = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

    def parse(self):
        lines = self.read_input_txt()
        # build hill map
        # dict of (x, y) = true if tree
        self.hill = {}
        for (y, line) in enumerate(lines):
            for (x, t) in enumerate(line.strip()):
                self.hill[(x, y)] = t == '#'

        self.width = x+1
        self.height = y+1

    def solve_slope(self, slope):
        tree_count = 0
        x, y = 0, 0
        while y < self.height:
            tree_count += int(self.hill[x, y])
            x = (x + slope[0]) % self.width
            y += slope[1]
        return tree_count

    def part1(self):
        # find trees encounterd on slope of (3, 1)
        return self.solve_slope((3, 1))

    def part2(self):
        a = self.solve_slope((1, 1))
        b = self.solve_slope((3, 1))
        c = self.solve_slope((5, 1))
        d = self.solve_slope((7, 1))
        e = self.solve_slope((1, 2))
        return a * b * c * d * e