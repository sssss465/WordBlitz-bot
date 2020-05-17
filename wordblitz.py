#!/usr/bin/env python3

import pyautogui
import json
import argparse
import tkinter as tks
import collections
import random
import numpy as np

ROWS = 4
COLS = 4

grid_to_pix = collections.defaultdict(list)
found = set()


def load_words():
    with open('words_dictionary.json') as word_file:
        valid_words = json.load(word_file)
    return valid_words


def dfs(grid, start: tuple, visited=set(), depth=10):
    """
    Searches for words in the grid with max depth of 10
    """
    pass


def populate(grid=None):
    """
    Populates empty grid or returns a new one

    Args:
        None: None

    Returns:
        Randomly generated grid
    """
    if not grid:
        grid = [[None*4] for i in range(4)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = chr(ord('A') + random.randint(0, 25))
    print(grid)
    return grid


def dfs():
    pass


if __name__ == '__main__':
    # demo print
    parser = argparse.ArgumentParser(description="Cheat at wordblitz")
    parser.add_argument('-d', '--depth', type=int,
                        help='depth of the word search. eg. longest word that can be found', default=10)
    parser.add_argument(
        '-s', '--source', help='source of where grid is from, default is pulling from website (you need to have the game open)', choices=['browser'], default='browser')
    parser.add_argument('test', nargs='?', help="testing mode")
    args = parser.parse_args()
    depth = args.depth
    source = args.source
    testing_mode = args.t
    english_words = load_words()
    print('Dict size:',  len(english_words))
    print('depth is', depth)
    print('source is ', source)
    print('testing mode is', testing_mode)
    grid = [[None]*4 for i in range(4)]
    # TODO: populate grid
    # TODO: find the pixel values of each grid value (could be manual)

    print(pyautogui.size())
    print('dant' in english_words)
