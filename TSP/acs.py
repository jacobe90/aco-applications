import math

from tsp import EuclideanTSP
import numpy as np

# SUS List
# what cit(y)(ies) SHOULD the ants start at?
# cooler visualization - actually show how the pheromone strengths change over time
print("")


def acs(tsp, n_iters, get_animation=False):
    best_tours = []
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
        next_city = tbv[np.argmin(np.asarray(map(lambda c: tsp.distance(cur, c), tbv)))]
        tau_0 += tsp.distance(cur, next_city)
        cur = next_city
        tbv.remove(cur)
    tau_0 += tsp.distance(cur, 0)

    # initialization phase
    pheromones = np.ones((tsp.n_cities, tsp.n_cities)) * tau_0
    r_i = np.random.randint(tsp.n_cities, size=m) # ant starting positions
    r = r_i.copy() # current positions of all the ants
    s = np.empty(m, dtype=int) # the next position of each ant
    J = np.empty((m, tsp.n_cities), dtype=list)
    L_best = math.inf
    best_tour = None
    iters = 0
    for k in range(m):
        cities_to_visit = list(range(tsp.n_cities))
        cities_to_visit.remove(r_i[k])
        J[k][r_i[k]] = cities_to_visit

    while iters < n_iters:
        iters += 1
        # tour-building phase
        Tour = np.empty((m, tsp.n_cities), dtype=tuple)
        for i in range(tsp.n_cities):
            # print("city {}/{}", i, tsp.n_cities)
            if i < tsp.n_cities - 1:
                for k in range(m):
                    # choose s[k]
                    q = np.random.uniform(0, 1)
                    if q < q_0:
                        jman = (map(lambda u: tsp.distances[r[k]][u] * ((1 / tsp.distance(r[k], u)) ** beta),
                                       J[k][r[k]]))
                        idx = np.argmax(np.asarray(list(map(lambda u: tsp.distance(r[k], u) * ((1/tsp.distance(r[k], u)) ** beta),
                                                 J[k][r[k]]))))
                        #print(idx)
                        s[k] = J[k][r[k]][idx]
                    else:
                        total = sum(list(map(lambda u: tsp.distance(r[k], u) * ((1/tsp.distance(r[k], u)) ** beta),
                                             J[k][r[k]])))
                        probabilities = [tsp.distance(r[k], u) * ((1/tsp.distance(r[k], u)) ** beta) / total for u in J[k][r[k]]]
                        s[k] = np.random.choice(J[k][r[k]], p=probabilities)
                        jman_is_cool = s[k]
                    remaining = J[k][r[k]].copy()
                    remaining.remove(s[k])
                    c = J[k]
                    d = s[k]
                    J[k][int(s[k])] = remaining
                    Tour[k][i] = (r[k], s[k])
            else:
                for k in range(m):
                    # ants go back to initial city
                    s[k] = r_i[k]
                    Tour[k][i] = (r[k], s[k])

            # local updating phase
            for k in range(m):
                # jacob = (1 - rho) * pheromones[int(r[k])][int(s[k])] + rho * tau_0
                pheromones[r[k]][int(s[k])] = (1 - rho) * pheromones[r[k]][int(s[k])] + rho * tau_0 # Canonical ACS local update
                r[k] = s[k] # move ant to the next city

        # global update phase
        # Tour - array of tours
        # tour - array of tuples
        L = np.empty(m)
        for k in range(m):
            L[k] = sum(list(map(lambda edge: tsp.distance(int(edge[0]), int(edge[1])), Tour[k])))
        L_max = np.min(L)
        if L_max < L_best:
            L_best = L_max
            best_tour = Tour[np.argmin(L)]
        for i in range(tsp.n_cities):
            for j in range(tsp.n_cities):
                pheromones[i][j] = (1 - alpha) * pheromones[i][j]
        for edge in best_tour:
            pheromones[int(edge[0])][int(edge[1])] += alpha * (1 / L_best)
        # if iters % 1 == 0:
        print("Iteration {}/5000, current best tour is size {}".format(iters, L_best))
        if iters % int(n_iters / 10) == 0 and get_animation:
            best_tours.append(best_tour.copy())
    print("L_best is {}".format(L_best))
    return best_tour if not get_animation else best_tours
