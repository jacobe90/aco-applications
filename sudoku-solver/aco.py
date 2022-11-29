# TODO
# constraint propagation
# aco algorithm
# convert everything to numpy

# SUS List
# add get row, get column, get box functions DONE
# need to initialize ants to all different locations in the puzzle DONE
# need to track fail cells when doing constraint propagation DONE

# Potential problems to investigate
# math for updating pheromones could be wrong
# constraint propagation messed up?
import time

import mpmath
import numpy as np
import math
import random

# class Ant:
#     def __int__(self, puzzle, idx):
#         self.puzzle = puzzle
#         self.idx = idx # current index of ant in the sudoku
#         self.cells_set = 0
#
#     def step():
#
#         idx += 1


def aco(puzzle):
    # set hyperparameters
    rho = 0.9
    q_0 = 0.9
    rho_bve = 0.005
    m = 10
    # number of ants
    tau_0 = 1/(puzzle.d * puzzle.d) # initial pheromone values
    zeta = 0.1
    delta_tau_best = 0

    # puzzle parameters
    c = puzzle.d * puzzle.d # number of units
    d = puzzle.d # puzzle dimension

    cp_time = 0
    # constraint propagation on puzzle
    t0 = time.time()
    propagate_constraints(puzzle, 0)
    cp_time = cp_time + (time.time() - t0)
    # copy the puzzle
    best_solution = puzzle.copy()
    f_start = 0
    for vs in puzzle.value_sets:
        if len(vs) == 1:
            f_start += 1

    # initialize global pheromone matrix
    pheromones = np.zeros((c, d))
    pheromones.fill(tau_0)

    count = 0
    while not best_solution.solved():
        count += 1
        # keep track of puzzles, cells set by each ant, and starting positions
        puzzle_copies = []
        cells_set = np.zeros(m)
        cells_set.fill(f_start)
        initial_positions = np.random.randint(c, size=m)

        for ant in range(0, m):
            puzzle_copies.append(puzzle.copy())
        for iter in range(0, c):
            for ant_idx in range(0, m):
                # if current cell is not fixed
                cur_pos = (initial_positions[ant_idx] + iter) % c
                copy = puzzle_copies[ant_idx]
                if len(copy.value_sets[cur_pos]) > 1:
                    # choose value
                    vs = copy.value_sets[cur_pos]
                    q = random.uniform(0, 1)
                    ants_choice = None
                    if q < q_0:
                        j = pheromones[cur_pos]
                        ants_choice = max(vs, key=lambda x:(pheromones[cur_pos][x-1])) # BUG - this is wrong. surprised things are still working so well
                    else:
                        sum = 0
                        for x in vs:
                            sum += pheromones[cur_pos][x-1]
                        probabilities = [pheromones[cur_pos][x-1]/sum for x in vs]
                        ants_choice = np.random.choice(vs, p=probabilities)
                    copy.value_sets[cur_pos] = [ants_choice]
                    # propagate constraints
                    t0 = time.time()
                    fixed = propagate_constraints(copy, 0)
                    while fixed != 0:
                        fixed = propagate_constraints(copy, 0)
                    # #cells_set[ant_idx] += fixed
                    # while fixed != 0:
                    #     fixed = propagate_constraints(copy, cur_pos)
                    #     #cells_set[ant_idx] += fixed
                    cp_time = cp_time + (time.time() - t0)
                    # local pheromone update
                    pheromones[cur_pos][ants_choice-1] = (1 - zeta) * pheromones[cur_pos][ants_choice-1] + zeta * tau_0
                    if ant_idx == 0:
                        num_fixed = cells_set[ant_idx]
                        num_actually_fixed = 0
                        for x in copy.value_sets:
                            if len(x) == 1:
                                num_actually_fixed += 1
                        #copy.print_puzzle()
                        #print("\n")
        # find best ant
        cells_set = [copy.filled() for copy in puzzle_copies]
        f_best = max(cells_set)
        delta_tau = 0
        if f_best != puzzle.d * puzzle.d:
            delta_tau = c / (c - f_best)
        else:
            best_solution = puzzle_copies[np.argmax(cells_set)]
            best_solution.print_puzzle()
            return best_solution, count, cp_time

        if delta_tau > delta_tau_best:
            best_solution = puzzle_copies[np.argmax(cells_set)]
            delta_tau_best = delta_tau

        fixed_count = 0
        for vs in best_solution.value_sets:
            if len(vs) == 1:
                fixed_count += 1
        # if count % 10 == 0:
        #     print("Global Iteration %d" % count)
        #     print("Best ant fixed {}/{} cells".format(fixed_count, c))
        #     best_solution.print_puzzle()
        #     print("\n")
        # global pheromone update
        for i in range(c):
            if len(best_solution.value_sets[i]) == 1:
                val = best_solution.value_sets[i][0]
                pheromones[i][val-1] = (1 - rho) * pheromones[i][val-1] + rho * delta_tau_best

        # best value evaporation
        delta_tau_best = delta_tau_best * (1 - rho_bve)

    return best_solution, count, cp_time


def propagate_constraints(puzzle, i):
    row = puzzle.get_row(i)
    column = puzzle.get_column(i)
    box = puzzle.get_box(i)

    for unit in set(row + column + box):
        # TODO - replace with constant time lookup somehow
        # another data structure in Sudoku class?

        if unit != i and len(puzzle.value_sets[unit]) > 1:
            fixed_in_cell = set()
            unit_row = puzzle.get_row(unit)
            unit_col = puzzle.get_column(unit)
            unit_box = puzzle.get_box(unit)
            for x in unit_row:
                if len(puzzle.value_sets[x]) == 1:
                    fixed_in_cell.add(puzzle.value_sets[x][0])
            for x in unit_col:
                if len(puzzle.value_sets[x]) == 1:
                    fixed_in_cell.add(puzzle.value_sets[x][0])
            for x in unit_box:
                if len(puzzle.value_sets[x]) == 1:
                    fixed_in_cell.add(puzzle.value_sets[x][0])
            for f in fixed_in_cell:
                try:
                    puzzle.value_sets[unit].remove(f)
                except ValueError:
                    pass
            # if unit is fixed
            if len(puzzle.value_sets[unit]) == 1:
                return 1 + propagate_constraints(puzzle, unit)

            # check to see if unit contains any singleton values for its row/column
            for v in puzzle.value_sets[unit]:
                # check if v is in the row, column, box
                # row
                row_singleton = True
                for x in unit_row:
                    if x != unit and v in puzzle.value_sets[x]:
                        row_singleton = False
                if row_singleton:
                    puzzle.value_sets[unit] = [v]
                    return 1 + propagate_constraints(puzzle, unit)

                # column
                column_singleton = True
                for x in unit_col:
                    if x != unit and v in puzzle.value_sets[x]:
                        column_singleton = False
                if column_singleton:
                    puzzle.value_sets[unit] = [v]
                    return 1 + propagate_constraints(puzzle, unit)

                # box
                box_singleton = True
                for x in unit_box:
                    if x != unit and v in puzzle.value_sets[x]:
                        box_singleton = False
                if box_singleton:
                    puzzle.value_sets[unit] = [v]
                    return 1 + propagate_constraints(puzzle, unit)
    return 0
