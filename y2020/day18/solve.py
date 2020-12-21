import numpy
from collections import defaultdict
from AoC import AoC
import re

class Solver(AoC):
    example_data = """2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

    def parse(self):
        lines = self.read_input_txt()

        self.homework = []

        def parse_line(items):
            hw = []
            i = 0
            while i < len(items):
                c = items[i]
                if c.isnumeric():
                    hw.append(int(c))
                elif c in '+*':
                    hw.append(c)
                elif c == '(':
                    (ii, item) = parse_line(items[i+1:])
                    i += ii+1
                    hw.append(item)
                    continue
                elif c == ')':
                    return (i+1, hw)
                i += 1
            return (i, hw)

        for line in lines:
            line = line.strip().replace(' ', '')
            items = [c for c in re.split(r'(\d+|[+*\(\)])', line) if c]
            (_, hw) = parse_line(items)
            self.homework.append(hw)


    def part1(self):

        def eval_line(hw):
            tot = 0
            op = '+'
            for item in hw:
                if isinstance(item, int):
                    tot = tot+item if op == '+' else tot*item
                elif isinstance(item, str):
                    op = item
                else:
                    # nested list
                    tot = tot+eval_line(item) if op == '+' else tot*eval_line(item)
            return tot

        total = 0
        for (i, hw) in enumerate(self.homework):
            answer = eval_line(hw)
            total += answer
        return total

    def part2(self):
        def eval_line(hw):
            tot = 0
            op = '+'
            for (i, item) in enumerate(hw):
                if isinstance(item, int):
                    if op == '+':
                        tot = tot + item
                    else:
                        tot = tot * eval_line(hw[i:])
                        return tot
                elif isinstance(item, str):
                    op = item
                else:
                    # nested list
                    if op == '+':
                        tot = tot+eval_line(item)
                    else:
                        tot = tot*eval_line(hw[i:])
                        return tot
            return tot

        total = 0
        for (i, hw) in enumerate(self.homework):
            answer = eval_line(hw)
            total += answer
        return total
        
