import matplotlib.pyplot as plt
import os
import numpy as np


def main():
    # load everything into a dictionary
    averages = dict()
    for file in os.listdir("test_results"):
        with open("test_results/" + file, "r") as test_file:
            lines = test_file.readlines()
            avg = sum(list(map(lambda line: float(line[:-1]), lines))) / 100
            averages[file.split('_')[1][:-4]] = avg

    puzzles = list(averages.keys())
    avgs = list(averages.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(puzzles, avgs, color='blue',
            width=0.4)

    plt.ylabel("Time (sec)")
    plt.title("Average Solution Time (over 100 runs)")
    plt.show()


if __name__ == "__main__":
    main()