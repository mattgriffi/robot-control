# ECE102 project
# Due 9/29/2016
# Program to convert keyboard input to mouse input in order to
# remote control a LEGO robot through the NXT software. Keyboard input will come from an
# Xinput controller converted to keyboard input through antimicro.


import copy
import win32api
import pyautogui
import pyperclip
import time

pyautogui.PAUSE = 0

# Button coordinates in the remote control UI
UP_BUTTON = 637, 294
DOWN_BUTTON = 637, 350
LEFT_BUTTON = 581, 350
RIGHT_BUTTON = 693, 350
ACTION = 637, 404
CONNECTIONS = 631, 491
CONFIGURE = 807, 467
SPEED_UP = 823, 309
SPEED_DOWN = 823, 396
CONNECT = 300, 575
CONNECTIONS_CLOSE = 734, 574
DROP_DOWN = 826, 290
ENGINE_SLOT_1 = 825, 265
ENGINE_SLOT_2 = 825, 276
ENGINE_SLOT_3 = 825, 288
ENGINE_SLOT_4 = 825, 301
ENGINE_SLOT_5 = 825, 314
FORWARD = 770, 390
BACK = 814, 390
CHECK = 830, 421

# Misc UI coordinates
ACTION_POWER_TXT_BOX = 828, 361
TURRET = 420, 444
MOVEMENT = 420, 460

currently_forward = True
current_engine = 'A'

# Track controller input
buttons_pressed = {
    'l_stick_up': False,
    'l_stick_left': False,
    'l_stick_down': False,
    'l_stick_right': False,
    'left': False,
    'right': False,
    'a': False,
    'b': False,
    'x': False,
    'y': False,
    'r_shoulder': False,
    'start': False
}
buttons_currently_down = copy.deepcopy(buttons_pressed)

# These are the keys that will be listened for
# Keys must all be alphabetic
L_STICK_UP = 82  # R
L_STICK_LEFT = 71  # G
L_STICK_DOWN = 66  # B
L_STICK_RIGHT = 78  # N
LEFT = 75  # K
RIGHT = 76  # L
A = 79  # O
B = 80  # P
X = 74  # J
Y = 77  # M
R_SHOULDER = 85  # U
START = 73  # I

current_NXT = 1


def main():
    while True:
        check_for_key_presses()
        send_input()


