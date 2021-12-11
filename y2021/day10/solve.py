from AoC import AoC
import numpy as np

OPEN = '[({<'
CLOSE = '])}>'
O_TO_C = {'[': ']', '{': '}', '(': ')', '<': '>'}
SCORE = {')': 3, ']': 57, '}': 1197, '>': 25137}
SCORE_2 = {')': 1, ']': 2, '}': 3, '>': 4}

class Solver(AoC):
    example_data = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


    def parse(self):
        self.lines = self.read_input_txt()

    def part1(self):
        tot_score = 0
        self.incomplete_lines = [] # (line, stack)
        for line in self.lines:
            line = line.strip('\n')
            stack = []
            invalid = ''
            for c in line:
                if c in OPEN:
                    stack.append(c)
                if c in CLOSE:
                    o = stack.pop()
                    if c != O_TO_C[o]:
                        invalid = c
                        break
            if invalid:
                tot_score += SCORE[invalid]
            else:
                self.incomplete_lines.append((line, stack))
        return tot_score

    def part2(self):
        scores = []
        for (line, stack) in self.incomplete_lines:
            score = 0
            completion = ''.join([O_TO_C[s] for s in stack[::-1]])
            for c in completion:
                score *= 5
                score += SCORE_2[c]
            scores.append(score)

        scores.sort()
        print(scores)
        return scores[(len(scores)//2)]