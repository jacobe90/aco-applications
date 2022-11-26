from sudoku import Sudoku
from aco import propogate_constraints
import time
def main():
    puzzle = Sudoku("sabuncu1.txt")
    print("before:")
    puzzle.print_puzzle()
    t1 = time.time()
    while propogate_constraints(puzzle)[0] != 0:
        print("ran")
        continue
    t2 = time.time()
    print("after:")
    puzzle.print_puzzle()
    print("took %d seconds", t2 - t1)

if __name__ == "__main__":
    main()