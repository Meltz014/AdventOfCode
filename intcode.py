import queue
import numpy
import time
import threading

debug = False
# opcodes
HALT = 99
ADD = 1
MUL = 2
INPUT = 3
OUTPUT = 4
JE = 5 # jump if true
JNE = 6 # jump if false
LT = 7 # less than
EQ = 8 # equal
RB = 9 # relative base mod

# Param modes
POS = 0
IMM = 1
REL = 2

REALLOC_BUF = 1000

mode_cache = {}

class Halted(Exception):
    pass

def get_modes(modes_int, n):
    global mode_cache
    modes = mode_cache.get((modes_int, n), None)
    og_modes = modes_int
    if not modes:
        modes = [0] * n
        for i in range(n):
            modes[i] = modes_int % 10
            modes_int //= 10
        mode_cache[(og_modes, n)] = modes
    return modes

class CPU():
    def __init__(self, memory, input_block=False, input_q=None):
        self.memory = memory
        self.pc = 0
        self.relative_base = 0
        self.done = False

        self.handlers = {
            ADD: self.handle_add,
            MUL: self.handle_mul,
            INPUT: self.handle_input,
            OUTPUT: self.handle_output,
            JE: self.handle_je,
            JNE: self.handle_jne,
            LT: self.handle_lt,
            EQ: self.handle_eq,
            RB: self.handle_rb,
        }

        self.input_block = input_block
        if not input_q:
            self.input_q = queue.Queue()
        else:
            self.input_q = input_q
        self.output_q = queue.Queue()
        self.bg_thread = None
        self.pause = False

    def copy(self):
        new = CPU(numpy.array(self.memory, copy=True), self.input_block)
        new.pc = self.pc
        return new

    def queue_input(self, user_val):
        if self.done:
            raise(Halted())
        self.input_q.put(user_val)

    def get_output(self, block=False):
        if self.done and self.output_q.empty():
            raise(Halted())
        if block:
            #print('waiting')
            while True:
                if self.done and self.output_q.empty():
                    raise(Halted())
                try:
                    out = self.output_q.get_nowait()
                    #print(f'done {out}')
                    return out
                except queue.Empty:
                    time.sleep(0)
        else:
            return self.output_q.get_nowait()

    def exec(self, pc=0):
        self.pause = False
        self.pc = pc
        while not self.pause:
            opcode_mode = self.memory[self.pc]
            opcode = opcode_mode % 100
            modes = opcode_mode // 100
            if opcode == HALT:
                self.done = True
                if debug:
                    print(f'Program halted. PC: {self.pc}')
                return

            func = self.handlers.get(opcode)
            if func:
                func(modes)
            else:
                raise(Exception(f'Invalid opcode {opcode} at position {self.pc}'))

    def background_exec(self, pc=0):
        self.pause = False
        self.input_block = True
        self.bg_thread = threading.Thread(target=self.exec, args=(pc, ), daemon=True)
        self.bg_thread.start()

    def stop(self):
        self.pause = True
        if self.bg_thread:
            self.bg_thread.join()
            self.bg_thread = None
        return self.pc

    def _expand(self):
        size = len(self.memory) * 2
        self.memory = numpy.append(self.memory, numpy.zeros(size, dtype=self.memory.dtype))

    def read(self, addr):
        try:
            return self.memory[addr]
        except IndexError:
            self._expand()
            return self.memory[addr]

    def write(self, addr, newval):
        try:
            self.memory[addr] = newval
        except IndexError:
            self._expand()
            self.memory[addr] = newval

    def get_param_vals(self, modes_int, n):
        vals = [0] * n
        for (i, mode) in enumerate(get_modes(modes_int, n)):
            param = self.read(self.pc+1+i)
            if mode == POS:
                vals[i] = self.read(param)
            elif mode == IMM:
                vals[i] = param
            elif mode == REL:
                vals[i] = self.read(self.relative_base + param)

        return vals

    def handle_add(self, modes):
        (_, _, out_mode) = get_modes(modes, 3)
        assert out_mode != IMM
        (left, right) = self.get_param_vals(modes, 2)
        out = self.read(self.pc+3)
        if out_mode == REL:
            out = out + self.relative_base
        if debug:
            print(f'Add: {left}, {right}')
        self.write(out, left + right)
        if debug:
            print(f'Res {out}: {self.read(out)}')
        self.pc += 4

    def handle_mul(self, modes):
        (_, _, out_mode) = get_modes(modes, 3)
        assert out_mode != IMM
        (left, right) = self.get_param_vals(modes, 2)
        out = self.read(self.pc+3)
        if out_mode == REL:
            out = out + self.relative_base
        if debug:
            print(f'Mul: {left}, {right}')
        self.write(out, left * right)
        if debug:
            print(f'Res {out}: {self.read(out)}')
        self.pc += 4

    def handle_input(self, modes):
        (in_mode, ) = get_modes(modes, 1)
        assert in_mode != IMM
        out = self.read(self.pc+1)
        if in_mode == REL:
            out = out + self.relative_base

        if self.input_block:
            while True:
                if self.done and self.input_q.empty():
                    raise(Halted())
                try:
                    user = self.input_q.get_nowait()
                    break
                except queue.Empty:
                    if self.pause:
                        return
                    time.sleep(0)
        else:
            try:
                user = self.input_q.get_nowait()
            except queue.Empty:
                user = int(input('Input an int:'))
        self.write(out, user)
        self.pc += 2

    def handle_output(self, modes):
        (output, ) = self.get_param_vals(modes, 1)
        #print(f'Program output at PC{self.pc}: {output}')
        self.output_q.put(output)
        self.pc += 2

    def handle_je(self, modes):
        (test, val) = self.get_param_vals(modes, 2)
        if test:
            self.pc = val
        else:
            self.pc += 3

    def handle_jne(self, modes):
        (test, val) = self.get_param_vals(modes, 2)
        if test == 0:
            self.pc = val
        else:
            self.pc += 3

    def handle_lt(self, modes):
        (_, _, out_mode) = get_modes(modes, 3)
        assert out_mode != IMM
        (left, right) = self.get_param_vals(modes, 2)
        out = self.read(self.pc+3)
        if out_mode == REL:
            out = out + self.relative_base
        self.write(out, left < right)
        self.pc += 4

    def handle_eq(self, modes):
        (_, _, out_mode) = get_modes(modes, 3)
        assert out_mode != IMM
        (left, right) = self.get_param_vals(modes, 2)
        out = self.read(self.pc+3)
        if out_mode == REL:
            out = out + self.relative_base
        self.write(out, left == right)
        self.pc += 4

    def handle_rb(self, modes):
        (new_rb, ) = self.get_param_vals(modes, 1)
        self.relative_base += new_rb
        self.pc += 2