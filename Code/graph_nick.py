#!/usr/bin/env python

import matplotlib.pyplot as plt

def plot(x,y, name, truths):
    colors = ['green' if truth else 'red' for truth in truths]

    plt.scatter(x, y, c=colors, marker='o')

    plt.title(f"Time Complexity for {name}")

    plt.xlabel("Variables in SAT Problem")
    plt.ylabel("Time to Compute (microseconds)")

    plt.savefig(f"../Graphs/plot_{name}_time_complexity.pdf", format='pdf')

    plt.show()

def plot_both(x,y1, y2):
    fig, ax = plt.subplots()

    ax.scatter(x, y2, label='DumbSAT', marker='s')
    ax.scatter(x, y1, label='DPLL', marker='^')

    ax.set_xlabel('Variables in SAT Problem')
    ax.set_ylabel('Time to Compute (microseconds)')
    ax.set_title('Time Complexity for DumbSAT v DPLL')
    ax.legend()

    plt.savefig(f"../Graphs/plot_both_time_complexity.pdf", format='pdf')
    plt.show()