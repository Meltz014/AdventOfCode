from copy import deepcopy

class HandHeld():
    """
    CPU emulator for "Hand Held gaming device"
    """
    valid_opcodes = ['acc', 'nop', 'jmp']
    def __init__(self, raw_instructions):
        self.callback = None
        self._pc = 0
        self._acc = 0
        self.go = True
        self.finished = False

        # parse raw instructions
        self.program = []
        for line in raw_instructions:
            (instr, i_arg) = line.strip().split(' ')
            self.program.append((instr, int(i_arg)))

        # save a copy of program to enable reset()
        self.original_program = deepcopy(self.program)

        # history of instructions executed
        self.pc_hist = []

    def reset(self):
        self._pc = 0
        self._acc = 0
        self.go = True
        self.pc_hist = []
        self.finished = False
        self.program = deepcopy(self.original_program)

    def run(self, callback=None):
        if callback:
            self.callback = callback
        while self.go:
            if self.callback:
                self.callback(self)
            (instr, i_arg) = self.program[self._pc]
            # keep track of instr calls
            self.pc_hist.append(self._pc)
            # run op func
            if instr in self.valid_opcodes:
                getattr(self, instr)(i_arg)
            else:
                print(f'invalid opcode: {instr, i_arg}')
                self.halt()
                break
            if self._pc == len(self.program):
                self.finished = True
                self.halt()

    def halt(self):
        self.go = False

    # opcodes...
    def acc(self, amt):
        self._acc += amt
        self._pc += 1

    def nop(self, *args):
        # no op; do nothing
        self._pc += 1

    def jmp(self, offset):
        self._pc += offset
