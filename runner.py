import time
import argparse
import importlib
import os
from timeit import timeit

def format_time(seconds: float) -> str:
    if seconds > 1e0:
        return f"{seconds:.2f} sec"
    if seconds > 1e-3:
        return f"{int(seconds * 1e3)} ms"
    if seconds > 1e-6:
        return f"{int(seconds * 1e6)} μs"
    if seconds > 1e-9:
        return f"{int(seconds * 1e9)} ns"
    return str(seconds)

parser = argparse.ArgumentParser()
parser.add_argument('-y', help="AoC puzzle year", required=True)
parser.add_argument('-d', help="AoC puzzle day", required=True)
parser.add_argument('-e', help="Example data option", action='store_true', required=False)
parser.add_argument('-b', help="Run timeit benchmark", action='store_true', required=False)
parser.add_argument('-v', help="Run in visualizer (if available)", action='store_true', required=False)
parser.add_argument('-n', help="Number of times to run for benchmark", required=False, default=1000, type=int)
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
    if args.v:
        # run in visualizer
        if args.b:
            print('-b option not supported in visualizer mode!')

        visualize = importlib.import_module(f'y{year}.day{day}.visualize')

        solver = visualize.Solver(day, use_example=args.e)
        solver.visualize()
    else:
        solver = solve.Solver(day, use_example=args.e)
        parse_start = time.perf_counter()
        solver.parse()
        parse_end = time.perf_counter()
        if args.b:
            elapsed_parse = timeit(solver.parse, number=args.n)
            elapsed_p1 = timeit(solver.part1, number=args.n)
            elapsed_p2 = timeit(solver.part2, number=args.n)
            print(f'Elapsed (parse) (timeit): {format_time(elapsed_parse/args.n)}')
            print(f'Elapsed (part1) (timeit): {format_time(elapsed_p1/args.n)}')
            print(f'Elapsed (part2) (timeit): {format_time(elapsed_p2/args.n)}')
        else:
            p1_start = time.perf_counter()
            p1 = solver.part1()
            p1_end = time.perf_counter()
            print(f'Part 1: {p1}')
            p2_start = time.perf_counter()
            p2 = solver.part2()
            p2_end = time.perf_counter()
            print(f'Part 2: {p2}')

            print(f'Elapsed (parse): {format_time(parse_end-parse_start)}')
            print(f'Elapsed (part1): {format_time(p1_end-p1_start)}')
            print(f'Elapsed (part2): {format_time(p2_end-p2_start)}')


else:
    # legacy main method
    start = time.perf_counter()
    solve.main()
    end = time.perf_counter()

    print(f'Elapsed: {end-start}s')
