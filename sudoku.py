import numpy as np

# goal - class to load sudoku from a file
# units - rows, cells, columns, boxes
#

# TODO
# implement game board copying

class Sudoku:
    def __init__(self, path):
        self.d = None
        self.cell_dim = None
        self.something = None
        self.value_sets = []
        self.load_puzzle(path)

    def load_puzzle(self, path):
        with open(path, 'r') as sudoku:
            lines = sudoku.readlines()
        self.cell_dim = int(lines[0])
        self.d = int(lines[0])*int(lines[0])
        self.something = int(lines[1])
        count = 0
        for i in range(2, 2+self.d, 1):
            row = lines[i].split("\t")
            for num in row:
                n = int(num)
                if n == -1:
                    self.value_sets.append([z for z in range(1, self.d+1)])
                else:
                    self.value_sets.append([int(n)])

    # top left corner of box
    # 0 + x + 9y
    # x = cell_dim * i % 3
    # y = cell_dim * i / 3
    def get_box(self, i):
        box = []
        box_start = self.cell_dim * (i % self.cell_dim) + self.d * self.cell_dim * int(i / self.cell_dim)
        for row in range(0, self.cell_dim):
            for x in range(box_start + 9*row, box_start + 9*row + self.cell_dim):
                box.append(x)
        return box

    def set_value_set(self, ):
        pass

    def get_value_set(self, i):
        pass

    def print_puzzle(self):
        for c in range(self.d * self.d):
            vs = self.value_sets[c]
            if len(vs) == 1:
                print("{}\t".format(vs[0]), end=" ")
            else:
                print("-1\t", end=" ")
            if c % (self.d) == self.d - 1:
                print("\n", end = "")
