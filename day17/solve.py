import numpy
import os
import threading
import time
from collections import defaultdict
from intcode import CPU, Halted
import matplotlib.pyplot as plt
from matplotlib import colors
from queue import Queue, Empty

N = 1
S = 2
W = 3
E = 4

REVERSE = {
    N: S,
    E: W,
    W: E,
    S: N
}

ROT_R = {
    N: E,
    E: S,
    S: W,
    W: N
}

ROT_L = {
    N: W,
    W: S,
    S: E,
    E: N
}

SCAF = ord('#')

def print_grid(grid):
    x_size = max(grid, key=lambda x: x[0])[0] + 1
    y_size = max(grid, key=lambda x: x[1])[1] + 1
    os.system('cls')
    for row in range(y_size):
        print(''.join(chr(grid[(col, row)]) for col in range(x_size)))

def find_intersections(grid):
    max_x = max(grid, key=lambda x: x[0])[0]
    max_y = max(grid, key=lambda x: x[1])[1]

    for y in range(1, max_y): # exclude borders
        for x in range(1, max_x):
            if grid[(x, y)] == SCAF:
                # if 4 adjacent spots are scaffold
                if grid[(x-1, y)] == SCAF and grid[(x+1, y)] == SCAF and grid[(x, y-1)] == SCAF and grid[(x, y+1)] == SCAF:
                    yield (x,y)

def main():
    # part 1
    memory_ = numpy.loadtxt(r'day17\input.txt', delimiter=',', dtype=numpy.int64)
    memory = numpy.array(memory_, copy=True)
    cpu = CPU(memory)
    cpu.background_exec()

    grid = defaultdict(lambda:ord('.'))
    (x, y) = (0, 0)

    bot_loc = (0,0)

    while True:
        try:
            val = cpu.get_output(block=True)
            if val == 10:
                # new row
                x = 0
                y += 1
                #print_grid(grid)
                continue
            if val == ord('^'):
                bot_loc = (x, y)
            grid[(x,y)] = val
            x += 1
        except Halted:
            print('Program Halted')
            break

    print(f'Part 1: {sum( x*y for (x,y) in find_intersections(grid))}')

    ### part 2:
    sub_a = 'R,8,L,4,R,4,R,10,R,8\n'
    sub_b = 'L,12,L,12,R,8,R,8\n'
    sub_c = 'R,10,R,4,R,4\n'
    main_routine = 'A,A,B,C,B,C,B,C,C,A\n'

    memory = numpy.array(memory_, copy=True)
    memory[0] = 2 # set to override mode
    cpu = CPU(memory)

    # queue inputs
    for c in main_routine + sub_a + sub_b + sub_c + 'n\n':
        cpu.queue_input(ord(c))

    # run
    cpu.exec()

    while True:
        try:
            space_dust = cpu.get_output()
        except (Empty, Halted):
            break
    print(f'Part 2: {space_dust}')


if __name__ == '__main__':
    main()
