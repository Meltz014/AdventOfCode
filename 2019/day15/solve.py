import numpy
import threading
import time
from collections import defaultdict
from intcode import CPU, Halted
import matplotlib.pyplot as plt
from matplotlib import colors
from queue import Queue

do_plot = False

target_node = None

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

target_found_sig = False

plot_q = Queue()

def plot(maze, cur_x, cur_y, show=False):
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
    if show:
        plt.imshow(grid, interpolation='nearest', origin='upper', cmap=cmap, norm=norm)
        ax = plt.gca()
        ax.set_xticks(numpy.arange(0, maxx-minx+1, 1), minor=True)
        ax.set_yticks(numpy.arange(0, maxy-miny+1, 1), minor=True)
        ax.grid(which='minor', color='y', linestyle='-', linewidth=1)
        plt.show()
    else:
        args = (grid, )
        kwargs = dict(interpolation='nearest', origin='upper', cmap=cmap, norm=norm)
        plot_q.put((args, kwargs))

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

def maze_worker(cpu, facing, maze, root_node, pos):
    global target_found_sig
    global target_node
    (x, y) = pos
    threads = []
    target_found = False
    while True:
        try:
            time.sleep(0)
            (left, fwd, right) = check_neighbors(cpu, facing)
            maze[step(x, y, ROT_R[facing])] = right
            maze[step(x, y, ROT_L[facing])] = left
            maze[step(x, y, facing)] = fwd
            if do_plot:
                plot(maze, x, y)
            if right == TARGET:
                print(f'Target found! {step(x, y, ROT_R[facing])}')
                target_found = True
                break
            elif left == TARGET:
                print(f'Target found! {step(x, y, ROT_L[facing])}')
                target_found = True
                break
            elif fwd == TARGET:
                print(f'Target found! {step(x, y, facing)}')
                target_found = True
                break

            if (right == WALL) and (fwd == WALL) and (left == WALL):
                # dead end.  Die
                print(f'Dead end found at {(x, y)}')
                break

            open_count = sum([left!=WALL, fwd!=WALL, right!=WALL])

            f_t = True
            if right != WALL:
                # queue next move
                new_facing = ROT_R[facing]
            elif fwd != WALL:
                new_facing = facing
                f_t = False
            elif left != WALL:
                new_facing = ROT_L[facing]

            if open_count > 1:
                # create threads for fwd &/or left
                cpu.stop()
                if left != WALL:
                    print('creating left thread')
                    left_cpu = cpu.copy()
                    left_cpu.background_exec(pc=left_cpu.pc)
                    _facing = ROT_L[facing]
                    left_cpu.queue_input(_facing)
                    assert left_cpu.get_output(block=True) == MOVED_FWD
                    _pos = step(x, y, _facing)
                    left_node = MazeNode(parent=root_node, length=1)
                    root_node.left = left_node
                    root_node.right = MazeNode(parent=root_node)
                    root_node = root_node.right
                    left_thread = threading.Thread(target=maze_worker, args=(left_cpu, _facing, maze, left_node, _pos))
                    left_thread.start()
                    threads.append(left_thread)
                if f_t and fwd != WALL:
                    print('creating fwd thread')
                    fwd_cpu = cpu.copy()
                    fwd_cpu.background_exec(pc=fwd_cpu.pc)
                    fwd_cpu.queue_input(facing)
                    assert fwd_cpu.get_output(block=True) == MOVED_FWD
                    _pos = step(x, y, facing)
                    left_node = MazeNode(parent=root_node, length=1)
                    root_node.left = left_node
                    root_node.right = MazeNode(parent=root_node)
                    root_node = root_node.right
                    fwd_thread = threading.Thread(target=maze_worker, args=(fwd_cpu, facing, maze, left_node, _pos))
                    fwd_thread.start()
                    threads.append(fwd_thread)

                # resume CPU exec
                cpu.background_exec(pc=cpu.pc)

            facing = new_facing
            cpu.queue_input(facing)
            assert cpu.get_output(block=True) == MOVED_FWD
            (x, y) = step(x, y, facing)
            root_node.length += 1
        except Halted:
            print('halted')
            break
        except Exception as e:
            print(f'unknown exception {e}')
            target_found_sig = True
            plot_q.put(None)
            #raise e

    if target_found:
        root_node.length += 1
        if not target_node:
            target_node = root_node
    for t in threads:
        print(f'joining {t}')
        t.join()

def fill_down(node):
    l_len = 0
    r_len = 0
    if node.left:
        l_len = fill_down(node.left)
    if node.right:
        r_len = fill_down(node.right)

    return node.length + max(l_len, r_len)

def fill_up(node):
    d_len = 0
    u_len = 0
    if node.parent:
        u_len = fill_up(node.parent)
        if node is node.parent.left:
            d_len = fill_down(node.parent.right)
        elif node is node.parent.right:
            d_len = fill_down(node.parent.left)

    return max(u_len, d_len) + node.length

class MazeNode():
    def __init__(self, parent=None, length=0):
        self.length=length
        self.left = None
        self.right = None
        self.parent = parent

def main():
    # part 1
    memory_ = numpy.loadtxt('day15\input.txt', delimiter=',', dtype=numpy.int64)
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

    root_node = MazeNode()

    root_thread = threading.Thread(target=maze_worker, args=(cpu, facing, maze, root_node, (x, y)))
    root_thread.start()

    first = True
    if do_plot:
        while True:
            task = plot_q.get()
            if task:
                args, kwargs = task
                plt.imshow(*args, **kwargs)
                #plt.pause(0.0001)
                if first:
                    plt.show(block=False)
                    first == False
                else:
                    plt.draw()
                time.sleep(0)
            else:
                break
                print('plot kill')

    root_thread.join()
    test = target_node
    steps = 0
    while test:
        steps += test.length
        test = test.parent
    print(f'part 1: {steps}')
    plot(maze, 0, 0, show=True)

    print(target_node)

    ### part 2
    print(f'Part 2: {fill_up(target_node)}')

# 540 too high

if __name__ == '__main__':
    main()
