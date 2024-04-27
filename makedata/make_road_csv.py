#!python
# -*- mode: python; Encoding: utf-8; coding: utf-8 -*-
# Last updated: <2024/04/27 08:21:20 +0900>
"""
Make road data csv

Usage:
    python make_road_csv.py INPUT_spline.csv > OUTPUT.csv

Windows10 x64 22H2 + Python 3.10.10 64bit

by mieki256
License: CC0 / Public Domain
"""

import os
import sys
import math
import random

ROADW = 40.0

centers = []  # road center line
roads = []  # road edge
wlines = []  # road white line
trees = []
stg_xmin, stg_ymin = 0.0, 0.0
stg_xmax, stg_ymax = 0.0, 0.0
stg_width, stg_height = 0.0, 0.0

tree_cols_len = 6


def create_trees():
    global trees
    for i in range(len(centers) - 1):
        fg = 0
        x, y, r = 0.0, 0.0, 0.0
        c = 0
        if random.random() < 0.4:
            x0, y0 = centers[i]
            x1, y1 = centers[i + 1]
            xd, yd = x1 - x0, y1 - y0

            # normalize vector
            lg = math.sqrt(xd * xd + yd * yd)
            wx = xd / lg
            wy = yd / lg

            w = random.randint(100, 400)
            xa = -wy * w
            ya = wx * w
            if i % 2 == 0:
                x = x0 + xa
                y = y0 + ya
            else:
                x = x0 - xa
                y = y0 - ya
            r = random.randint(25, 50)
            c = random.randint(0, tree_cols_len - 1)

            # Check for collisions between trees and the road. very slow
            fg = 1
            for pos in centers:
                cx, cy = pos
                if (((x - cx) ** 2) + ((y - cy) ** 2)) < ((r + ROADW) ** 2):
                    fg = 0
                    break

        if fg:
            trees.append({"fg": 1, "x": x, "y": y, "r": r, "col": c})
        else:
            trees.append({"fg": 0, "x": 0, "y": 0, "r": 0, "col": 0})


def calc_road_edge(xs, ys):
    """save road center and edge position."""
    global centers, roads, wlines
    global stg_xmin, stg_ymin
    global stg_xmax, stg_ymax
    global stg_width, stg_height

    centers = []
    roads = []
    wlines = []

    scale = 1000000.0
    linew = 2.0
    for i in range(len(xs)):
        # save road center
        x0, y0 = xs[i] * scale, ys[i] * scale
        centers.append([x0, y0])
        if i >= len(xs) - 1:
            break

        # save road edge
        x1, y1 = xs[i + 1] * scale, ys[i + 1] * scale
        xd, yd = x1 - x0, y1 - y0
        lg = math.sqrt(xd * xd + yd * yd)
        wx = xd / lg
        wy = yd / lg
        px2 = x0 - (wy * (ROADW * 1.0))
        py2 = y0 + (wx * (ROADW * 1.0))
        px3 = x0 + (wy * (ROADW * 1.0))
        py3 = y0 - (wx * (ROADW * 1.0))
        roads.append([px2, py2, px3, py3])

        # save white line edge
        lx2 = x0 - (wy * (linew * 1.0))
        ly2 = y0 + (wx * (linew * 1.0))
        lx3 = x0 + (wy * (linew * 1.0))
        ly3 = y0 - (wx * (linew * 1.0))
        wlines.append([lx2, ly2, lx3, ly3])

    stg_xmin, stg_ymin, stg_xmax, stg_ymax = get_area_size(roads)
    stg_width = stg_xmax - stg_xmin
    stg_height = stg_ymax - stg_ymin
    # print(f"area = ( {stage_xmin}, {stage_ymin} ) - ( {stage_xmax}, {stage_ymax} )")
    # print(f"area size w x h = {stage_width} x {stage_height}")


def get_area_size(roads):
    xmin, ymin = roads[0][0], roads[0][1]
    xmax, ymax = xmin, ymin
    for i in range(len(roads)):
        x0, y0, x1, y1 = roads[i]
        if x0 < xmin:
            xmin = x0
        if x1 < xmin:
            xmin = x1
        if x0 > xmax:
            xmax = x0
        if x1 > xmax:
            xmax = x1
        if y0 < ymin:
            ymin = y0
        if y1 < ymin:
            ymin = y1
        if y0 > ymax:
            ymax = y0
        if y1 > ymax:
            ymax = y1

    return (xmin, ymin, xmax, ymax)


def load_csv(infile):
    ax = []
    ay = []
    with open(infile, "r") as file:
        for line in file:
            line = line.rstrip()
            x, y = line.split(",")
            ax.append(float(x))
            ay.append(float(y))
    return ax, ay


def main():
    if len(sys.argv) != 2:
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} INPUT.csv")
        sys.exit()

    # load csv and initialize work
    infile = sys.argv[1]
    xs, ys = load_csv(infile)

    random.seed()
    calc_road_edge(xs, ys)
    create_trees()

    print(
        f"# length,centers={len(centers)},roads={len(roads)},wlines={len(wlines)},trees={len(trees)}"
    )

    print(
        "# center_x,center_y,road_x0,road_y0,road_x1,road_y1,line_x0,line_y0,line_x1,line_y1,tree_fg,tree_x,tree_y,tree_r,tree_col"
    )
    for i in range(len(centers)):
        cx, cy = centers[i]
        if i < len(centers) - 1:
            rx0, ry0, rx1, ry1 = roads[i]
            lx0, ly0, lx1, ly1 = wlines[i]
            t = trees[i]
            tfg, tx, ty, r, col = t["fg"], t["x"], t["y"], t["r"], t["col"]
            print(
                f"{cx},{cy},{rx0},{ry0},{rx1},{ry1},{lx0},{ly0},{lx1},{ly1},{tfg},{tx},{ty},{r},{col}"
            )
        else:
            print(f"{cx},{cy},0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0")


if __name__ == "__main__":
    main()
