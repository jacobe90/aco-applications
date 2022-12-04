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


# def test_cp():
#     puzzle = Sudoku("logic-solvable/sabuncu5.txt")
#     count = 0
#     for vs in puzzle.value_sets:
#         if len(vs) == 1:
#             count += 1
#     fixed = propagate_constraints(puzzle, 0)
#     count += fixed
#     while fixed != 0:
#         print("fixed: %d cells"%fixed)
#         fixed = propagate_constraints(puzzle, 0)
#         count += fixed
#     puzzle.print_puzzle()

# def cp_bug():
#     puzzle = Sudoku("", False)
#     puzzle.d = 9
#     puzzle.cell_dim = 3
#     puzzle.value_sets = [[1, 2, 5, 6, 7], [2, 4, 5, 7], [1, 2, 4, 6, 7], [1, 3, 4, 6, 7, 9], [1, 3, 4, 5, 9], [3, 4, 5, 6, 7], [1, 3, 7, 9], [1, 3, 5, 9], [8], [1, 2, 5, 6, 7, 8], [2, 5, 7, 8], [3], [1, 6, 7, 8, 9], [1, 5, 8, 9], [5, 6, 7, 8], [4], [1, 5, 9], [1, 2, 5, 7, 9], [1, 5, 7, 8], [9], [1, 4, 7], [1, 3, 4, 7, 8], [2], [3, 4, 5, 7, 8], [1, 3, 7], [6], [1, 5, 7], [1, 2, 3, 5, 8], [2, 3, 4, 5, 8], [1, 2, 4], [3, 4, 8], [7], [9], [1, 3, 6, 8], [1, 3, 4, 5, 8], [1, 4, 5, 6], [3, 5, 7, 8, 9], [3, 4, 5, 7, 8], [4, 7, 9], [3, 4, 8], [6], [1], [2], [3, 4, 5, 8, 9], [4, 5, 9], [1, 3, 8, 9], [6], [1, 4, 9], [5], [3, 4, 8], [2], [1, 3, 8, 9], [7], [1, 4, 9], [2, 3, 6, 7, 9], [2, 3, 7], [8], [1, 2, 3, 4, 6, 7, 9], [1, 3, 4, 9], [3, 4, 6, 7], [5], [1, 4, 9], [1, 4, 6, 7, 9], [3, 6, 7, 9], [1], [6, 7, 9], [3, 4, 6, 7, 8, 9], [3, 4, 5, 8, 9], [3, 4, 5, 6, 7, 8], [6, 7, 8, 9], [2], [4, 6, 7, 9], [4], [2, 7], [5], [1, 2, 6, 7, 8, 9], [1, 8, 9], [6, 7, 8], [1, 6, 7, 8, 9], [1, 8, 9], [3]]
#     puzzle.value_sets[16] = [1]
#     count = 0
#     num_originally_fixed = 0
#     for x in puzzle.value_sets:
#         if len(x) == 1:
#             num_originally_fixed += 1
#     fixed, failed = propagate_constraints(puzzle)
#     count += fixed
#     while fixed != 0:
#         print("fixed: %d cells" % fixed)
#         fixed, failed = propagate_constraints(puzzle)
#         count += fixed
#     num_actually_fixed = 0
#     for x in puzzle.value_sets:
#         if len(x) == 1:
#             num_actually_fixed += 1
#     print(num_originally_fixed + count)
#     print(num_actually_fixed)


def main():
    test_all_logic_solvable()


if __name__ == "__main__":
    main()