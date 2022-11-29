class EuclideanTSP:
    def __init__(self, path):
        self.name = None
        self.n_cities = None
        self.V = []
        self.load(path)

    def load(self, path):
        with open(path, 'r') as fin:
            N = 8
            header = [next(fin) for x in range(N)]
            self.name = header[0].split(" : ")[1]
            self.n_cities = int(header[4].split(" : ")[1])
            self.V = [next(fin).split(" ")[1:] for x in range(self.n_cities)]
            self.V = list(filter(lambda a: len(a) > 1, self.V))
            self.V = list(map(lambda a: (float(a[0]), float(a[1].strip('\n'))) if len(a) > 1 else None, self.V))