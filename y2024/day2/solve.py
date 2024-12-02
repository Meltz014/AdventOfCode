from AoC import AoC
import numpy as np
from collections import Counter


def is_safe(row):
    diffs = np.diff(row)
    _safe = np.logical_or(np.all(diffs < 0), np.all(diffs > 0))
    # check for all diffs 0 < diff <= 3
    safe = np.logical_and(_safe, np.all(np.logical_and(np.abs(diffs) <= 3, np.abs(diffs) > 0)))
    return safe


class Solver(AoC):
    example_data = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

    def parse(self):
        self.raw = self.read_input_numeric(dtype=np.int64, split_rows=True)

    def part1(self):
        """
        Check diff for each row.  Numbers must be all increasing or all decreasing, but only by 1, 2, or 3.
        """

        # input rows are not the same shape, so we can't vectorize this
        total_safe = 0
        for row in self.raw:
            if is_safe(row):
                total_safe += 1

        return total_safe

    def part2(self):
        total_safe = 0
        for row in self.raw:
            if is_safe(row):
                total_safe += 1
            else:
                # if one level can be removed to make it safe, then we're safe
                # brute force because lazy
                for i in range(len(row)):
                    new_row = np.delete(row, i)
                    if is_safe(new_row):
                        total_safe += 1
                        break

        return total_safe
