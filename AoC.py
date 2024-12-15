import numpy

class NotImplementedError(Exception):
    pass

class AoC():

    example_data = ""

    def __init__(self, day, use_example=False, debug=False):
        self._day = day
        self._debug = debug
        self._use_example = use_example
        self.is_part_2 = False

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

    def read_input_numeric(self, dtype=numpy.int64, sep='\n', split_rows=False):
        if self._use_example:
            if self.example_data:
                if split_rows:
                    return [numpy.fromstring(l, dtype=dtype, sep=sep) for l in self.example_data.splitlines()]
                else:
                    return numpy.fromstring(self.example_data, dtype=dtype, sep=sep)
            else:
                print('warning: no example data defined.  Using input.txt')
        with open(f'day{self._day}\input.txt', 'r') as fid:
            if split_rows:
                return [numpy.fromstring(l, dtype=dtype, sep=sep) for l in fid.readlines()]
            else:
                txt = fid.read()
                return numpy.fromstring(txt, dtype=dtype, sep=sep)

    def parse(self):
        raise NotImplementedError()

    def part1(self):
        raise NotImplementedError()

    def part2(self):
        raise NotImplementedError()
    
    def debug(self, *args, **kwargs):
        if self._debug:
            print(*args, **kwargs)