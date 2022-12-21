import numpy

class NotImplementedError(Exception):
    pass

class AoC():

    example_data = ""

    def __init__(self, day, use_example=False, debug=False):
        self._day = day
        self._debug = debug
        self._use_example = use_example

    def read_input_txt(self, split=True):
        if self._use_example:
            if self.example_data:
                # add \n to replicate behavior of fid.readlines()
                if split:
                    return [l + '\n' for l in self.example_data.splitlines()]
                else:
                    return self.example_data
            else:
                print('warning: no example data defined.  Using input.txt')
        with open(f'day{self._day}\input.txt') as fid:
            if split:
                return fid.readlines()
            else:
                return fid.read()

    def read_input_numeric(self, dtype=numpy.int64, sep='\n'):
        if self._use_example:
            if self.example_data:
                return numpy.fromstring(self.example_data, dtype=dtype, sep=sep)
            else:
                print('warning: no example data defined.  Using input.txt')
        return numpy.loadtxt(f'day{self._day}\input.txt', dtype=dtype, delimiter=sep)

    def parse(self):
        raise NotImplementedError()

    def part1(self):
        raise NotImplementedError()

    def part2(self):
        raise NotImplementedError()