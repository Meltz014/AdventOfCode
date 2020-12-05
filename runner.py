import time
import argparse
import importlib
import os

parser = argparse.ArgumentParser()
parser.add_argument('-d', required=True)
parser.add_argument('-y', required=True)
args = parser.parse_args()

day = args.d
year = args.y
os.chdir(year)
solve = importlib.import_module(f'{year}.day{day}.solve')

print(f'running day{day}')
start = time.time()
solve.main()
end = time.time()

print(f'Elapsed: {end-start}s')
