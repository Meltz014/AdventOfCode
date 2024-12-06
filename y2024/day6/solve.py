from AoC import AoC

class Solver(AoC):
    example_data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    def show_grid(self):
        for y in range(self.bounds[1] + 1):
            for x in range(self.bounds[0] + 1):
                if (x, y) == self.start:
                    print('@', end='')
                elif (x, y) in self.grid:
                    print(self.grid[(x, y)], end='')
                elif (x, y) in self.visited:
                    print(self.visited[(x, y)], end='')
                else:
                    print('.', end='')
            print()

    def parse(self):
        self.grid = {}
        self.start = None
        raw = self.read_input_txt()
        for y, line in enumerate(raw):
            for x, char in enumerate(line.strip()):
                if char == '^':
                    self.start = (x, y)
                    self.grid[(x,y)] = '^'
                elif char == '#':
                    self.grid[(x, y)] = char
        self.debug(self.start)
        self.debug(self.grid)
        self.bounds = (x, y)

    def part1(self):
        """
        Determine area of visited grid locations

        -1, 0 -> 0, 1
        0, 1 -> 1, 0
        1, 0 -> 0, -1
        0, -1 -> -1, 0

        """
        total = 1 # Account for starting position
        direction = (0, -1)
        self.visited = {self.start: '^'}
        pos = self.start
        while True:
            step = pos[0] + direction[0], pos[1] + direction[1]
            if step[0] > self.bounds[0] or step[1] > self.bounds[1] or step[0] < 0 or step[1] < 0:
                break
            cur = self.grid.get(step)
            if cur == '#':
                # rotate 90 deg to right
                direction = (-direction[1], direction[0])
            else:
                cur = self.visited.get(step)
                pos = step
                if not cur:
                    total += 1
                    if direction == (-1, 0):
                        c = '<'
                    elif direction == (0, -1):
                        c = '^'
                    elif direction == (1, 0):
                        c = '>'
                    elif direction == (0, 1):
                        c = 'v'
                    self.visited[step] = c

        if self._debug:
            self.show_grid()
        return total

    def part2(self):
        """
        """
        char_to_dir = {
            '^': (0, -1),
            '>': (1, 0),
            'v': (0, 1),
            '<': (-1, 0)
        }
        dir_to_char = {
            (0, -1): '^',
            (1, 0): '>',
            (0, 1): 'v',
            (-1, 0): '<'
        }
        total = 0
        new_visited_template = {}
        for new_obs in self.visited:
            if new_obs == self.start:
                continue
            new_visited_template[new_obs] = self.visited[new_obs]
            direction = char_to_dir[self.visited[new_obs]]
            new_visited = new_visited_template.copy()
            pos = new_obs[0] - direction[0], new_obs[1] - direction[1]
            while True:
                step = pos[0] + direction[0], pos[1] + direction[1]
                if step[0] > self.bounds[0] or step[1] > self.bounds[1] or step[0] < 0 or step[1] < 0:
                    # exited map.  Not a loop
                    break
                cur = self.grid.get(step)
                if cur == '#' or step == new_obs:
                    # rotate 90 deg to right
                    direction = (-direction[1], direction[0])
                else:
                    cur = new_visited.get(step)
                    pos = step
                    if cur:
                        if (
                            (direction == (-1, 0) and cur == "<")
                            or (direction == (0, -1) and cur == "^")
                            or (direction == (1, 0) and cur == ">")
                            or (direction == (0, 1) and cur == "v")
                        ):
                            # found a loop
                            total += 1
                            break
                    else:
                        if direction == (-1, 0):
                            c = '<'
                        elif direction == (0, -1):
                            c = '^'
                        elif direction == (1, 0):
                            c = '>'
                        elif direction == (0, 1):
                            c = 'v'
                        new_visited[step] = c

        return total
