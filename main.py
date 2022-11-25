from sudoku import Sudoku
from aco import propogate_constraints

def main():
    puzzle = Sudoku("sabuncu1.txt")
    print("before:")
    puzzle.print_puzzle()
    while propogate_constraints(puzzle) != 0:
        print("ran")
        continue
    print("after:")
    puzzle.print_puzzle()


if __name__ == "__main__":
    main()