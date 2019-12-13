import re
import numpy

class Moon():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def __repr__(self):
        return f'<Moon pos:({self.x}, {self.y}, {self.z}) vel: ({self.vx, self.vy, self.vz})'

    def apply_gravity(self, other):
        self.apply_gravity_x(other)
        self.apply_gravity_y(other)
        self.apply_gravity_z(other)

    def apply_gravity_x(self, other):
        self.vx += 1 if self.x < other.x else -1 if self.x > other.x else 0

    def apply_gravity_y(self, other):
        self.vy += 1 if self.y < other.y else -1 if self.y > other.y else 0

    def apply_gravity_z(self, other):
        self.vz += 1 if self.z < other.z else -1 if self.z > other.z else 0

    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def energy(self):
        pe = sum([abs(self.x), abs(self.y), abs(self.z)])
        ke = sum([abs(self.vx), abs(self.vy), abs(self.vz)])
        return pe * ke

    def getstate(self):
        return (self.x, self.y, self.z, self.vx, self.vy, self.vz)

def universe_state(moons):
    state = moons[0].getstate()
    for moon in moons[1::]:
        state += moon.getstate()
    return state

def main():
    moons = []
    with open('day12\\input.txt') as fid:
        for row in fid:
            m_obj = re.match(r'<x=(\-?\d+), y=(\-?\d+), z=(\-?\d+)>', row)
            (x, y, z) = (int(m) for m in m_obj.groups())
            moons.append(Moon(x, y, z))

    for i in range(1000):
        for moon in moons:
            for other_moon in moons:
                if moon is not other_moon:
                    moon.apply_gravity(other_moon)

        for moon in moons:
            moon.update_position()

    total_e = sum(m.energy() for m in moons)
    print(f'Part 1 energy: {total_e}')

    moons = []
    with open('day12\\input.txt') as fid:
        for row in fid:
            m_obj = re.match(r'<x=(\-?\d+), y=(\-?\d+), z=(\-?\d+)>', row)
            (x, y, z) = (int(m) for m in m_obj.groups())
            moons.append(Moon(x, y, z))
    axes_iter = [0, 0, 0]
    for axis in range(3):
        i = 0
        while True:
            i += 1
            for moon in moons:
                for other_moon in moons:
                    if moon is not other_moon:
                        if axis == 0:
                            moon.apply_gravity_x(other_moon)
                        elif axis == 1:
                            moon.apply_gravity_y(other_moon)
                        elif axis == 2:
                            moon.apply_gravity_z(other_moon)

            for moon in moons:
                moon.update_position()

            # check if all velocities are 0
            all_zero = True
            for moon in moons:
                test = None
                if axis == 0:
                    test = moon.vx
                elif axis == 1:
                    test = moon.vy
                elif axis == 2:
                    test = moon.vz
                if test:
                    all_zero = False
                    break
            if all_zero:
                break

        axes_iter[axis] = i*2

    print(f'Part 2 LCM of: {axes_iter}')

if __name__ == '__main__':
    main()