def send_input():
    if buttons_pressed['l_stick_down'] and not buttons_currently_down['l_stick_down'] \
            and True not in buttons_currently_down.values():
        pyautogui.mouseDown(DOWN_BUTTON)
        buttons_currently_down['l_stick_down'] = True
    elif buttons_currently_down['l_stick_down'] and not buttons_pressed['l_stick_down']:
        pyautogui.mouseUp(DOWN_BUTTON)
        buttons_currently_down['l_stick_down'] = False

    if buttons_pressed['l_stick_up'] and not buttons_currently_down['l_stick_up'] \
            and True not in buttons_currently_down.values():
        pyautogui.mouseDown(UP_BUTTON)
        buttons_currently_down['l_stick_up'] = True
    elif buttons_currently_down['l_stick_up'] and not buttons_pressed['l_stick_up']:
        pyautogui.mouseUp(UP_BUTTON)
        buttons_currently_down['l_stick_up'] = False

    if buttons_pressed['l_stick_left'] and not buttons_currently_down['l_stick_left'] \
            and True not in buttons_currently_down.values():
        pyautogui.mouseDown(LEFT_BUTTON)
        buttons_currently_down['l_stick_left'] = True
    elif buttons_currently_down['l_stick_left'] and not buttons_pressed['l_stick_left']:
        pyautogui.mouseUp(LEFT_BUTTON)
        buttons_currently_down['l_stick_left'] = False

    if buttons_pressed['l_stick_right'] and not buttons_currently_down['l_stick_right'] \
            and True not in buttons_currently_down.values():
        pyautogui.mouseDown(RIGHT_BUTTON)
        buttons_currently_down['l_stick_right'] = True
    elif buttons_currently_down['l_stick_right'] and not buttons_pressed['l_stick_right']:
        pyautogui.mouseUp(RIGHT_BUTTON)
        buttons_currently_down['l_stick_right'] = False

    if buttons_pressed['a'] and not buttons_currently_down['a'] \
            and True not in buttons_currently_down.values():
        pyautogui.mouseDown(ACTION)
        buttons_currently_down['a'] = True
    elif buttons_currently_down['a'] and not buttons_pressed['a']:
        pyautogui.mouseUp(ACTION)
        buttons_currently_down['a'] = False

    if buttons_pressed['x'] and not buttons_currently_down['x'] \
            and True not in buttons_currently_down.values():
        switch_motor('A')
        buttons_currently_down['x'] = True
    elif buttons_currently_down['x'] and not buttons_pressed['x']:
        buttons_currently_down['x'] = False

    if buttons_pressed['y'] and not buttons_currently_down['y'] \
            and True not in buttons_currently_down.values():
        switch_motor('B')
        buttons_currently_down['y'] = True
    elif buttons_currently_down['y'] and not buttons_pressed['y']:
        buttons_currently_down['y'] = False

    if buttons_pressed['b'] and not buttons_currently_down['b'] \
            and True not in buttons_currently_down.values():
        switch_motor('C')
        buttons_currently_down['b'] = True
    elif buttons_currently_down['b'] and not buttons_pressed['b']:
        buttons_currently_down['b'] = False

    if buttons_pressed['r_shoulder'] and not buttons_currently_down['r_shoulder'] \
            and True not in buttons_currently_down.values():
        swap_direction()
        buttons_currently_down['r_shoulder'] = True
    elif buttons_currently_down['r_shoulder'] and not buttons_pressed['r_shoulder']:
        buttons_currently_down['r_shoulder'] = False

    if buttons_pressed['left'] and not buttons_currently_down['left'] \
            and True not in buttons_currently_down.values():
        adjust_active_speed('down')
        buttons_currently_down['left'] = True
    elif buttons_currently_down['left'] and not buttons_pressed['left']:
        buttons_currently_down['left'] = False

    if buttons_pressed['right'] and not buttons_currently_down['right'] \
            and True not in buttons_currently_down.values():
        adjust_active_speed('up')
        buttons_currently_down['right'] = True
    elif buttons_currently_down['right'] and not buttons_pressed['right']:
        buttons_currently_down['right'] = False

    if buttons_pressed['start'] and not buttons_currently_down['start'] \
            and True not in buttons_currently_down.values():
        swap_NXT()
        buttons_currently_down['start'] = True
    elif buttons_currently_down['start'] and not buttons_pressed['start']:
        buttons_currently_down['start'] = False


def swap_NXT():
    global current_NXT

    # The native remote control interface can only connect to one NXT at a time, and each
    # NXT can only control 3 motors, which isn't enough for our robot. This method will swap
    # the bluetooth connection between the two NXTs required to control all of our motors
    # Unfortunately, the Lego software can take upwards of 30 seconds to make the switch
    start_time = time.time()
    open_connections()

    # Wait for the connections screen to open, which can take a few seconds
    while not (pyautogui.pixelMatchesColor(396, 443, (254, 168, 62)) or
               pyautogui.pixelMatchesColor(396, 458, (254, 168, 62))):
        time.sleep(0.1)

    if current_NXT == 1:
        pyautogui.click(MOVEMENT)
        time.sleep(0.1)
        pyautogui.click(CONNECT)
        current_NXT = 2
    else:
        pyautogui.click(TURRET)
        time.sleep(0.1)
        pyautogui.click(CONNECT)
        current_NXT = 1

    # Wait for the connection to complete so the connection screen can be closed
    # This can take up to 30 seconds
    while not pyautogui.pixelMatchesColor(700, 550, (239, 240, 231)):
        time.sleep(0.1)
        pyautogui.click(CONNECTIONS_CLOSE)

    print('Time taken to switch NXT: ', str(time.time() - start_time))


def adjust_active_speed(direction: str):

    open_config()

    pyautogui.doubleClick(ACTION_POWER_TXT_BOX)
    time.sleep(0.1)
    ctrl_c()

    current_speed = int(pyperclip.paste())
    if direction == 'up':
        current_speed += 25
    elif direction == 'down':
        current_speed -= 25
    print('New speed: ', str(current_speed))
    pyperclip.copy(str(current_speed))
    time.sleep(0.05)

    ctrl_v()

    pyautogui.click(CHECK)


