import numpy
from intcode import CPU

def main():
    # part 1
    memory_ = numpy.loadtxt('day2\input.txt', delimiter=',', dtype=numpy.int64)
    memory = numpy.array(memory_, copy=True)
    memory[1] = 12
    memory[2] = 2
    cpu = CPU(memory)
    cpu.exec()
    print(f'Part 1: Result at index 0: {cpu.memory[0]}')

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
    cpu = CPU(memory)
    cpu.exec()
    print(f'Result for x: {x}, y: {y} is: {cpu.memory[0]}')


if __name__ == '__main__':
    main()
