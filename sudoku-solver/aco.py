import time
import numpy as np
import random


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
                    # propagate constraints
                    t0 = time.time()
                    copy.assign(cur_pos, ants_choice)
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

