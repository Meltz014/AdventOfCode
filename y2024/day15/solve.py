from AoC import AoC
from tqdm import tqdm
import numpy as np

class Solver(AoC):
    example_data = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

    example_data_1 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

    def show_grid(self):
        if self._debug:
            for y, row in enumerate(self.grid):
                for x, g in enumerate(row):
                    if self.is_part_2:
                        if g == self.BOX:
                            c = '['
                        else:
                            c = self.grid_to_char[g]
                    else:
                        c = self.grid_to_char[g]
                    print(f" {c}", end="")
                print()

    def parse(self):
        self.WALL = 1
        self.BOX = 2
        self.BOXR = 3
        self.BOT = 4
        self.char_to_grid = {
            '#': self.WALL,
            'O': self.BOX,
            '[': self.BOX,
            ']': self.BOXR,
            '@': self.BOT,
            '.': 0
        }
        self.grid_to_char = {
            self.WALL: '#',
            self.BOX: 'O',
            self.BOXR: ']',
            self.BOT: '@',
            0: '.'
        }
        self.dir_dict = {
            '^': (-1, 0),
            '>': (0, 1),
            'v': (1, 0),
            '<': (0, -1)
        }
        self.tqdm_total = 0
        grid = []
        self.start = None
        self.instructions = ''
        raw = self.read_input_txt()
        for y, line in enumerate(raw):
            if line.strip() == '':
                break
            grid.append([])
            for x, char in enumerate(line.strip()):
                g = self.char_to_grid[char]
                if g == self.BOT:
                    self.start = (y,x)
                grid[y].append(g)
        self.bounds = (y,x)

        for line in raw[y+1:]:
            self.instructions += line.strip()

        # put in numpy
        self.grid = np.array(grid, dtype=np.uint8)
        self.show_grid()

    def parse2(self):
        grid = []
        self.start = None
        raw = self.read_input_txt()
        for y, line in enumerate(raw):
            if line.strip() == '':
                break
            grid.append([])
            for x, char in enumerate(line.strip()):
                g = self.char_to_grid[char]
                if g == self.BOT:
                    self.start = (y,x*2)
                    gg = 0
                if g == self.BOX:
                    gg = self.BOXR
                if g == self.WALL:
                    gg = self.WALL
                if g == 0:
                    gg = 0
                grid[y].append(g)
                grid[y].append(gg)
        self.grid = np.array(grid, dtype=np.uint8)
        self.show_grid()

    def move_easy(self, y, x, dir):
        cur = self.grid[y,x]
        if cur == self.WALL:
            return False
        if cur == 0:
            return True
        dy, dx = self.dir_dict[dir]
        if self.move_easy(y+dy, x+dx, dir):
            self.grid[y,x] = 0
            self.grid[y+dy, x+dx] = cur
            return True
        return False
    
    def move_hard(self, y, x, dir):
        # dir will only be ^ or v
        dy, dx = self.dir_dict[dir]
        cur = self.grid[y,x]
        if cur == self.WALL:
            return False
        if cur == 0:
            return True
        if cur == self.BOX: # left box
            # need to check here and to the right
            l = self.move_hard(y+dy, x+dx, dir)
            r = self.move_hard(y+dy, x+dx+1, dir)
            return l and r
        if cur == self.BOXR: # right box
            # need to check here and to the left
            r = self.move_hard(y+dy, x+dx, dir)
            l = self.move_hard(y+dy, x-1+dx, dir)
            return l and r
        if cur == self.BOT:
            return self.move_hard(y+dy, x+dx, dir)

    def move_hard_propogate(self, y, x, dir):
        # only gets called if the move is known to be good
        dy, dx = self.dir_dict[dir]
        cur = self.grid[y,x]
        if cur == 0:
            return
        if cur == self.BOX: # left box
            # need to check here and to the right
            self.move_hard_propogate(y+dy, x+dx, dir)
            self.move_hard_propogate(y+dy, x+dx+1, dir)
            self.grid[y, x:x+2] = 0
            self.grid[y+dy, x:x+2] = [self.BOX, self.BOXR]
            return
        if cur == self.BOXR: # right box
            # need to check here and to the left
            self.move_hard_propogate(y+dy, x+dx, dir)
            self.move_hard_propogate(y+dy, x-1+dx, dir)
            self.grid[y, x-1:x+1] = 0
            self.grid[y+dy, x-1:x+1] = [self.BOX, self.BOXR]
            return
        if cur == self.BOT:
            self.move_hard_propogate(y+dy, x+dx, dir)
            self.grid[y, x] = 0
            self.grid[y+dy, x+dx] = self.BOT


    def sum_gps(self):
        tot = 0
        for y, row in enumerate(self.grid):
            for x, g in enumerate(row):
                if g == self.BOX:
                    tot += (y*100 + x)
        return tot

    def part1(self):
        """
        BFS to find number of 9's reachable by each 0
        """
        y, x = self.start
        for dir in self.instructions:
            if self.move_easy(y, x, dir):
                dy, dx = self.dir_dict[dir]
                y += dy
                x += dx

        self.show_grid()

        return self.sum_gps()

    def part2(self):
        """
        """
        self.parse2()

        y, x = self.start
        for dir in self.instructions:
            if dir in '<>':
                if self.move_easy(y, x, dir):
                    dy, dx = self.dir_dict[dir]
                    y += dy
                    x += dx
            else:
                if self.move_hard(y, x, dir):
                    self.move_hard_propogate(y, x, dir)
                    dy, dx = self.dir_dict[dir]
                    y += dy
                    x += dx

        self.show_grid()

        return self.sum_gps()
