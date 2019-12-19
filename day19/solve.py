import numpy
import os
from collections import defaultdict
from intcode import CPU, Halted

def print_grid(grid):
    x_size = max(grid, key=lambda x: x[0])[0] + 1
    y_size = max(grid, key=lambda x: x[1])[1] + 1
    os.system('cls')
    for row in range(y_size):
        print(''.join(str(grid[(col, row)]) for col in range(x_size)))


def main():
    # part 1
    memory_ = numpy.loadtxt(r'day19\input.txt', delimiter=',', dtype=numpy.int64)
    #memory = numpy.array(memory_, copy=True)
    #cpu = CPU(memory)
    #cpu.background_exec()

    grid = defaultdict(int)

    memory = numpy.array(memory_, copy=True)
    cpu = CPU(memory)
    for x in range(50):
        for y in range(50):
            cpu.queue_input(x)
            cpu.queue_input(y)
            try:
                cpu.exec(pc=0)
            except Halted:
                pass
            val = cpu.get_output()
            cpu.reset()
            grid[(x,y)] = val
            #print(f'{(x, y)}: {val}')

    print_grid(grid)

    count = sum(v for v in grid.values())
    print(f'Part 1: {count}')


if __name__ == '__main__':
    main()
