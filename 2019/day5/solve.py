import numpy
from intcode import CPU

def main():
    # part 1
    print('Part 1:')
    memory_ = numpy.loadtxt('day5\input.txt', delimiter=',', dtype=numpy.int64)
    memory = numpy.array(memory_, copy=True)
    cpu = CPU(memory)
    cpu.queue_input(1)
    cpu.exec()

    # part 2
    print('=============================================\nPart 2')
    memory_ = numpy.loadtxt('day5\input.txt', delimiter=',', dtype=numpy.int64)
    memory = numpy.array(memory_, copy=True)
    #test = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    #memory = numpy.array(test, dtype=numpy.int64)
    cpu = CPU(memory)
    cpu.queue_input(5)
    cpu.exec()


if __name__ == '__main__':
    main()
