import time
import argparse
import importlib

parser = argparse.ArgumentParser()
parser.add_argument('-day', required=True)
args = parser.parse_args()

solve = importlib.import_module(f'day{args.day}.solve')

print(f'running day{args.day}')
start = time.time()
solve.main()
end = time.time()

print(f'Elapsed: {end-start}s')
