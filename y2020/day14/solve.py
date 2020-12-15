from collections import defaultdict
from AoC import AoC
import re

class Solver(AoC):
    example_data = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

    def parse(self):
        lines = self.read_input_txt()

        self.mem = {}
        self.chunks = [] # (mask_1, mask_0, )
        instr = [] # (addr, val)
        raw_mask = None
        mask_1 = None
        mask_0 = None
        pattern = re.compile(r'mem\[(\d+)\]\s=\s(\d+)')
        start = True
        for line in lines:
            if 'mask' in line:
                if not start:
                    self.chunks.append((mask_1, mask_0, instr))
                    instr = []
                raw_mask = line.strip().split(' = ')[1]
                print('     ' + raw_mask)
                mask_1 = int(raw_mask.replace('X', '0'), 2)
                mask_0 = int(raw_mask.replace('X', '1'), 2)
            else:
                start = False
                line = line.strip()
                if line:
                    m_obj = pattern.match(line)
                    (addr, val) = m_obj.groups()
                    instr.append((int(addr), int(val)))
        self.chunks.append((mask_1, mask_0, instr))
        inst = []
        raw_mask = None


    def part1(self):
        for (m1, m0, instr) in self.chunks:
            #print(f'm1 : {m1:036b}')
            #print(f'm0 : {m0:036b}')
            for (addr, val) in instr:
                print(f'  -  {(addr, val)}')
                val = val | m1
                val = val & m0
                self.mem[addr] = val

        return sum([v for v in self.mem.values()])

    def part2(self):
        self.mem = {}
        mx_max = 0
        for (m1, m0, instr) in self.chunks:
            mx = ~(m1 | ~m0)
            #print(f'm1 : {m1:036b}')
            #print(f'm0 : {m0:036b}')
            #print(f'mx : {mx:036b}')
            for (addr, val) in instr:
                # set all bits where 1 in the mask
                addr |= m1
                # clear all bits where X in the mask
                addr &= (~mx)
                # Need to generate all values for X in mask, then apply it to the address.
                # I.e. mask = X0X0, addr = 0100
                #   x_bit_val = 00, 01, 10, 11
                #   addr_mod = 0000, 0010, 1000, 1010
                #   addr =     0100, 0110, 1100, 1110
                mx_bits = f'{mx:b}'.count('1')
                for x_bit_val in range(2**mx_bits):
                    addr_mod = 0
                    for i in range(36):
                        # build addr_mod from L to R by l shifting each loop
                        addr_mod <<= 1
                        # check msb of mx (X's in mask)
                        if (mx << i) & 0b100000000000000000000000000000000000:
                            # set bit in addr_mod if current x_bit_val bit is 1
                            addr_mod |= 1 if (x_bit_val & 2**(mx_bits-1)) else 0
                            x_bit_val = x_bit_val << 1
                    # set memory at modified addr
                    self.mem[addr | addr_mod] = val

        return sum([v for v in self.mem.values()])
