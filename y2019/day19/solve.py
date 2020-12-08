import numpy
import os
from collections import defaultdict
from y2019.intcode import CPU, Halted

def print_grid(grid):
    x_size = max(grid, key=lambda x: x[0])[0] + 1
    y_size = max(grid, key=lambda x: x[1])[1] + 1
    #os.system('cls')
    for row in range(y_size):
        print(''.join(str(grid[(col, row)]) for col in range(x_size)))

def get_point(cpu, x, y):
    cpu.queue_input(x)
    cpu.queue_input(y)
    try:
        cpu.exec(pc=0)
    except Halted:
        pass
    val = cpu.get_output()
    cpu.reset()
    return val

def main():
    # part 1
    memory_ = numpy.loadtxt(r'day19\input_mine.txt', delimiter=',', dtype=numpy.int64)
    # darkgray answer: 379 981
    memory = numpy.array(memory_, copy=True)
    cpu = CPU(memory)
    grid = defaultdict(int)
    for x in range(100):
        for y in range(100):
            grid[(x,y)] = get_point(cpu, x, y)
            #print(f'{(x, y)}: {val}')
    print_grid(grid)
    count = sum(v for v in grid.values())
    print(f'Part 1: {count}')

    ##### part 2
    yprime = 99
    xprime = 99

    x = 0
    y = 0

    bl = 0
    tr = 0

    while True:
        bl = get_point(cpu, x, y+yprime)
        tr = get_point(cpu, x+xprime, y)

        if bl and tr:
            print(f'Part 2: {(x, y)}')
            break
        # iterate x
        while bl == 0:
            x += 1
            bl = get_point(cpu, x, y+yprime)
        # iterate y
        while tr == 0:
            y += 1
            tr = get_point(cpu, x+xprime, y)


if __name__ == '__main__':
    main()
