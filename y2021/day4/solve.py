from AoC import AoC
import numpy as np

class Solver(AoC):
    example_data = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

    def parse(self):
        raw = self.read_input_txt()
        raw += ['\n']
        self.draw = np.array([int(i) for i in raw[0].strip('\n').split(',')])
        self.boards = []
        board = np.zeros((5,5), dtype=np.uint8)
        row = 0
        for line in raw[2:]:
            if line == '\n':
                self.boards.append(board.copy())
                board = np.zeros((5,5), dtype=np.uint8)
                row = 0
                continue
            board[row,:] = np.array([int(i) for i in line.strip('\n').split()], dtype=np.uint8)
            row += 1
        self.reset_game()

    def reset_game(self):
        self.marks = [np.zeros_like(board) for board in self.boards]

    def draw_num(self, num):
        for (mark, board) in zip(self.marks, self.boards):
            mark[board == num] = 1

    def check_win(self):
        wins = []
        for (i, mark) in enumerate(self.marks):
            cols = np.sum(mark, axis=0)
            rows = np.sum(mark, axis=1)
            if np.any(cols == 5) or np.any(rows == 5):
                wins.append(i)
        return wins

    def part1(self):
        winner = None
        win_num = 0
        for num in self.draw:
            self.draw_num(num)
            winners = self.check_win()
            if winners:
                winner = winners[0]
                win_num = num
                print(self.boards[winner])
                break

        # sum all unmarked numbers
        w_board = self.boards[winner]
        w_marks = self.marks[winner]
        unmarked = np.sum(w_board[w_marks == 0])
        return unmarked * win_num

    def part2(self):
        # find *last* board to win
        self.reset_game()
        lose_num = 0
        loser = None
        for (i, num) in enumerate(self.draw):
            self.draw_num(num)
            winners = self.check_win()
            if winners:
                for winner in winners[::-1]:
                    if len(self.boards) > 1:
                        self.boards.pop(winner)
                        self.marks.pop(winner)
                    else:
                        # loser found
                        lose_num = num
                        loser = winner
                        break
                if loser is not None:
                    break
        w_board = self.boards[loser]
        w_marks = self.marks[loser]

        unmarked = np.sum(w_board[w_marks == 0])
        return unmarked * lose_num

