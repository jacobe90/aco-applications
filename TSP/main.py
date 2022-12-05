from tsp import EuclideanTSP
from acs import acs
import matplotlib.pyplot as plt


def wi29_visualization():
    etsp = EuclideanTSP("wi29.tsp")
    plt.plot([x for x in list(map(lambda p: p[0], etsp.V))], [y for y in list(map(lambda p: p[1], etsp.V))], 'ro')
    plt.show(block=False)
    n_iters = 50
    best_tours = acs(etsp, n_iters, get_animation=True)
    count = 0
    for best_tour in best_tours:
        plt.clf()
        plt.title("iteration {}/{}".format(count, n_iters))
        plt.plot([x for x in list(map(lambda p: p[0], etsp.V))], [y for y in list(map(lambda p: p[1], etsp.V))], 'ro')
        x = list(map(lambda p: etsp.V[p[0]], best_tour))
        y = list(map(lambda p: etsp.V[p[1]], best_tour))
        for i in range(etsp.n_cities):
            plt.plot([x[i][0], y[i][0]], [x[i][1],y[i][1]], 'b-')
        plt.draw()
        plt.pause(1)
        count += n_iters / 10


def ar1952():
    etsp = EuclideanTSP("ar9152.tsp")
    plt.plot([x for x in list(map(lambda p: p[0], etsp.V))], [y for y in list(map(lambda p: p[1], etsp.V))], 'ro')
    plt.show(block=False)
    n_iters = 10
    best_tours = acs(etsp, n_iters, get_animation=True)
    count = 0
    for best_tour in best_tours:
        plt.clf()
        plt.title("iteration {}/{}".format(count, n_iters))
        plt.plot([x for x in list(map(lambda p: p[0], etsp.V))], [y for y in list(map(lambda p: p[1], etsp.V))], 'ro')
        x = list(map(lambda p: etsp.V[p[0]], best_tour))
        y = list(map(lambda p: etsp.V[p[1]], best_tour))
        for i in range(etsp.n_cities):
            plt.plot([x[i][0], y[i][0]], [x[i][1], y[i][1]], 'b-')
        plt.draw()
        plt.pause(1)
        count += n_iters / 10


def qatar():
    etsp = EuclideanTSP("qa194.tsp")
    plt.plot([x for x in list(map(lambda p: p[0], etsp.V))], [y for y in list(map(lambda p: p[1], etsp.V))], 'ro')
    plt.show(block=False)
    n_iters = 100
    best_tours = acs(etsp, n_iters, get_animation=True)
    count = 0
    for best_tour in best_tours:
        plt.clf()
        plt.title("iteration {}/{}".format(count, n_iters))
        plt.plot([x for x in list(map(lambda p: p[0], etsp.V))], [y for y in list(map(lambda p: p[1], etsp.V))], 'ro')
        x = list(map(lambda p: etsp.V[p[0]], best_tour))
        y = list(map(lambda p: etsp.V[p[1]], best_tour))
        for i in range(etsp.n_cities):
            plt.plot([x[i][0], y[i][0]], [x[i][1], y[i][1]], 'b-')
        plt.draw()
        plt.pause(1)
        count += n_iters / 10


def main():
    etsp = EuclideanTSP("wi29.tsp")
    acs(etsp, 5000, local_search=True)
    print(etsp.V)


if __name__ == "__main__":
    wi29_visualization()