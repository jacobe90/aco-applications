import numpy as np

# goal - class to load sudoku from a file
# units - rows, cells, columns, boxes
#

# TODO
# implement game board copying


class Sudoku:
    def __init__(self, path, load=True):
        self.d = None
        self.cell_dim = None
        self.something = None
        self.value_sets = []
        if load:
            self.load_puzzle(path)

    def load_puzzle(self, path):
        with open(path, 'r') as sudoku:
            lines = sudoku.readlines()
        self.cell_dim = int(lines[0])
        self.d = int(lines[0])*int(lines[0])
        self.something = int(lines[1])

        self.value_sets = [[x for x in range(1, self.d+1)] for y in range(self.d * self.d)]

        count = 0
        for i in range(2, 2+self.d, 1):
            row = lines[i].split("\t")
            for num in row:
                if num == '\n':
                    continue
                n = int(num)
                if n != -1:
                    self.assign(count, n)
                count += 1

    def copy(self):
        copy = Sudoku(None, False)
        copy.d = self.d
        copy.cell_dim = self.cell_dim
        copy.something = self.something
        copy.value_sets = []
        for vs in self.value_sets:
            newvs = [v for v in vs]
            copy.value_sets.append(newvs)
        return copy

    # assign [d] to puzzle.value_sets[i]
    def assign(self, i, d):
        other_vals = list(filter(lambda v: v != d, self.value_sets[i]))
        return all(self.eliminate(i, other_val) for other_val in other_vals)

    # eliminate d from puzzle.value_sets[i]
    def eliminate(self, i, d):
        if d not in self.value_sets[i]:
            return True
        self.value_sets[i].remove(d)
        if len(self.value_sets[i]) == 0:
            return False
        elif len(self.value_sets[i]) == 1:
            d2 = self.value_sets[i][0]
            if not all(self.eliminate(i2, d2) for i2 in self.peers(i)):
                return False
        for u in self.units(i):
            dplaces = [s for s in u if d in self.value_sets[s]]
            if len(dplaces) == 0:
                return False
            elif len(dplaces) == 1:
                if not self.assign(dplaces[0], d):
                    return False
        return True

    def units(self, i):
        return [self.get_box(i), self.get_row(i), self.get_column(i)]

    def peers(self, i):
        peers = list(set(self.get_box(i) + self.get_row(i) + self.get_column(i)))
        peers.remove(i)
        return peers

    def filled(self):
        filled = 0
        for vs in self.value_sets:
            if len(vs) == 1:
                filled += 1
        return filled

    def solved(self):
        # check rows contain values 1-d
        for i in range(0, self.d * self.d, self.d):
            row = [self.value_sets[j] for j in self.get_row(i)]
            for x in range(1, self.d+1):
                found_x = False
                for vs in row:
                    if len(vs) != 1:
                        return False
                    if vs[0] == x:
                        found_x = True
                if not found_x:
                    return False
        # check columns contain values 1-d
        for i in range(0, self.d):
            col = [self.value_sets[j] for j in self.get_column(i)]
            for x in range(1, self.d + 1):
                found_x = False
                for vs in col:
                    if len(vs) != 1:
                        return False
                    if vs[0] == x:
                        found_x = True
                if not found_x:
                    return False
        # check boxes contain values 1-d
        for i in range(0, self.d):
            box = [self.value_sets[j] for j in self.get_box(i)]
            for x in range(1, self.d + 1):
                found_x = False
                for vs in box:
                    if len(vs) != 1:
                        return False
                    if vs[0] == x:
                        found_x = True
                if not found_x:
                    return False
        return True

    def get_row(self, i):
        return [x for x in range(i - i % self.d, i - i % self.d + self.d, 1)]

    def get_column(self, i):
        return [x for x in range(i % self.d, self.d * self.d, self.d)]
    # top left corner of box
    # 0 + x + 9y
    # x = cell_dim * i % 3
    # y = cell_dim * i / 3
    def get_box(self, i):
        box_index = int((i % self.d) / self.cell_dim) + self.cell_dim * int(int(i / self.d) / self.cell_dim)
        box = []
        box_start = self.cell_dim * (box_index % self.cell_dim) + self.d * self.cell_dim * int(box_index / self.cell_dim)
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
