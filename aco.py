# TODO
# constraint propagation
# aco algorithm
# convert everything to numpy

# SUS List
# add get row, get column, get box functions DONE
# need to initialize ants to all different locations in the puzzle DONE
# need to track fail cells when doing constraint propagation DONE

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
    m = 10  # number of ants
    tau_0 = 1/(puzzle.d * puzzle.d) # initial pheromone values
    zeta = 0.1
    delta_tau_best = 0

    # puzzle parameters
    c = puzzle.d * puzzle.d # number of units
    d = puzzle.d # puzzle dimension
    best_solution = puzzle.copy()

    # constraint propagation on puzzle
    while propogate_constraints(best_solution)[0] != 0:
        continue

    # initialize global pheromone matrix
    pheromones = np.array([c, d])
    pheromones.fill(tau_0)

    while not best_solution.solved():
        # keep track of puzzles, cells set by each ant, and starting positions
        puzzle_copies = []
        cells_set = np.zeros(m)
        initial_positions = np.random.randint(c, size=m)

        for ant in range(0, m):
            puzzle_copies.append(best_solution.copy())
        for iter in range(0, c):
            for ant_idx in range(0, m):
                # if current cell is not fixed
                cur_pos = (initial_positions[ant_idx] + iter) % c
                copy = puzzle_copies[ant_idx]
                if len(copy.value_sets[cur_pos]) != 1:
                    # choose value
                    vs = copy.value_sets[cur_pos]
                    q = random.uniform(0, 1)
                    ants_choice = None
                    if q < q_0:
                        ants_choice = vs[np.argmax([pheromones[cur_pos][x] for x in vs])]
                    else:
                        sum = 0
                        for x in vs:
                            sum += pheromones[cur_pos][x]
                        probabilities = [pheromones[cur_pos][x]/sum for x in vs]
                        ants_choice = np.random.choice(vs, p=probabilities)
                    puzzle.value_sets[cur_pos] = [ants_choice]
                    # propagate constraints
                    fixed, failed = propogate_constraints(puzzle)
                    cells_set[ant_idx] += (fixed - failed)
                    while fixed != 0:
                        fixed, failed = propogate_constraints(puzzle)
                        cells_set[ant_idx] += (fixed - failed)
                    # local pheromone update
                    pheromones[cur_pos][ants_choice] = (1 - zeta) * pheromones[cur_pos][ants_choice] + zeta * tau_0
        # find best ant
        f_best = np.max(cells_set)
        delta_tau = c / (c - f_best)
        if delta_tau > delta_tau_best:
            best_solution = puzzle_copies[np.argmax(cells_set)]
            delta_tau_best = delta_tau

        # global pheromone update
        for i in range(c):
            if len(best_solution.value_sets[i]) == 1:
                val = best_solution.value_sets[i][0]
                pheromones[i][val] = (1 - rho) * pheromones[i][val] + rho * delta_tau_best

        # best value evaporation
        delta_tau_best = delta_tau_best * (1 - rho_bve)


def propogate_constraints(puzzle):
    # loop through all units
    # if the unit is already fixed, continue
    fixed_total = 0
    failed_total = 0
    for i in range(0, puzzle.d*puzzle.d):
        if len(puzzle.value_sets[i]) != 1:
            # get all fixed values from row, column, and box of the unit
            fixed_in_cell = set()
            for x in range(i - i % puzzle.d, i - i % puzzle.d + puzzle.d, 1):
                if len(puzzle.value_sets[x]) == 1:
                    fixed_in_cell.add(puzzle.value_sets[x][0])
            for x in range(i % puzzle.d, puzzle.d*puzzle.d,9):
                if len(puzzle.value_sets[x]) == 1:
                    fixed_in_cell.add(puzzle.value_sets[x][0])
            # x + 3y
            # x = (i%9)/3
            # y = (i/9)/3
            box_index = int((i % puzzle.d) / puzzle.cell_dim) + puzzle.cell_dim * int(int(i / puzzle.d) / puzzle.cell_dim)
            #print(box_index)
            for x in puzzle.get_box(box_index):
                if len(puzzle.value_sets[x]) == 1:
                    fixed_in_cell.add(puzzle.value_sets[x][0])
            # update the unit's value set
            #print(fixed_in_cell)
            for f in fixed_in_cell:
                if f in puzzle.value_sets[i]:
                    puzzle.value_sets[i].remove(f)

            # if unit is fixed
            if len(puzzle.value_sets[i]) == 1:
                fixed_total += 1

            # if unit is failed
            if len(puzzle.value_sets[i]) == 0:
                failed_total += 1

            # if any value is the only one of its kind in a row, column, or box
            for v in puzzle.value_sets[i]:
                # check if v is in the row, column, box
                # row
                row_singleton = True
                for x in range(i - i % puzzle.d, i - i % puzzle.d + puzzle.d, 1):
                    if x != i and v in puzzle.value_sets[x]:
                        row_singleton = False
                if row_singleton:
                    puzzle.value_sets[i] = [v]
                    fixed_total += 1
                    break

                # column
                column_singleton = True
                for x in range(i % puzzle.d, puzzle.d * puzzle.d, 9):
                    if x != i and v in puzzle.value_sets[x]:
                        column_singleton = False
                if column_singleton:
                    puzzle.value_sets[i] = [v]
                    fixed_total += 1
                    break

                # box
                box_singleton = True
                for x in puzzle.get_box(box_index):
                    if x != i and v in puzzle.value_sets[x]:
                        box_singleton = False
                if box_singleton:
                    puzzle.value_sets[i] = [v]
                    fixed_total += 1
                    break
    return fixed_total, failed_total
