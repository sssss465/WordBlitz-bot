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
pytesseract==0.3.4
requests==2.23.0
PyAutoGUI==0.9.50
numpy==1.18.1
tqdm==4.46.0
colorful==0.5.4
opencv_python==4.2.0.34
Pillow==7.1.2
```