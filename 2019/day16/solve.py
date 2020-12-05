import numpy
from collections import defaultdict
import math
import time

patterns = {}
base = [0, 1, 0, -1]

def phase_digit(signal, idx):
    global patterns
    if idx not in patterns:
        pat = []
        for sub in ([b]*idx for b in base):
            pat += sub
        reps = math.ceil((len(signal)+1) / (idx * 4))
        pattern = pat * reps
        pattern = numpy.array(pattern[1:len(signal)+1], numpy.int8)
        patterns[idx] = pattern
    else:
        pattern = patterns[idx]

    return abs(numpy.dot(signal, pattern)) % 10

def main():
    global patterns
    #signal_str = '80871224585914546619083218645595'
    with open(r'day16\input.txt') as fid:
        signal_str = fid.read().strip()
    signal = [int(i) for i in signal_str]
    new_signal = numpy.array(signal, dtype=numpy.int8)
    reps = 100
    for i in range(reps):
        new_signal = numpy.array([phase_digit(new_signal, i+1) for i in range(len(new_signal))], dtype=numpy.int8)

    print('Part 1: ' + ''.join(str(s) for s in new_signal[:8]))
    #print(''.join(str(s) for s in new_signal))

    #### part 2
    real_ = numpy.array(signal, dtype=numpy.int8)
    offset = int(''.join(str(i) for i in real_[:7]))
    real_signal = numpy.tile(real_, 10000)
    offset_signal = real_signal[offset:]
    offset_signal = offset_signal[::-1] # backwards for cumsum
    start_time = time.time()
    for i in range(reps):
        offset_signal = numpy.mod( numpy.cumsum(offset_signal), 10 )

    # re-reverse it
    offset_signal = offset_signal[::-1]

    print('Part 2: ' + ''.join(str(s) for s in offset_signal[:8]))
    #print(''.join(str(s) for s in offset_signal))

if __name__ == '__main__':
    main()
