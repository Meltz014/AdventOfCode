import numpy
import matplotlib.pyplot as plt
from collections import defaultdict
from intcode import CPU, Halted

WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

def main():
    # part 1
    memory_ = numpy.loadtxt('day13\input.txt', delimiter=',', dtype=numpy.int64)
    memory = numpy.array(memory_, copy=True)
    cpu = CPU(memory)
    cpu.background_exec()

    screen = defaultdict(lambda: 0)

    while True:
        try:
            x = cpu.get_output(block=True)
            y = cpu.get_output(block=True)
            val = cpu.get_output(block=True)
            screen[(x,y)] = val
            print(f'({x}, {y}) {val}')
        except Halted:
            print('halted')
            break

    blocks = len([i for i in screen.values() if i == BLOCK])
    print(f'Part 1: {blocks}')

    memory = numpy.array(memory_, copy=True)
    memory[0] = 2
    # hack to make paddle the whole width
    memory[1608:1652] = 3
        
    cpu = CPU(memory)
    for i in range(10000):
        cpu.queue_input(0)
    screen = defaultdict(lambda: 0)

    cpu.background_exec()
    score = 0
    while True:
        try:
            x = cpu.get_output(block=True)
            y = cpu.get_output(block=True)
            val = cpu.get_output(block=True)
            if (x == -1) and (y == 0):
                score = val
            #screen[(x,y)] = val
            #print(f'({x}, {y}) {val}')
        except Halted:
            print('halted')
            break

    print(f'Part 2: {score}')


if __name__ == '__main__':
    main()
