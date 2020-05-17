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
from tqdm import tqdm
import cv2
import pytesseract
from pytesseract import Output
import time
from os import path
# from selenium import webdriver
pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/4.0.0_1/bin/tesseract'
ROWS = 4
COLS = 4
english_words = None  # dictionary

grid_to_pix = collections.defaultdict(list)
found = set()


def load_words() -> Dict:
    with open('words_dictionary.json') as word_file:
        valid_words = json.load(word_file)
    return valid_words


def setup(demo=False):
    """
    Takes a screenshot of the current screen, detects where
    the grid and which numbers are in it (in beta)
    """
    # browser = webdriver.Chrome()
    # browser.get('https://www.facebook.com/instantgames/2211386328877300/')
    # time.sleep(2)
    if demo:
        image = cv2.imread('FLrHv.png')
    else:
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    x = np.shape(image)[0]
    img = image[x//3: x - x//8, :np.shape(image)[1]//2, :]  # split in half

    # cv2.imshow('screenshot', img)
    # cv2.waitKey(0)
    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    threshhold = 0
    ret, gray = cv2.threshold(
        gray, threshhold, 255, cv2.THRESH_BINARY)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    # rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))

    # # Appplying dilation on the threshold image
    # dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    # gray = cv2.medianBlur(gray, 3)
    print(np.shape(gray))
    # cv2.imshow('screenshot', gray)
    # cv2.waitKey(0)
    text = pytesseract.image_to_string(gray, config='--psm 6', lang='eng')
    print(text)

    rows = text.split('\n')
    out = []
    for i, r in enumerate(rows):
        chars = []
        for c in r:
            if c == '|':
                chars.append('I')
            if ord(c) >= ord('A') and ord(c) <= ord('Z'):
                chars.append(c)
        if len(chars) == 4:
            out.append(chars)
        else:
            fix = input(
                f'fix the grid by typing the characters separated by a space on row {i} Row was read as {chars}')
            out.append(fix.split(' '))
    if len(out) == 4:
        r = input(
            f'input was read as {np.asarray(out)}, is this fine? \n Enter a row number that you want to change or press enter (0-3)')
        while len(r) != 0:
            fix = input(
                f'fix the grid by typing the characters separated by a space on row {int(r)} or press enter to exit')
            out[int(r)] = fix.split(' ')
            r = input(
                f'input was read as {np.asarray(out)}, is this fine? \n Enter a row number that you want to change or press enter (0-3)')
        return out
    else:
        return False
    img = gray

    d = pytesseract.image_to_data(
        img, output_type=Output.DICT, config='--psm 6', lang='eng')
    n_boxes = len(d['level'])
    print(n_boxes, 'boxes')
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top']
                        [i], d['width'][i], d['height'][i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # cv2.imshow('img', img)
    # cv2.waitKey(0)


def mapping(overwrite=False):
    """generates grid to pixel mapping"""
    global grid_to_pix
    import pickle
    if not path.exists('mapping.pkl') or overwrite:
        print("Generating positions for the board...")
        for i in range(ROWS):
            for j in range(COLS):
                input(
                    f"Move your mouse to center of {i,j}, then press enter when ready to read mouse position")
                grid_to_pix[(i, j)] = tuple(pyautogui.position())
        print('generated', grid_to_pix)
        # json.dump(grid_to_pix, open("mapping.json", 'w'))
        with open('mapping.pkl', 'wb') as handle:
            pickle.dump(grid_to_pix, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        # read from file
        print("Reading binds from file (mapping.pkl)")
        with open('mapping.pkl', 'rb') as handle:
            grid_to_pix = pickle.load(handle)


def draw(coords: List, speed=0.0) -> None:
    # pyautogui.moveTo(0, 0, duration=0.5)
    # pyautogui.moveRel(0, 100, duration=0.5)
    # pyautogui.dragTo(button='left')
    # print(pyautogui.position())
    # pyautogui.write('Hello world')

    # selenium or pyautogui hmm
    # core-letter-cell contains each letters values
    print(cf.orange(
        'Warning: getting ready to draw, do not touch cursor, Move to a corner to exit'))
    time.sleep(1)
    for w, cd in coords:
        off = grid_to_pix[cd[0]]
        print('drawing', w)
        pyautogui.moveTo(off[0], off[1], duration=speed)
        pyautogui.mouseDown()
        for c in cd[1:]:
            off = grid_to_pix[c]
            pyautogui.dragTo(off[0], off[1], button='left',
                             mouseDownUp=False, duration=speed)
        pyautogui.mouseUp()


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
    if b.lower() in english_words and b.lower() not in found:
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


def search(grid, depth=6):
    # print(depth, 'hi')
    for i in tqdm(range(ROWS)):
        for j in range(COLS):
            # print('searching cell', i, j)
            dfs(grid, (i, j), build=[], build_coord=[],
                visited=set(), max_depth=depth)


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
                        help='depth of the word search. eg. longest word that can be found', metavar=6, default=6)
    parser.add_argument(
        '-s', '--source', help='source of where grid is from, default is pulling from website (you need to have the game open)', choices=['browser', 'generated'], default='browser')
    parser.add_argument('-test', help="testing mode",
                        action='store_true')
    args = parser.parse_args()
    depth = args.depth
    source = args.source
    testing_mode = args.test
    english_words = load_words()
    grid = setup()
    binds = mapping()
    cf.use_style('solarized')
    print(cf.bold_yellow(f'Dict size: {len(english_words)}'))
    print('depth is', depth)
    print('source is ', source)
    print('testing mode is', testing_mode)
    if not grid:
        if not testing_mode:
            print(cf.red_bold(
                'Failed to recognize the grid. Try again on a different puzzle'))
            import sys
            sys.exit(1)
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
    if testing_mode:
        print(cf.yellow(f'{words_found}'))
    draw(words_found)  # check privacy settings before drawing
