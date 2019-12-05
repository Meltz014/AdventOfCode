import numpy
import itertools
debug = False
# opcodes
HALT = 99
ADD = 1
MUL = 2

def handle_add(memory, pc):
    (left, right, out) = memory[pc+1:pc+4]
    if debug:
        print(f'Add {left}: {memory[left]}, {right}: {memory[right]}')
    memory[out] = memory[left] + memory[right]
    if debug:
        print(f'Res {out}: {memory[out]}')
    pc += 4
    return pc

def handle_mul(memory, pc):
    (left, right, out) = memory[pc+1:pc+4]
    if debug:
        print(f'Mul {left}: {memory[left]}, {right}: {memory[right]}')
    memory[out] = memory[left] * memory[right]
    if debug:
        print(f'Res {out}: {memory[out]}')
    pc += 4
    return pc

handlers = {
    ADD: handle_add,
    MUL: handle_mul
}

def exec_program(memory):
    pc = 0
    while True:
        opcode = memory[pc]
        if opcode == HALT:
            if debug:
                print(f'Program halted. PC: {pc}')
            return

        func = handlers.get(opcode)
        if func:
            pc = func(memory, pc)
        else:
            raise(Exception(f'Invalid opcode {opcode} at position {pc}'))

def main():
    # part 1
    memory_ = numpy.loadtxt('day2\input.txt', delimiter=',', dtype=numpy.int64)
    memory = numpy.array(memory_, copy=True)
    memory[1] = 12
    memory[2] = 2
    exec_program(memory)
    print(f'Part 1: Result at index 0: {memory[0]}')

    # solution found from emperical data ¯\_(ツ)_/¯
    # output = mx + ny + c
    # m = 460800
    # y = 1
    # c = 337061
    memory = numpy.array(memory_, copy=True)
    x = 42
    y = 59
    memory[1] = x
    memory[2] = y
    exec_program(memory)
    print(f'Result for x: {x}, y: {y} is: {memory[0]}')


if __name__ == '__main__':
    main()
