from tsp import EuclideanTSP
from acs import acs


def main():
    etsp = EuclideanTSP("wi29.tsp")
    acs(etsp)
    print(etsp.V)


if __name__ == "__main__":
    main()