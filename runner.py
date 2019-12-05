import time
import argparse
import importlib

parser = argparse.ArgumentParser()
parser.add_argument('-day', required=True)
args = parser.parse_args()

day = args.day

solve = importlib.import_module(f'day{day}.solve')

print(f'running day{day}')
start = time.time()
solve.main()
end = time.time()

print(f'Elapsed: {end-start}s')
