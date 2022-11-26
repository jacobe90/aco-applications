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


def main():
    aco_initial_test()


if __name__ == "__main__":
    main()