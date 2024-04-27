#!python
# -*- mode: python; Encoding: utf-8; coding: utf-8 -*-
# Last updated: <2024/04/22 01:02:32 +0900>
"""
Draw a line based on the csv output by QGIS

QGISからエクスポート、エディタで編集して作成したcsvを読み込んで、
pygameで描画する

Usage: python draw_line.py INPUT.csv

Windows10 x64 22H2 + Python 3.10.10 64bit + pygame 2.5.2
by mieki256
License: CC0 / Public Domain
"""

import sys
import pygame
from pygame.locals import *

SCRW, SCRH = 1280, 720


def read_csv(infile):
    data = []
    with open(infile, "r") as file:
        for line in file:
            line = line.rstrip()
            x, y = line.split(",")
            x = float(x)
            y = float(y)
            data.append({"x": x, "y": y})
    return data


def get_pos_list(infile):
    srcdata = read_csv(infile)
    xlist = [v["x"] for v in srcdata]
    ylist = [v["y"] for v in srcdata]
    xmin = min(xlist)
    xmax = max(xlist)
    ymin = min(ylist)
    ymax = max(ylist)
    xa = xmax - xmin
    ya = ymax - ymin
    cx = (xmin + xmax) / 2.0
    cy = (ymin + ymax) / 2.0
    scale = xa if xa > ya else ya

    print(f"xmin = {xmin}")
    print(f"ymin = {ymin}")
    print(f"xmax = {xmax}")
    print(f"ymax = {ymax}")
    print(f"x_range = {xa}")
    print(f"y_range = {ya}")
    print(f"scale = {scale}")

    data = []
    for i in range(len(xlist)):
        x = (xlist[i] - cx) / (scale / 2.0)
        y = -(ylist[i] - cy) / (scale / 2.0)
        data.append({"x": x, "y": y})

    return data


def main():
    if len(sys.argv) < 2:
        sys.exit()

    infile = sys.argv[1]
    data = get_pos_list(infile)

    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCRW, SCRH))

    idx = 0
    running = True
    clock = pygame.time.Clock()

    # main loop
    while running:
        pygame.display.update()

        # clea screen
        screen.fill((255, 255, 255))

        # check key event
        for ev in pygame.event.get():
            if ev.type == QUIT:
                running = False
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE or ev.key == K_q:
                    # ESC key or Q key to exit
                    running = False
                if ev.key == K_UP:
                    idx = (idx + 1) % (len(data) - 1)
                if ev.key == K_DOWN:
                    idx = (idx - 1 + len(data) - 1) % (len(data) - 1)

        # check key pressed
        pygame.event.pump()
        pressed = pygame.key.get_pressed()
        if pressed[K_RIGHT]:
            idx = (idx + 1) % (len(data) - 1)
        if pressed[K_LEFT]:
            idx = (idx - 1 + len(data) - 1) % (len(data) - 1)

        # draw lines
        scale = (SCRW - 16) / 2
        bx = SCRW / 2
        by = SCRH / 2
        for i in range(len(data) - 1):
            if i >= len(data) - 1:
                continue

            x0, y0 = data[i]["x"], data[i]["y"]
            x1, y1 = data[i + 1]["x"], data[i + 1]["y"]

            x0 = x0 * scale + bx
            x1 = x1 * scale + bx

            # y0 = y0 * scale + by
            # y1 = y1 * scale + by

            y0 = y0 * scale * 1.3 + by
            y1 = y1 * scale * 1.3 + by

            if i == idx:
                pygame.draw.line(screen, (255, 0, 0), (x0, y0), (x1, y1), 3)
                pygame.draw.circle(screen, (0, 128, 128), (x0, y0), 16, 1)
            else:
                pygame.draw.line(screen, (0, 0, 0), (x0, y0), (x1, y1))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
