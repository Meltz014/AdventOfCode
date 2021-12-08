import numpy
from y2019.intcode import CPU, Halted

def y2021_d7():
    print('2021 Day 7 Easter Egg: run input as intcode program')
    memory_ = numpy.loadtxt('y2021\day7\input.txt', delimiter=',', dtype=numpy.int64)

    memory = numpy.array(memory_, copy=True)
    cpu = CPU(memory)
    cpu.background_exec()

    try:
        while True:
            print(chr(cpu.get_output(block=True)),end='')
    except Halted:
        pass
    print('\nDone')

y2021_d7()
