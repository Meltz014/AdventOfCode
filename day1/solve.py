
import numpy

def main():
    masses = numpy.loadtxt('input.txt', dtype=numpy.uint32)
    fuel = (masses // 3) - 2
    print(numpy.sum(fuel))

main()