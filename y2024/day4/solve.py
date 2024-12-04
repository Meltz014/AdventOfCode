from AoC import AoC
import re

class Solver(AoC):
    example_data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

    example_data_1 = """XMASQQSAMX
MMQQQQQQMM
AQAQQQQAQA
SQQSQQSQQS
QQQQQQQQQQ
QQQQQQQQQQ
SQQSQQSQQS
AQAQQQQAQA
MMQQQQQQMM
XMASQQSAMX"""

    example_data_2 = """SAMXQQXMAS
AAQQQQQQAA
MQMQQQQMQM
XQQXQQXQQX
QQQQQQQQQQ
QQQQQQQQQQ
XQQXQQXQQX
MQMQQQQMQM
AAQQQQQQAA
SAMXQQXMAS"""

    def parse(self):
        self.raw = self.read_input_txt()
        for (i, line) in enumerate(self.raw):
            self.raw[i] = line.strip()
        #self.debug(self.raw)

    def part1(self):
        """
        Need to search for "XMAS" in input data
        """
        total = 0
        for (i, line) in enumerate(self.raw):
            for (j, char) in enumerate(line):
                if char == "X":
                    # check horiz
                    if j <= len(line)-4 and line[j+1:j+4] == 'MAS':
                        total += 1
                        self.debug(i, j, 'H')
                    if j >= 3 and line[j-3:j] == 'SAM':
                        total += 1
                        self.debug(i, j, 'h')
                    # check vert
                    if i <= len(self.raw)-4 and self.raw[i+1][j] == 'M' and self.raw[i+2][j] == 'A' and self.raw[i+3][j] == 'S':
                        total += 1
                        self.debug(i, j, 'V')
                    if i >= 3 and self.raw[i-3][j] == 'S' and self.raw[i-2][j] == 'A' and self.raw[i-1][j] == 'M':
                        total += 1
                        self.debug(i, j, 'v')
                    # check diag
                    if i <= len(self.raw)-4 and j <= len(line)-4 and self.raw[i+1][j+1] == 'M' and self.raw[i+2][j+2] == 'A' and self.raw[i+3][j+3] == 'S':
                        total += 1
                        self.debug(i, j, 'DD')
                    if i >= 3 and j >= 3 and self.raw[i-3][j-3] == 'S' and self.raw[i-2][j-2] == 'A' and self.raw[i-1][j-1] == 'M':
                        total += 1
                        self.debug(i, j, 'dd')
                    # check diag
                    if i <= len(self.raw)-4 and j >= 3 and self.raw[i+1][j-1] == 'M' and self.raw[i+2][j-2] == 'A' and self.raw[i+3][j-3] == 'S':
                        total += 1
                        self.debug(i, j, 'Dd')
                    if i >= 3 and j <= len(line)-4 and self.raw[i-3][j+3] == 'S' and self.raw[i-2][j+2] == 'A' and self.raw[i-1][j+1] == 'M':
                        total += 1
                        self.debug(i, j, 'dD')

        return total

    def part2(self):
        """
        Need to search for "MAS" in the shape of an X
        """

        total = 0
        for (i, line) in enumerate(self.raw):
            for (j, char) in enumerate(line):
                if char == "A" and i >= 1 and j >= 1 and i < len(self.raw)-1 and j < len(line) - 1:
                    if self.raw[i-1][j-1] == 'M' and self.raw[i-1][j+1] == 'M' and self.raw[i+1][j-1] == 'S' and self.raw[i+1][j+1] == 'S':
                        total += 1
                        self.debug(i,j,'1')
                    if self.raw[i-1][j-1] == 'S' and self.raw[i-1][j+1] == 'M' and self.raw[i+1][j-1] == 'S' and self.raw[i+1][j+1] == 'M':
                        total += 1
                        self.debug(i,j,'2')
                    if self.raw[i-1][j-1] == 'S' and self.raw[i-1][j+1] == 'S' and self.raw[i+1][j-1] == 'M' and self.raw[i+1][j+1] == 'M':
                        total += 1
                        self.debug(i,j,'3')
                    if self.raw[i-1][j-1] == 'M' and self.raw[i-1][j+1] == 'S' and self.raw[i+1][j-1] == 'M' and self.raw[i+1][j+1] == 'S':
                        total += 1
                        self.debug(i,j,'4')
        return total
