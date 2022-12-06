import os

from sudoku import Sudoku
from aco import aco
import time


# def sabuncu_initial_test():
#     puzzle = Sudoku("sabuncu1.txt")
#     print("before {} filled:".format(puzzle.filled()))
#     puzzle.print_puzzle()
#     t1 = time.time()
#     # while puzzle.filled() < 81:
#     # propagate_constraints(puzzle, 4)
#     j = 0
#     for i in range(0, 81):
#
#         if puzzle.filled() < 81:
#             print("ran {}".format(i))
#             j = propagate_constraints(puzzle, i)
#     # while propagate_constraints(puzzle, 4) != 0:
#     #     print("ran")
#     #     continue
#     t2 = time.time()
#     print("after: {} filled".format(puzzle.filled()))
#     puzzle.print_puzzle()
#     print("took %d seconds", t2 - t1)


def aco_initial_test():
    puzzle = Sudoku("aiescargot.txt")
    print("before:")
    puzzle.print_puzzle()
    print("after:")
    aco(puzzle)[0].print_puzzle()


def test_all_logic_solvable():
    s = os.listdir("logic-solvable")
    for sudoku in os.listdir("logic-solvable"):
        print("solving {}".format(sudoku))
        puzzle = Sudoku("logic-solvable" + "/" + sudoku)
        t0 = time.time()
        sol, niters, cp_time = aco(puzzle)
        t1 = time.time()
        print("solved! took {} iterations and {} seconds. cp time: {} seconds\n".format(niters, t1 - t0, cp_time))


def test_and_log_results(sudoku):
    with open("test_" + sudoku, "w") as test_file:
        for i in range(100):
            puzzle = Sudoku("logic-solvable/" + sudoku)

            t0 = time.time()
            if aco(puzzle) == -1:
                test_file.write("timed out\n")
                continue
            t1 = time.time()
            if i % 1 == 0:
                print("iteration {}/100".format(i))
            # print("{} solved.".format(i))
            test_file.write("{}\n".format(t1 - t0))


def main():
    for sudoku in os.listdir("logic-solvable"):
        print("running tests for {}".format(sudoku))
        test_and_log_results(sudoku)


if __name__ == "__main__":
    test_all_logic_solvable()