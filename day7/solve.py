import numpy
import itertools
import threading

from intcode import CPU

def main():
    # part 1
    memory_ = numpy.loadtxt('day7\input.txt', delimiter=',', dtype=numpy.int64)
    ##memory_ = numpy.fromstring('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', sep=',', dtype=numpy.int64)
    ##memory_ = numpy.fromstring('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0', sep=',', dtype=numpy.int64)

    max_out = None
    max_seq = None
    for phase_seq in itertools.permutations(range(5), 5):
        last_output = 0
        for phase in phase_seq:
            memory = numpy.array(memory_, copy=True)
            cpu = CPU(memory)
            cpu.queue_input(phase)
            cpu.queue_input(last_output)
            cpu.exec()
            last_output = cpu.get_output()
        if not max_out or (last_output > max_out):
            max_out = last_output
            max_seq = phase_seq
            
    print(f'Part 1: Max: {max_out}')
    print(f'Part 1: Max Seq: {max_seq}')

    # 3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
    # part 2
    #memory_ = numpy.fromstring('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5', sep=',', dtype=numpy.int64)

    max_out = None
    max_seq = None
    for phase_seq in itertools.permutations(range(5,10), 5):
        cpu_a = CPU(numpy.array(memory_, copy=True), input_block=True)
        cpu_b = CPU(numpy.array(memory_, copy=True), input_block=True, input_q=cpu_a.output_q)
        cpu_c = CPU(numpy.array(memory_, copy=True), input_block=True, input_q=cpu_b.output_q)
        cpu_d = CPU(numpy.array(memory_, copy=True), input_block=True, input_q=cpu_c.output_q)
        cpu_e = CPU(numpy.array(memory_, copy=True), input_block=True, input_q=cpu_d.output_q)

        cpu_a.input_q = cpu_e.output_q

        cpu_a.queue_input(phase_seq[0])
        cpu_a.queue_input(0)
        cpu_b.queue_input(phase_seq[1])
        cpu_c.queue_input(phase_seq[2])
        cpu_d.queue_input(phase_seq[3])
        cpu_e.queue_input(phase_seq[4])
        # start CPU's in threads
        a_thread = threading.Thread(target=cpu_a.exec)
        b_thread = threading.Thread(target=cpu_b.exec)
        c_thread = threading.Thread(target=cpu_c.exec)
        d_thread = threading.Thread(target=cpu_d.exec)
        e_thread = threading.Thread(target=cpu_e.exec)

        a_thread.start()
        b_thread.start()
        c_thread.start()
        d_thread.start()
        e_thread.start()

        e_thread.join()
        last_output = cpu_e.get_output()
        if not max_out or (last_output > max_out):
            max_out = last_output
            max_seq = phase_seq

    print(f'Part 2 max out: {max_out}')

if __name__ == '__main__':
    main()
