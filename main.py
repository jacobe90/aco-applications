import os

from sudoku import Sudoku
from aco import propagate_constraints, aco
import time


def sabuncu_initial_test():
    puzzle = Sudoku("sabuncu1.txt")
    print("before:")
    puzzle.print_puzzle()
    t1 = time.time()
    while propagate_constraints(puzzle)[0] != 0:
        print("ran")
        continue
    t2 = time.time()
    print("after:")
    puzzle.print_puzzle()
    print("took %d seconds", t2 - t1)


def aco_initial_test():
    puzzle = Sudoku("aiescargot.txt")
    print("before:")
    puzzle.print_puzzle()
    print("after:")
    aco(puzzle).print_puzzle()


def test_all_logic_solvable():
    s = os.listdir("logic-solvable")
    for sudoku in os.listdir("logic-solvable"):
        print("solving {}".format(sudoku))
        puzzle = Sudoku("logic-solvable" + "/" + sudoku)
        aco(puzzle).print_puzzle()


def test_cp():
    puzzle = Sudoku("logic-solvable/sabuncu5.txt")
    count = 0
    for vs in puzzle.value_sets:
        if len(vs) == 1:
            count += 1
    fixed, failed = propagate_constraints(puzzle)
    count += fixed
    while fixed != 0:
        print("fixed: %d cells"%fixed)
        fixed, failed = propagate_constraints(puzzle)
        count += fixed
    print(count)

def main():
    test_all_logic_solvable()


if __name__ == "__main__":
    main()