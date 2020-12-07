import time
import argparse
import importlib
import os
import ptvsd

parser = argparse.ArgumentParser()
parser.add_argument('-d', required=True)
parser.add_argument('-y', required=True)
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
os.chdir(year)
solve = importlib.import_module(f'{year}.day{day}.solve')

print(f'running day{day}')
start = time.time()
solve.main()
end = time.time()

print(f'Elapsed: {end-start}s')
