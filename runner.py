import time
import argparse
import importlib
import os

parser = argparse.ArgumentParser()
parser.add_argument('-d', required=True)
parser.add_argument('-y', required=True)
parser.add_argument('-e', action='store_true', required=False)
parser.add_argument('-debug', action='store_true', required=False)

args = parser.parse_args()

if args.debug:
    import ptvsd
    # Allow other computers to attach to ptvsd at this IP address and port.
    ptvsd.enable_attach(address=('0.0.0.0', 30000), redirect_output=True)
    # Pause the program until a remote debugger is attached
    print(f'waiting for debugger to attach on port {30000}...')
    ptvsd.wait_for_attach()

day = args.d
year = args.y
os.chdir(f'y{year}')
solve = importlib.import_module(f'y{year}.day{day}.solve')

print(f'running day{day}')
if hasattr(solve, 'Solver'):
    # new Solver class
    solver = solve.Solver(day, use_example=args.e)
    parse_start = time.time()
    solver.parse()
    parse_end = time.time()
    p1_start = time.time()
    p1 = solver.part1()
    p1_end = time.time()
    print(f'Part 1: {p1}')
    p2_start = time.time()
    p2 = solver.part2()
    p2_end = time.time()
    print(f'Part 2: {p2}')

    print(f'Elapsed (parse): {parse_end-parse_start}')
    print(f'Elapsed (part1): {p1_end-p1_start}')
    print(f'Elapsed (part2): {p2_end-p2_start}')


else:
    # legacy main method
    start = time.time()
    solve.main()
    end = time.time()

    print(f'Elapsed: {end-start}s')
