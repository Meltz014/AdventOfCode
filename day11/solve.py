import numpy
import matplotlib.pyplot as plt
from collections import defaultdict
from intcode import CPU, Halted

BLACK = 0
WHITE = 1

COCLOCK = 0
CLOCK = 1

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class DirState():
    def __init__(self):
        self.coclock = None
        self.clock = None

    def rotate(self, direction):
        if direction == CLOCK:
            return self.clock
        else:
            return self.coclock

up = DirState()
right = DirState()
down = DirState()
left = DirState()

up.coclock = left
up.clock = right
right.coclock = up
right.clock = down
down.coclock = right
down.clock = left
left.coclock = down
left.clock = up

def main():
    # part 1
    memory_ = numpy.loadtxt('day11\input.txt', delimiter=',', dtype=numpy.int64)

    memory = numpy.array(memory_, copy=True)
    cpu = CPU(memory)
    cpu.background_exec()

    (x, y) = (0, 0)
    panels = defaultdict(lambda: BLACK)
    facing = up
    loop_count = 0
    panels[(x,y)] = BLACK
    while (not cpu.done): # and (len(panels) < 400):
        #print(f'input: {panels[(x,y)]}')
        loop_count += 1
        if not loop_count % 1000:
            print(loop_count)
        try:
            cpu.queue_input(panels[(x,y)])
            color = cpu.get_output(block=True)
            #print(f'{color}')
            direction = cpu.get_output(block=True)
            #print(f'{direction}')
        except Halted:
            print('Program done')
            break

        panels[(x,y)] = color

        # rotate
        facing = facing.rotate(direction)

        # move forward
        if facing is up:
            y -= 1
        elif facing is right:
            x += 1
        elif facing is down:
            y += 1
        elif facing is left:
            x -= 1

    #print(f'Part 1: {len(panels)}')
    min_x = min(panels, key=lambda p: p[0])[0]
    max_x = max(panels, key=lambda p: p[0])[0]
    min_y = min(panels, key=lambda p: p[1])[1]
    max_y = max(panels, key=lambda p: p[1])[1]

    img = numpy.zeros((max_y+1-min_y, max_x+1-min_x), dtype=numpy.uint8)
    for (panel, color) in panels.items():
        img[panel[1], panel[0]] = color
    #plt.imshow(img)
    #plt.show()
    print(panels)


if __name__ == '__main__':
    main()
