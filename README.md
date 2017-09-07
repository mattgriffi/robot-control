# Lego Robot Remote Control

This program was used for a group project in my engineering class. Our assignment was to use the Lego Mindstorm software (which has a drag-and-drop code block interface) to program a Lego robot to do something interesting. That wasn't good enough for me. Instead, I wrote a Python script that would allow my team to remotely control the robot via Bluetooth using an Xbox controller.

This program listens for certain keyboard key presses. To use it with an Xinput controller, you will need a program to convert Xinput to key presses. I used [antimicro](https://github.com/AntiMicro/antimicro).

## Usage

To use this program, simply run it like any other Python program:

```sh
python robotcontrol.py
```

In order to actually use this program, you will need a Lego Mindstorm robot and the NXT software, which can be found [here](https://www.lego.com/en-us/mindstorms/downloads). The NXT software should be fullscreen, with the remote control interface open in the default position. Please note that this program was only tested on a 1920x1080 screen, and it may not function on other resolutions.

The program will run in the background until killed, and will constantly listen for key presses. Pressing certain keys will cause it to move the mouse and click on the corresponding parts of the remote control UI.

## Installation

This program requires Python 3.5 or newer.

The required 3rd party modules are listed in requirements.txt and can be batch installed with the following command:

```sh
pip install -r requirements.txt
```

This program uses the win32api to retrieve key press information, which means that it will only work on Windows (and was only tested on Windows 10).
