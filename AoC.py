import numpy

class NotImplementedError(Exception):
    pass

class AoC():

    example_data = ""

    def __init__(self, day, use_example=False):
        self._day = day
        self._use_example = use_example

    def read_input_txt(self):
        if self._use_example:
            if self.example_data:
                # add \n to replicate behavior of fid.readlines()
                return [l + '\n' for l in self.example_data.splitlines()]
            else:
                print('warning: no example data defined.  Using input.txt')
        with open(f'day{self._day}\input.txt') as fid:
            return fid.readlines()

    def read_input_numeric(self, dtype=numpy.int64):
        if self._use_example:
            if self.example_data:
                return numpy.fromstring(self.example_data, dtype=dtype, sep='\n')
            else:
                print('warning: no example data defined.  Using input.txt')
        return numpy.loadtxt(f'day{self._day}\input.txt', dtype=dtype)

    def parse(self):
        raise NotImplementedError()

    def part1(self):
        raise NotImplementedError()

    def part2(self):
        raise NotImplementedError()