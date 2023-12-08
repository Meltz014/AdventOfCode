from AoC import AoC
import numpy as np

class Solver(AoC):
    example_data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

    example_data_1 = """12.......*..
+.........34
.......-12..
..78........
..*....60...
78..........
.......23...
....90*12...
............
2.2......12.
.*.........*
1.1.......56"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        self.board = {
            'nums': {}, # {row: {num: [col, col, col]}}
            'parts': []
        }
        for (row, line) in enumerate(raw):
            num = ''
            num_coords = []
            for (col, c) in enumerate(line.strip()):
                if c.isnumeric():
                    num += c
                    num_coords.append(col)
                else:
                    if num:
                        if row not in self.board['nums']:
                            self.board['nums'][row] = []
                        self.board['nums'][row].append((int(num), num_coords))
                        num_coords = []
                        num = ''
                    if c == '.':
                        continue
                    else:
                        self.board['parts'].append((c, (row, col)))
            if num:
                if row not in self.board['nums']:
                    self.board['nums'][row] = []
                self.board['nums'][row].append((int(num), num_coords))
                num_coords = []
                num = ''

        print(self.board)


    def part1(self):
        valid = []
        self.part_index = {} # symbol: {(row, col): [list of part adj. part nums]}
        for (part, (row, col)) in self.board['parts']:
            if part not in self.part_index:
                self.part_index[part] = {}
            valid_for_this_part = []
            self.part_index[part][(row, col)] = valid_for_this_part
            for i in range(-1, 2):
                if i == -1 and row == 0:
                    continue
                if i == 1 and row == max(self.board['nums']):
                    continue
                if row + i not in self.board['nums']:
                    continue
                part_nums_to_check = self.board['nums'][row+i]

                for (part_num, pnum_cols) in part_nums_to_check:
                    for pnum_col in pnum_cols:
                        if pnum_col in range(col-1, col+2):
                            # pnum is adjacent to part
                            valid.append(part_num)
                            valid_for_this_part.append(part_num)
                            break

        print(valid)
        return sum(valid)

    def part2(self):
        gear_ratios = 0
        for (coords, parts) in self.part_index['*'].items():
            if len(parts) == 2:
                ratio = parts[0] * parts[1]
                gear_ratios += ratio
        return gear_ratios
