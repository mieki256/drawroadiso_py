#!python
# -*- mode: python; Encoding: utf-8; coding: utf-8 -*-
# Last updated: <2024/04/22 01:03:07 +0900>
"""
Draw a line by matplotlib

読み込んだcsvの座標値を matplotlib で描画

Usage:
    python draw_line_plot.py INPUT.csv

Windows10 x64 22H2 + Python 3.10.10 64bit + matplotlib 3.8.4
"""

import sys
import matplotlib.pyplot as plt


def loadData(infile):
    ax = []
    ay = []
    with open(infile, "r") as file:
        for line in file:
            line = line.rstrip()
            x, y = line.split(",")
            x = float(x)
            y = float(y)
            ax.append(x)
            ay.append(y)
    return ax, ay


if len(sys.argv) < 2:
    sys.exit()

infile = sys.argv[1]
x, y = loadData(infile)

plt.plot(x, y, color="cyan", label="Data (line)")
plt.plot(x, y, "r.", label="Data (point)")

plt.legend(loc="best")
# plt.savefig("output_graph.png")
plt.show()