def swap_direction():
    global currently_forward

    open_config()

    if currently_forward:
        pyautogui.click(BACK)
        currently_forward = False
    else:
        pyautogui.click(FORWARD)
        currently_forward = True

    click_check_button()


def switch_motor(engine_letter):
    global current_engine

    open_config()

    # Click the engine change drop down
    pyautogui.click(DROP_DOWN)
    time.sleep(0.5)

    # The position of each drop down option on the screen changes depending on which
    # engine is currently selected
    if engine_letter == 'A':
        if current_engine == 'A':
            pyautogui.click(ENGINE_SLOT_3)
        elif current_engine == 'B':
            pyautogui.click(ENGINE_SLOT_2)
        elif current_engine == 'C':
            pyautogui.click(ENGINE_SLOT_1)
        current_engine = 'A'

    elif engine_letter == 'B':
        if current_engine == 'A':
            pyautogui.click(ENGINE_SLOT_4)
        elif current_engine == 'B':
            pyautogui.click(ENGINE_SLOT_3)
        elif current_engine == 'C':
            pyautogui.click(ENGINE_SLOT_2)
        current_engine = 'B'

    elif engine_letter == 'C':
        if current_engine == 'A':
            pyautogui.click(ENGINE_SLOT_5)
        elif current_engine == 'B':
            pyautogui.click(ENGINE_SLOT_4)
        elif current_engine == 'C':
            pyautogui.click(ENGINE_SLOT_3)
        current_engine = 'C'

    click_check_button()
    click_check_button()


def check_for_key_presses():

    # GetKeyState will return a negative number if the key is currently pressed, or a
    # positive number if it is not
    buttons_pressed['l_stick_up'] = win32api.GetKeyState(L_STICK_UP) < 0
    buttons_pressed['l_stick_down'] = win32api.GetKeyState(L_STICK_DOWN) < 0
    buttons_pressed['l_stick_left'] = win32api.GetKeyState(L_STICK_LEFT) < 0
    buttons_pressed['l_stick_right'] = win32api.GetKeyState(L_STICK_RIGHT) < 0
    buttons_pressed['a'] = win32api.GetKeyState(A) < 0
    buttons_pressed['b'] = win32api.GetKeyState(B) < 0
    buttons_pressed['x'] = win32api.GetKeyState(X) < 0
    buttons_pressed['y'] = win32api.GetKeyState(Y) < 0
    buttons_pressed['r_shoulder'] = win32api.GetKeyState(R_SHOULDER) < 0
    buttons_pressed['start'] = win32api.GetKeyState(START) < 0
    buttons_pressed['left'] = win32api.GetKeyState(LEFT) < 0
    buttons_pressed['right'] = win32api.GetKeyState(RIGHT) < 0


def ctrl_v():
    pyautogui.keyDown('ctrl')
    time.sleep(0.01)
    pyautogui.keyDown('v')
    time.sleep(0.01)
    pyautogui.keyUp('v')
    time.sleep(0.01)
    pyautogui.keyUp('ctrl')
    time.sleep(0.1)


def ctrl_c():
    pyautogui.keyDown('ctrl')
    time.sleep(0.01)
    pyautogui.keyDown('c')
    time.sleep(0.01)
    pyautogui.keyUp('c')
    time.sleep(0.01)
    pyautogui.keyUp('ctrl')


def open_config():
    # Attempt to click it twice, since it sometimes doesn't work
    pyautogui.click(CONFIGURE)
    time.sleep(0.1)
    pyautogui.click(CONFIGURE)
    time.sleep(0.1)


def open_connections():

    # Do it twice, since it sometimes doesn't work
    pyautogui.click(CONNECTIONS)
    time.sleep(0.1)
    pyautogui.click(CONNECTIONS)
    time.sleep(0.1)


def click_check_button():
    # This is used to close out of config menus
    time.sleep(0.1)
    pyautogui.click(CHECK)


if __name__ == '__main__':
    main()
