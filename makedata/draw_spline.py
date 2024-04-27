#!python
# -*- mode: python; Encoding: utf-8; coding: utf-8 -*-
# Last updated: <2024/04/25 20:37:28 +0900>
"""
Draw a spline based on the csv output by QGIS

QGISからエクスポート、エディタで編集して作成したcsvを読み込んで、
scipyでスプライン補間する。結果は matplotlib で描画する。

Usage:
    python draw_spline.py INPUT.csv

Windows10 x64 22H2 + Python 3.10.10 64bit
scipy 1.13.0 + numpy 1.26.4 + matplotlib 3.8.4

Reference:

スプライン曲線と補間 - Emotion Explorer
https://emotionexplorer.blog.fc2.com/blog-entry-229.html
"""

import sys
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt


# S = 10
S = 20


def loadData(infile):
    ax = []
    ay = []
    with open(infile, "r") as file:
        for line in file:
            line = line.rstrip()
            x, y = line.split(",")
            x = float(x)
            y = float(y) * 1.3
            ax.append(x)
            ay.append(y)
    return ax, ay


# B-Spline 補間
def spline1(x, y):
    tck, u = interpolate.splprep([x, y], k=3, s=0)
    u = np.linspace(0, 1, num=len(x) * S, endpoint=True)
    spline = interpolate.splev(u, tck)
    return spline[0], spline[1]


# interp1dスプライン補間による曲線
def spline3(x, y):
    t = np.linspace(0, 1, len(x), endpoint=True)
    fx = interpolate.interp1d(t, x, kind="cubic")
    fy = interpolate.interp1d(t, y, kind="cubic")
    ta = np.linspace(0, 1, len(x) * S, endpoint=True)
    return fx(ta), fy(ta)


if len(sys.argv) < 2:
    sys.exit()

infile = sys.argv[1]
x, y = loadData(infile)

# B-Spline interpolation
bx, by = spline1(x, y)

# interp1d spline
ax, ay = spline3(x, y)

plt.plot(x, y, "ro", label="Data")
# plt.plot(bx, by, "b.", label="B-Spline interpolation")
plt.plot(bx, by, color="blue", label="B-Spline interpolation")
plt.plot(ax, ay, color="green", label="interp1d")

plt.legend(loc="best")
plt.savefig("output_graph.png")
plt.show()
