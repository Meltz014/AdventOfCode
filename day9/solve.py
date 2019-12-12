import numpy
from queue import Empty
from intcode import CPU, Halted

def main():
    # part 1
    memory_ = numpy.loadtxt('day9\input.txt', delimiter=',', dtype=numpy.int64)
    #memory_ = numpy.fromstring('1102,34915192,34915192,7,4,7,99,0', sep=',', dtype=numpy.int64)
    #memory_ = numpy.fromstring('104,1125899906842624,99', sep=',', dtype=numpy.int64)
    #memory_ = numpy.fromstring('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99', sep=',', dtype=numpy.int64)

    ### Part 1
    memory = numpy.array(memory_, copy=True)
    cpu = CPU(memory)
    cpu.queue_input(1)
    cpu.exec()
    print(f'Part 1 output:')
    try:
        while True:
            print(str(cpu.get_output(False)) + ' ',)
    except Halted:
        print('done')

    ### Part 2
    memory = numpy.array(memory_, copy=True)
    cpu = CPU(memory)
    cpu.queue_input(2)
    cpu.exec()
    print(f'Part 2 output:')
    try:
        while True:
            print(str(cpu.get_output(False)) + ' ',)
    except Halted:
        print('done')


if __name__ == '__main__':
    main()
