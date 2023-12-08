from AoC import AoC
import numpy as np

## 12 red cubes, 13 green cubes, and 14 blue cubes
MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

class Solver(AoC):
    example_data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    def parse(self):
        self.games = {}
        raw = self.read_input_txt(split=True)
        for raw_g in raw:
            game_id, sets = raw_g.split(':')
            game_id = int(game_id[5:])
            self.games[game_id] = []
            set_list = sets.split(';')
            for cubes in set_list:
                game = {}
                for cube in cubes.strip().split(','):
                    n, color = cube.strip().split(' ')
                    game[color] = int(n)
                self.games[game_id].append(game)
        for (_id, game) in self.games.items():
            print(_id, game)


    def part1(self):
        _sum = 0
        for (game_id, game) in self.games.items():
            invalid = False
            red = 0
            blue = 0
            green = 0
            for cubes in game:
                red = cubes.get('red', 0)
                green = cubes.get('green', 0)
                blue = cubes.get('blue', 0)
                if red > MAX_RED or green > MAX_GREEN or blue > MAX_BLUE:
                    invalid = True
                    break
            if not invalid:
                _sum += game_id
        return _sum

    def part2(self):
        _sum = 0
        for (game_id, game) in self.games.items():
            red = 0
            blue = 0
            green = 0
            for cubes in game:
                red = max(red, cubes.get('red', 0))
                green = max(green, cubes.get('green', 0))
                blue = max(blue, cubes.get('blue', 0))
            pwr = red * green * blue
            _sum += pwr
        return _sum
