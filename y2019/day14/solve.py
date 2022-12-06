import numpy
import matplotlib.pyplot as plt
from collections import defaultdict
from y2019.intcode import CPU, Halted
import math
from copy import deepcopy

test_a = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""
# 31 ORE

test_aa = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D, 1 C => 1 E
7 A, 1 E => 1 FUEL"""
# 42 ORE

test_b = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""
# 165 ORE

test_c = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""
# 13312

test_d = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""
# 180697

test_e = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""
#2210736, 460664 fuel

def build_db(data):
    db = {}
    for line in data:
        [react, prod] = line.split(' => ')
        reactants = defaultdict(int)
        (p_coeff, p_name) = prod.strip().split(' ')
        for _r in react.split(','):
            _r = _r.strip()
            [coef, name] = _r.split(' ')
            reactants[name] = int(coef)
        db[p_name] = {'coeff': int(p_coeff), 'reactants': reactants}
    return db

def do_sub(equ, db, leftover=None):
    if leftover is None:
        leftover = defaultdict(int)
    new_equ = deepcopy(equ)
    new_equ['reactants'] = defaultdict(int)
    new_equ['reactants']['ORE'] = equ['reactants']['ORE']
    for (name, coeff) in equ['reactants'].items():
        if name != 'ORE':
            #new_equ['reactants'].pop(name)
            reactant_equation = db[name]
            if leftover[name] >= coeff:
                needed = 0
                leftover[name] -= coeff
            else:
                needed = coeff - leftover[name]
                leftover[name] = 0

            new_count = math.ceil(needed / reactant_equation['coeff'])
            leftover[name] += (new_count * reactant_equation['coeff']) - needed
            for (new_react, new_react_c) in reactant_equation['reactants'].items():
                new_equ['reactants'][new_react] += new_react_c * new_count

    return(new_equ, leftover)

def main():

    #data = test_e.split('\n')
    with open(r'day14\input.txt') as fid:
        data = fid.readlines()
    db = build_db(data)

    fuel = db['FUEL']
    leftover = None

    while True:
        (fuel, leftover) = do_sub(fuel, db, leftover)
        print(fuel, leftover)
        if len(fuel['reactants'].keys()) == 1 and 'ORE' in fuel['reactants']:
            break
    print(f'Part 1: {fuel["reactants"]["ORE"]} ORE needed')
    p1 = fuel["reactants"]["ORE"]

    MAX_ORE = 1000000000000
    guess = MAX_ORE // p1
    last_guess = 0
    guesses = []
    while True:
        print(f'New guess: {guess}')
        guesses.append(guess)
        fuel = deepcopy(db['FUEL'])
        for item in fuel['reactants']:
            fuel['reactants'][item] *= guess
        while True:
            (fuel, leftover) = do_sub(fuel, db, leftover)
            if len(fuel['reactants'].keys()) == 1 and 'ORE' in fuel['reactants']:
                ore_cnt = fuel["reactants"]["ORE"]
                break
        tmp = guess
        if ore_cnt < MAX_ORE:
            if last_guess > guess:
                guess += math.ceil((last_guess - guess) / 2)
            else:
                guess += math.ceil((guess - last_guess) / 2)
        elif ore_cnt > MAX_ORE:
            if last_guess > guess:
                guess -= math.ceil((last_guess - guess) / 2)
            else:
                guess -= math.ceil((guess - last_guess) / 2)
        else:
            print(f'Exactly one trillion: {guess}')
        last_guess = tmp
        if guess in guesses:
            print(f'Part 2: {last_guess}, {ore_cnt}')
            break

if __name__ == '__main__':
    main()
