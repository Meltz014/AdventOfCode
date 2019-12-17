import numpy
from collections import defaultdict
from intcode import CPU, Halted

HIT_WALL = 0
MOVED_FWD = 1
TARGET_FOUND = 2

UNKNOWN = -1
EMPTY = 0
WALL = 1
TARGET = 2


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

def plot(maze, cur_x, cur_y):
    import matplotlib.pyplot as plt
    from matplotlib import colors

    minx = min(maze, key=lambda x: x[0])[0]
    maxx = max(maze, key=lambda x: x[0])[0]
    miny = min(maze, key=lambda x: x[1])[1]
    maxy = max(maze, key=lambda x: x[1])[1]

    grid = numpy.ones((maxy-miny+1, maxx-minx+1), dtype=numpy.int8) * UNKNOWN
    for ((x, y), val) in maze.items():
        grid[y-miny, x-minx] = val

    grid[cur_y-miny, cur_x-minx] = 3 # cursor position

    # make a color map of fixed colors
    cmap = colors.ListedColormap(['gray', 'white', 'black', 'red', 'blue'])
    bounds=[-1.5,-0.5,0.5,1.5,2.5,3.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    img = plt.imshow(grid, interpolation='nearest', origin='upper',
                     cmap=cmap, norm=norm)
    #plt.show()
    plt.pause(0.01)

def step(x, y, direction):
    if direction == N:
        y -= 1
    elif direction == S:
        y += 1
    elif direction == W:
        x -= 1
    else: # E
        x += 1

    return (x,y)

def check_right(cpu, facing):
    cpu.queue_input(ROT_R[facing])
    stat = cpu.get_output(block=True)
    if stat == MOVED_FWD:
        # move successful.  Mark as empty
        neighbor = EMPTY
        # move back
        cpu.queue_input(ROT_L[facing])
        assert cpu.get_output(block=True) == MOVED_FWD
    elif stat == HIT_WALL:
        # mark as wall
        neighbor = WALL
    elif stat == TARGET_FOUND:
        # mark as target
        neighbor = TARGET
    return neighbor

def check_left(cpu, facing):
    cpu.queue_input(ROT_L[facing])
    stat = cpu.get_output(block=True)
    if stat == MOVED_FWD:
        # move successful.  Mark as empty
        neighbor = EMPTY
        # move back
        cpu.queue_input(ROT_R[facing])
        assert cpu.get_output(block=True) == MOVED_FWD
    elif stat == HIT_WALL:
        # mark as wall
        neighbor = WALL
    elif stat == TARGET_FOUND:
        # mark as target
        neighbor = TARGET
    return neighbor

def check_fwd(cpu, facing):
    cpu.queue_input(facing)
    stat = cpu.get_output(block=True)
    if stat == MOVED_FWD:
        # move successful.  Mark as empty
        neighbor = EMPTY
        # move back
        cpu.queue_input(REVERSE[facing])
        assert cpu.get_output(block=True) == MOVED_FWD
    elif stat == HIT_WALL:
        # mark as wall
        neighbor = WALL
    elif stat == TARGET_FOUND:
        # mark as target
        neighbor = TARGET
    return neighbor

def check_neighbors(cpu, facing):
    left = check_left(cpu, facing)
    fwd = check_fwd(cpu, facing)
    right = check_right(cpu, facing)
    return (left, fwd, right)

def maze_worker(cpu, facing, maze, pos):
    (x, y) = pos
    while True:
        try:
            (left, fwd, right) = check_neighbors(cpu, facing)
            maze[step(x, y, ROT_R[facing])] = right
            maze[step(x, y, ROT_L[facing])] = left
            maze[step(x, y, facing)] = fwd
            plot(maze, x, y)
            if right == TARGET:
                print(f'Target found! {step(x, y, ROT_R[facing])}')
                break
            elif left == TARGET:
                print(f'Target found! {step(x, y, ROT_L[facing])}')
                break
            elif fwd == TARGET:
                print(f'Target found! {step(x, y, facing)}')
                break

            if right != WALL:
                facing = ROT_R[facing]
            elif (fwd == WALL) and (left != WALL):
                facing = ROT_L[facing]
            elif (fwd == WALL) and (left == WALL):
                facing = REVERSE[facing]

            cpu.queue_input(facing)
            assert cpu.get_output(block=True) == MOVED_FWD
            (x, y) = step(x, y, facing)
        except Halted:
            print('halted')
            break

def main():
    # part 1
    memory_ = numpy.loadtxt(r'day15\gaiwecoor.txt', delimiter=',', dtype=numpy.int64)
    memory = numpy.array(memory_, copy=True)
    cpu = CPU(memory)
    cpu.background_exec()

    maze = defaultdict(int)
    (x, y) = (0, 0)
    facing = N
    left = None
    right = None
    fwd = None
    maze[(x, y)] = EMPTY
    while True:
        try:
            (left, fwd, right) = check_neighbors(cpu, facing)
            maze[step(x, y, ROT_R[facing])] = right
            maze[step(x, y, ROT_L[facing])] = left
            maze[step(x, y, facing)] = fwd
            plot(maze, x, y)
            if right == TARGET:
                print(f'Target found! {step(x, y, ROT_R[facing])}')
                break
            elif left == TARGET:
                print(f'Target found! {step(x, y, ROT_L[facing])}')
                break
            elif fwd == TARGET:
                print(f'Target found! {step(x, y, facing)}')
                break


            if right != WALL:
                facing = ROT_R[facing]
            elif (fwd == WALL) and (left != WALL):
                facing = ROT_L[facing]
            elif (fwd == WALL) and (left == WALL):
                facing = REVERSE[facing]

            cpu.queue_input(facing)
            assert cpu.get_output(block=True) == MOVED_FWD
            (x, y) = step(x, y, facing)
        except Halted:
            print('halted')
            break



if __name__ == '__main__':
    main()
