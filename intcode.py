import queue

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

# Param modes
POS = 0
IMM = 1

def get_modes(modes_int, n):
    modes = []
    for i in range(n):
        modes.append(modes_int % 10)
        modes_int //= 10
    return modes


class CPU():
    def __init__(self, memory, input_block=False, input_q=None):
        self.memory = memory
        self.pc = 0

        self.handlers = {
            ADD: self.handle_add,
            MUL: self.handle_mul,
            INPUT: self.handle_input,
            OUTPUT: self.handle_output,
            JE: self.handle_je,
            JNE: self.handle_jne,
            LT: self.handle_lt,
            EQ: self.handle_eq,
        }

        self.input_block = input_block
        if not input_q:
            self.input_q = queue.Queue()
        else:
            self.input_q = input_q
        self.output_q = queue.Queue()

    def queue_input(self, user_val):
        self.input_q.put(user_val)

    def get_output(self):
        return self.output_q.get_nowait()

    def exec(self, pc=0):
        self.pc = pc
        while True:
            opcode_mode = self.memory[self.pc]
            opcode = opcode_mode % 100
            modes = opcode_mode // 100
            if opcode == HALT:
                if debug:
                    print(f'Program halted. PC: {self.pc}')
                return

            func = self.handlers.get(opcode)
            if func:
                func(modes)
            else:
                raise(Exception(f'Invalid opcode {opcode} at position {self.pc}'))

    def get_param_vals(self, modes_int, n):
        vals = []
        for (i, mode) in enumerate(get_modes(modes_int, n)):
            param = self.memory[self.pc+1+i]
            if mode == POS:
                vals.append(self.memory[param])
            elif mode == IMM:
                vals.append(param)

        return vals

    def handle_add(self, modes):
        (_, _, out_mode) = get_modes(modes, 3)
        assert out_mode == POS
        (left, right) = self.get_param_vals(modes, 2)
        out = self.memory[self.pc+3]
        if debug:
            print(f'Add: {left}, {right}')
        self.memory[out] = left + right
        if debug:
            print(f'Res {out}: {self.memory[out]}')
        self.pc += 4

    def handle_mul(self, modes):
        (_, _, out_mode) = get_modes(modes, 3)
        assert out_mode == POS
        (left, right) = self.get_param_vals(modes, 2)
        out = self.memory[self.pc+3]
        if debug:
            print(f'Mul: {left}, {right}')
        self.memory[out] = left * right
        if debug:
            print(f'Res {out}: {self.memory[out]}')
        self.pc += 4

    def handle_input(self, modes):
        (in_mode, ) = get_modes(modes, 1)
        assert in_mode == POS
        out = self.memory[self.pc+1]
        try:
            if self.input_block:
                user = self.input_q.get()
            else:
                user = self.input_q.get_nowait()
        except queue.Empty:
            user = int(input('Input an int:'))
        self.memory[out] = user
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
        assert out_mode == POS
        (left, right) = self.get_param_vals(modes, 2)
        out = self.memory[self.pc+3]
        self.memory[out] = left < right
        self.pc += 4

    def handle_eq(self, modes):
        (_, _, out_mode) = get_modes(modes, 3)
        assert out_mode == POS
        (left, right) = self.get_param_vals(modes, 2)
        out = self.memory[self.pc+3]
        self.memory[out] = left == right
        self.pc += 4