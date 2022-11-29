from tsp import EuclideanTSP
import numpy as np

def acs(tsp):
    # hyperparameters
    beta = 2
    q_0 = 0.9
    alpha = 0.1
    rho = 0.1
    m = 10 # number of ants
    tau_0 = None # gonna take some implementation to generate this

    # initialization phase
    pheromones = np.ones((tsp.n_cities, tsp.n_cities)) * tau_0
    r_i = np.random.randint(tsp.n_cities, size=m) # ant starting positions
    r = r_i.copy() # current positions of all the ants
    s = np.empty(m) # the next position of each ant
    J = np.empty((m, tsp.n_cities), set)
    for k in range(m):
        J[k][r_i[k]] = set(range(tsp.n_cities)).remove(r_i[k])