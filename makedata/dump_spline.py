#!python
# -*- mode: python; Encoding: utf-8; coding: utf-8 -*-
# Last updated: <2024/04/25 20:41:19 +0900>
"""
Output spline curve data

QGISからエクスポート、エディタで編集して作成したcsvを読み込んで、
scipyでスプライン補間した値を出力する。

Usage:
    python dump_spline.py -i INPUT.csv > OUTPUT.csv

Windows10 x64 22H2 + Python 3.10.10 64bit
scipy 1.13.0 + numpy 1.26.4
"""

import argparse
import sys
import numpy as np
from scipy import interpolate


# load csv file
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


# B-Spline
def spline1(x, y, s):
    tck, u = interpolate.splprep([x, y], k=3, s=0)
    u = np.linspace(0, 1, num=len(x) * s, endpoint=True)
    spline = interpolate.splev(u, tck)
    return spline[0], spline[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Input csv file")
    parser.add_argument("-n", "--num", type=int, default=10, help="number")
    args = parser.parse_args()

    if args.input is None:
        sys.exit()

    x, y = loadData(args.input)
    bx, by = spline1(x, y, args.num)

    for i in range(len(bx)):
        print(f"{bx[i]},{by[i]}")


if __name__ == "__main__":
    main()
