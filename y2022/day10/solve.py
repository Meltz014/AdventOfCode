from AoC import AoC
import numpy as np
import matplotlib.pyplot as plt

class CRT():
    def __init__(self):
        self.x = 1
        self.clock = 0

        self.p1_tot = 0
        self.screen = np.zeros((6,40), dtype=bool)

    def disp(self):
        print(self.screen)
        plt.imshow(self.screen)
        plt.show()

    def tick(self):
        # draw screen
        pixel = divmod((self.clock % 240), 40)
        sprite = self.x % 40
        if pixel[0] == 4:
            print(f'{self.x}, {pixel}, {sprite}, {pixel[1] in range(sprite-1, sprite+2)}')
            self.disp()
        self.screen[pixel] = pixel[1] in range(sprite-1, sprite+2)

        # Increment clock
        self.clock += 1
        if (self.clock == 20) or (self.clock+20)%40==0:
            self.p1_tot += self.clock * self.x



    def command(self, cmd, *args):
        self.tick()
        if cmd == 'noop':
            return
        elif cmd == 'addx':
            self.tick()
            self.x += int(args[0])


class Solver(AoC):
    example_data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        self.inst = []
        for line in raw:
            line = line.strip()
            self.inst.append(line.split())

    def part1(self):
        crt = CRT()
        tot = 0
        for i in self.inst:
            crt.command(*i)
        crt.disp()

        return crt.p1_tot

    def part2(self):
        return 'See generated plot'