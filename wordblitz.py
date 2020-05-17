#!/usr/bin/env python3

import pyautogui
import json
import argparse
import tkinter as tks
import collections
import random
import numpy as np
from typing import List, Dict
import colorful as cf

ROWS = 4
COLS = 4
english_words = None  # dictionary

grid_to_pix = collections.defaultdict(list)
found = set()


def load_words() -> Dict:
    with open('words_dictionary.json') as word_file:
        valid_words = json.load(word_file)
    return valid_words


def draw(coords: List) -> None:
    pass


dirs = ((-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1))

words_found = []


def dfs(grid, start: tuple, build=[], build_coord=[], visited=set(), depth=1, max_depth=10) -> None:
    """
    Searches for words in the grid with max depth of 10
    """
    if depth >= max_depth:
        return
    visited.add(start)
    build.append(grid[start[0]][start[1]])
    build_coord.append(start)
    b = ''.join(build)
    # print(b, visited)
    if b.lower() in english_words:
        # print(b)
        # print(build_coord)
        found.add(b.lower())
        words_found.append([b, build_coord[:]])
    for x, y in dirs:
        i = start[0] + x
        j = start[1] + y
        if i >= 0 and i < ROWS and j >= 0 and j < COLS:
            if (i, j) not in visited:
                c = visited.copy()
                dfs(grid, (i, j), build.copy(), build_coord.copy(),
                    c, depth + 1, max_depth)  # add the next one


def search(grid, depth=10):
    for i in range(ROWS):
        for j in range(COLS):
            print('searching cell', i, j)
            dfs(grid, (i, j), build=[], build_coord=[], visited=set(), depth)


def populate(grid=None) -> List[List]:
    """
    Populates empty grid or returns a new one

    # Args:
        grid: None

    # Returns:
        Generated Grid: list
    """
    if not grid:
        grid = [[None]*COLS for i in range(ROWS)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = chr(ord('A') + random.randint(0, 25))
    return grid


if __name__ == '__main__':
    # demo print
    parser = argparse.ArgumentParser(description="Cheat at wordblitz")
    parser.add_argument('-d', '--depth', type=int,
                        help='depth of the word search. eg. longest word that can be found', default=10)
    parser.add_argument(
        '-s', '--source', help='source of where grid is from, default is pulling from website (you need to have the game open)', choices=['browser'], default='browser')
    parser.add_argument('-test', help="testing mode",
                        action='store_true')
    args = parser.parse_args()
    depth = args.depth
    source = args.source
    testing_mode = args.test
    english_words = load_words()
    cf.use_style('solarized')
    print(cf.bold_yellow(f'Dict size: {len(english_words)}'))
    print('depth is', depth)
    print('source is ', source)
    print('testing mode is', testing_mode)
    grid = populate()
    print("Grid is")
    print(np.asarray(grid))
    # TODO: populate grid
    # TODO: find the pixel values of each grid value (could be manual)

    print(pyautogui.size())
    search(grid, depth)
    print(
        cf.green(f'we have found {len(words_found)} words... running draw algorithm'))
    words_found = sorted(words_found, key=lambda k: -len(k[0]))  # max score?
    print(words_found)
