from AoC import AoC
from itertools import zip_longest
from tqdm import tqdm
import numpy as np

class CPU():
    def __init__(self, aoc, a, b, c, prog):
        self.aoc = aoc
        self.a = a
        self.b = b
        self.c = c
        self.prog = prog
        self.pc = 0
        self.outputs = []
        self.original_state = {
            'a': self.a,
            'b': self.b,
            'c': self.c,
            'pc': self.pc,
            'outputs': self.outputs.copy(),
            'prog': self.prog.copy(),
        }

    def reset(self):
        self.a = self.original_state['a']
        self.b = self.original_state['b']
        self.c = self.original_state['c']
        self.pc = self.original_state['pc']
        self.outputs = self.original_state['outputs'].copy()
        self.prog = self.original_state['prog'].copy()

    def debug(self, *args, **kwargs):
        self.aoc.debug(*args, **kwargs)

    def get_combo_value(self, operand):
        if operand in [0,1,2,3]:
            return operand
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c
        raise Exception(f"Invalid operand {operand}")

    def run(self, until=None):
        while self.pc < len(self.prog):
            op = self.prog[self.pc]
            self.pc += 1
            operand = self.prog[self.pc]
            self.pc += 1
            self.operate(op, operand)
            if until:
                if until(self):
                    break

    def operate(self, op, operand):
        funcs = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }
        func = funcs[op]
        self.debug(f'{func.__name__}: {operand}')
        func(operand)
        self.debug(self)

    def adv(self, operand):
        """Divide a by operand**2"""
        value = self.get_combo_value(operand)
        self.a = self.a // (2**value)
    
    def bxl(self, operand):
        """bitwise xor of b and operandaz"""
        self.b = self.b ^ operand

    def bst(self, operand):
        value = self.get_combo_value(operand)
        self.b = value % 8

    def jnz(self, operand):
        if self.a:
            self.pc = operand

    def bxc(self, *args):
        self.b ^= self.c

    def out(self, operand):
        value = self.get_combo_value(operand)
        self.outputs.append(value % 8)

    def bdv(self, operand):
        value = self.get_combo_value(operand)
        self.b = self.a // (2 ** value)

    def cdv(self, operand):
        value = self.get_combo_value(operand)
        self.c = self.a // (2 ** value)

    def __str__(self):
        return f"CPU: a={self.a}, b={self.b}, c={self.c}, pc={self.pc}, outputs={self.outputs}"


class Solver(AoC):
    example_data = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


    def parse(self):
        self.tqdm_total = 0
        raw = self.read_input_txt()
        a = int(raw[0].strip()[12::])
        b = int(raw[1].strip()[12::])
        c = int(raw[2].strip()[12::])
        prog = raw[4].strip()[9::].split(',')
        prog = [int(i) for i in prog]
        self.debug(a, b, c, prog)
        self.cpu = CPU(self, a, b, c, prog)

    def part1(self):
        """
        """
        self.cpu.run()
        print(','.join(str(o) for o in self.cpu.outputs))
        return 0

    def part2(self):
        """
        """

        def test(x):
            A = x
            while A != 0:
                B = A & 0b111
                B ^= 0b011
                B ^= A >> B
                B ^= 0b101
                yield B & 0b111
                A >>= 3

        #new_a = 1
        new_a = (1<<(16*3)) - 1
        print(self.cpu.prog)
        def reverse_engineer(new_a, prog_counter):
            # work backwards to correlate MSB of a to program output
            for i in range(8):
                new_a = new_a - (new_a & (0b111 << (3*prog_counter)))
                new_a += (i << (3*prog_counter))
                out = list(test(new_a))
                #self.cpu.reset()
                #self.cpu.a = new_a
                #self.cpu.run()
                #out = self.cpu.outputs
                a_str = f'{new_a:048b}'
                a_bits = [a_str[i*3:i*3+3] for i in range(16)]
                print(f'{" ".join(a_bits)}: {out}: {prog_counter}')
                if len(out) < 16:
                    continue
                if out[prog_counter] == self.cpu.prog[prog_counter]:
                    if prog_counter == 0:
                        return new_a
                    ret = reverse_engineer(new_a, prog_counter-1)
                    if ret:
                        return ret
            return False

        new_a = reverse_engineer(new_a, 15)
        print(list(test(new_a)))
        return new_a

