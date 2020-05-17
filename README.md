## Wordblitz bot

usage: `./wordblitz.py [-h] [-d 6] [-s {browser,generated}] [-test] [-ov]`

Cheat at wordblitz

optional arguments:
  -h, --help            show this help message and exit
  -d 6, --depth 6       depth of the word search. eg. longest word that can be
                        found
  -s {browser,generated}, --source {browser,generated}
                        source of where grid is from, default is pulling from
                        website (you need to have the game open)
  -test                 testing mode
  -ov                   override pixel locations)

Important: tile the game so it is on the left side of the screen and make sure it is in full screen with as little text in the background as possible. start the script as the game starts. The first time running it will build the mappings for the mouse movements

### Requirements

```python
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
import time
```