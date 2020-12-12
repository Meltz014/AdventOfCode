
import re
import math
from AoC import AoC

class Ship():
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.facing = 0 # facing east

    def move(self, inst, mag):
        if inst in 'LR':
            self.facing += (1 if inst == 'L' else -1) * mag
        else:
            if inst == 'F':
                # get x and y components of mag & facing angle
                rad = math.radians(self.facing)
                dx = mag * math.cos(rad)
                dy = mag * math.sin(rad)
            elif inst == 'N':
                dx = 0
                dy = mag
            elif inst == 'S':
                dx = 0
                dy = -mag
            elif inst == 'E':
                dx = mag
                dy = 0
            elif inst == 'W':
                dx = -mag
                dy = 0
            self.pos_x += dx
            self.pos_y += dy

class ShipP2():
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.waypoint = [10, 1]

    def move(self, inst, mag):
        if inst in 'LR':
            # non-trig.  Assume 90deg inc
            mag = mag * (1 if inst == 'L' else -1)
            if mag in [90, -270]:
                self.waypoint = [self.waypoint[1] * -1, self.waypoint[0]]
            elif mag in [-90, 270]:
                self.waypoint = [self.waypoint[1], self.waypoint[0] * -1]
            elif mag in [180, -180]:
                self.waypoint = [self.waypoint[0] * -1, self.waypoint[1] * -1]
            else:
                raise(Exception('bad'))
        else:
            if inst == 'F':
                self.pos_x += self.waypoint[0] * mag
                self.pos_y += self.waypoint[1] * mag
            elif inst == 'N':
                self.waypoint[1] += mag
            elif inst == 'S':
                self.waypoint[1] -= mag
            elif inst == 'E':
                self.waypoint[0] += mag
            elif inst == 'W':
                self.waypoint[0] -= mag

class Solver(AoC):
    example_data = """F10
N3
F7
R90
F11"""

    def parse(self):
        lines = self.read_input_txt()
        self.instructions = []
        for line in lines:
            inst = line[0]
            mag = int(line[1:])
            self.instructions.append((inst, mag))


    def part1(self):
        ship = Ship()
        for (inst, mag) in self.instructions:
            ship.move(inst, mag)

        return abs(ship.pos_x) + abs(ship.pos_y)

    def part2(self):
        ship = ShipP2()
        for (inst, mag) in self.instructions:
            ship.move(inst, mag)

        return abs(ship.pos_x) + abs(ship.pos_y)