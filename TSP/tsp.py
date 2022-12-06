import numpy as np
import math
from matplotlib import pyplot as plt


class EuclideanTSP:
    def __init__(self, path):
        self.name = None
        self.n_cities = None
        self.V = []
        self.load(path)
        self.distances = np.empty((self.n_cities, self.n_cities))
        # self.calc_distances()

    def load(self, path):
        with open(path, 'r') as fin:
            N = 7
            header = [next(fin) for x in range(N)]
            self.name = header[0].split(" : ")[1]
            self.n_cities = int(header[4].split(" : ")[1])
            self.V = [next(fin).split(" ")[1:] for x in range(self.n_cities)]
            self.V = list(filter(lambda a: len(a) > 1, self.V))
            self.V = list(map(lambda a: (float(a[0]), float(a[1].strip('\n'))) if len(a) > 1 else None, self.V))

    def distance(self, i, j):
        x = self.V[i]
        y = self.V[j]
        dist = math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)
        if dist == 0:
            return 0.001
        return dist

    def calc_distances(self):
        for i in range(self.n_cities):
            for j in range(self.n_cities):
                x = self.V[i]
                y = self.V[j]
                self.distances[i][j] = math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

    def animate_from_file(self, file):
        tours = []
        with open(file) as acs_trace:
            cur_line = acs_trace.readline()
            tours = []
            count = 0
            while cur_line:
                count += 1
                print("reading line {}".format(count))
                if not cur_line == "same\n":
                    print("cur line is {}, len {}".format(cur_line, len(cur_line)))
                    tours.append(list(map(lambda s: tuple(map(lambda x: int(x), s.split(","))), list(filter(lambda a: a!='\n', cur_line.split(" "))))))
                # else:
                #     tours.append(tours[-1])
                cur_line = acs_trace.readline()
        plt.plot([x for x in list(map(lambda p: p[0], self.V))], [y for y in list(map(lambda p: p[1], self.V))],
                 'ro')
        plt.show(block=False)
        n_iters = len(tours)
        count = 1
        for best_tour in tours:
            plt.clf()
            plt.title("tour length: {}".format(sum(list(map(lambda tup: self.distance(tup[0], tup[1]), best_tour)))))
            plt.plot([x for x in list(map(lambda p: p[0], self.V))], [y for y in list(map(lambda p: p[1], self.V))],
                     'ro')
            x = list(map(lambda p: self.V[p[0]], best_tour))
            y = list(map(lambda p: self.V[p[1]], best_tour))
            for i in range(self.n_cities):
                plt.plot([x[i][0], y[i][0]], [x[i][1], y[i][1]], 'b-')
            plt.draw()
            input("Press Enter to continue...")
            plt.pause(1)
            count += 1
        input("press enter bud")
