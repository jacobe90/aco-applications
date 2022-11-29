import math

from tsp import EuclideanTSP
import numpy as np

# SUS List
# what city should ants start at?
# no tau_0 calculation


def acs(tsp):
    # hyperparameters
    beta = 2
    q_0 = 0.9
    alpha = 0.1
    rho = 0.1
    m = 10 # number of ants

    # find tau_0 via nearest neighbor method
    tau_0 = 0
    tbv = list(range(tsp.n_cities))
    cur = 0
    tbv.remove(cur)
    while len(tbv) > 0:
        next_city = tbv[np.argmin(np.asarray(map(lambda c: tsp.distances[cur][c], tbv)))]
        tau_0 += tsp.distances[cur][next_city]
        cur = next_city
        tbv.remove(cur)
    tau_0 += tsp.distances[cur][0]

    # initialization phase
    pheromones = np.ones((tsp.n_cities, tsp.n_cities)) * tau_0
    r_i = np.random.randint(tsp.n_cities, size=m) # ant starting positions
    r = r_i.copy() # current positions of all the ants
    s = np.empty(m) # the next position of each ant
    J = np.empty((m, tsp.n_cities), dtype=set)
    for k in range(m):
        cities_to_visit = set(range(tsp.n_cities))
        cities_to_visit.remove(r_i[k])
        J[k][r_i[k]] = cities_to_visit

    while True:
        # tour-building phase
        Tour = np.empty((m, tsp.n), dtype=tuple)
        for i in range(tsp.n_cities):
            if i < tsp.n_cities - 1:
                for k in range(m):
                    # choose s[k]
                    q = np.random.uniform(0, 1)
                    if q < q_0:
                        idx = np.argmax(np.asarray(map(lambda u: tsp.distances[r[k]][u] * ((1/tsp.distances[r[k]][u]) ** beta),
                                                 J[k][r[k]])))
                        s[k] = J[k][r[k]][idx]
                    else:
                        total = sum(list(map(lambda u: tsp.distances[r[k]][u] * ((1/tsp.distances[r[k]][u]) ** beta),
                                             J[k][r[k]])))
                        probabilities = [tsp.distances[r[k]][u] for u in J[k][r[k]]]
                        s[k] = np.random.choice(J[k][r[k]], p=probabilities)
                    remaining = J[k][r[k]].copy()
                    remaining.remove(s[k])
                    J[k][s[k]] = remaining
                    Tour[k][i] = (r[k], s[k])
            else:
                for k in range(m):
                    # ants go back to initial city
                    s[k] = r_i[k]
                    Tour[k][i] = (r[k], s[k])

            # local updating phase
            for k in range(m):
                pheromones[r[k]][s[k]] = (1 - rho) * pheromones[r[k]][s[k]] + rho * tau_0 # Canonical ACS local update
                r[k] = s[k] # move ant to the next city

        # global update phase
        # Tour - array of tours
        # tour - array of tuples
        L = np.empty(m)
        for k in range(m):
            L[k] = sum(list(map(lambda edge: tsp.distances[edge[0]][edge[1]], Tour[k])))
        best_tour = Tour[np.argmin(L)]
        L_best = np.max(L)
        for i in range(tsp.n_cities):
            for j in range(tsp.n_cities):
                pheromones[i][j] = (1 - alpha) * pheromones[i][j]
        for edge in best_tour:
            pheromones[edge[0]][edge[1]] += alpha * (1 / L_best)

        print("L_best is {}".format(L_best))
