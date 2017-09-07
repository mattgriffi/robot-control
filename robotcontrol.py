# ECE102 project
# Due 9/29/2016
# Program to convert keyboard input to mouse input to
# remote control a LEGO robot through the NXT software.
# Keyboard input will come from an Xinput controller
# converted to keyboard input through antimicro.
#
# This whole thing is a hacky mess...
# Good thing this isn't for a computer science class

import copy
import win32api
import pyautogui
import pyperclip
import time

pyautogui.PAUSE = 0

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
current_engine = 'A'
CHECK = 830, 421
FORWARD = 770, 390
BACK = 814, 390
currently_forward = True
ACTION_POWER_TXT_BOX = 828, 361
TURRET = 420, 444
MOVEMENT = 420, 460

# Track controller input
buttons_pressed = {
    'l_stick_up':False,
    'l_stick_left':False,
    'l_stick_down':False,
    'l_stick_right':False,
    'left':False,
    'right':False,
    'a':False,
    'b':False,
    'x':False,
    'y':False,
    'r_shoulder':False,
    'start':False
}
# Track input being sent to NXT
buttons_currently_down = copy.deepcopy(buttons_pressed)

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


def main() -> None:
    while True:
        # print(str(pyautogui.position()))
        check_for_key_presses()
        send_input()


def send_input():
    
    if buttons_pressed['l_stick_down'] and not buttons_currently_down['l_stick_down'] and not True in buttons_currently_down.values():
        pyautogui.mouseDown(DOWN_BUTTON)
        buttons_currently_down['l_stick_down'] = True
    elif buttons_currently_down['l_stick_down'] and not buttons_pressed['l_stick_down']:
        pyautogui.mouseUp(DOWN_BUTTON)
        buttons_currently_down['l_stick_down'] = False

    if buttons_pressed['l_stick_up'] and not buttons_currently_down['l_stick_up'] and not True in buttons_currently_down.values():
        pyautogui.mouseDown(UP_BUTTON)
        buttons_currently_down['l_stick_up'] = True
    elif buttons_currently_down['l_stick_up'] and not buttons_pressed['l_stick_up']:
        pyautogui.mouseUp(UP_BUTTON)
        buttons_currently_down['l_stick_up'] = False

    if buttons_pressed['l_stick_left'] and not buttons_currently_down['l_stick_left'] and not True in buttons_currently_down.values():
        pyautogui.mouseDown(LEFT_BUTTON)
        buttons_currently_down['l_stick_left'] = True
    elif buttons_currently_down['l_stick_left'] and not buttons_pressed['l_stick_left']:
        pyautogui.mouseUp(LEFT_BUTTON)
        buttons_currently_down['l_stick_left'] = False
    
    if buttons_pressed['l_stick_right'] and not buttons_currently_down['l_stick_right'] and not True in buttons_currently_down.values():
        pyautogui.mouseDown(RIGHT_BUTTON)
        buttons_currently_down['l_stick_right'] = True
    elif buttons_currently_down['l_stick_right'] and not buttons_pressed['l_stick_right']:
        pyautogui.mouseUp(RIGHT_BUTTON)
        buttons_currently_down['l_stick_right'] = False

    if buttons_pressed['a'] and not buttons_currently_down['a'] and not True in buttons_currently_down.values():
        pyautogui.mouseDown(ACTION)
        buttons_currently_down['a'] = True
    elif buttons_currently_down['a'] and not buttons_pressed['a']:
        pyautogui.mouseUp(ACTION)
        buttons_currently_down['a'] = False

    if buttons_pressed['x'] and not buttons_currently_down['x'] and not True in buttons_currently_down.values():
        switch_motor('A')
        buttons_currently_down['x'] = True
    elif buttons_currently_down['x'] and not buttons_pressed['x']:
        buttons_currently_down['x'] = False
        
    if buttons_pressed['y'] and not buttons_currently_down['y'] and not True in buttons_currently_down.values():
        switch_motor('B')
        buttons_currently_down['y'] = True
    elif buttons_currently_down['y'] and not buttons_pressed['y']:
        buttons_currently_down['y'] = False
        
    if buttons_pressed['b'] and not buttons_currently_down['b'] and not True in buttons_currently_down.values():
        switch_motor('C')
        buttons_currently_down['b'] = True
    elif buttons_currently_down['b'] and not buttons_pressed['b']:
        buttons_currently_down['b'] = False
        
    if buttons_pressed['r_shoulder'] and not buttons_currently_down['r_shoulder'] and not True in buttons_currently_down.values():
        swap_direction()
        buttons_currently_down['r_shoulder'] = True
    elif buttons_currently_down['r_shoulder'] and not buttons_pressed['r_shoulder']:
        buttons_currently_down['r_shoulder'] = False
        
    if buttons_pressed['left'] and not buttons_currently_down['left'] and not True in buttons_currently_down.values():
        adjust_active_speed('down')
        buttons_currently_down['left'] = True
    elif buttons_currently_down['left'] and not buttons_pressed['left']:
        buttons_currently_down['left'] = False
        
    if buttons_pressed['right'] and not buttons_currently_down['right'] and not True in buttons_currently_down.values():
        adjust_active_speed('up')
        buttons_currently_down['right'] = True
    elif buttons_currently_down['right'] and not buttons_pressed['right']:
        buttons_currently_down['right'] = False
        
    if buttons_pressed['start'] and not buttons_currently_down['start'] and not True in buttons_currently_down.values():
        swap_NXT()
        buttons_currently_down['start'] = True
    elif buttons_currently_down['start'] and not buttons_pressed['start']:
        buttons_currently_down['start'] = False


def swap_NXT():
    global current_NXT
    start_time = time.time()
    pyautogui.click(CONNECTIONS)
    time.sleep(0.1)
    pyautogui.click(CONNECTIONS)
    time.sleep(0.1)
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
    while not pyautogui.pixelMatchesColor(700, 550, (239, 240, 231)):
        time.sleep(0.1)
        pyautogui.click(CONNECTIONS_CLOSE)

    print('Time taken to switch NXT: ', str(time.time() - start_time))


def adjust_active_speed(direction: str):
    pyautogui.click(CONFIGURE)
    time.sleep(0.1)
    pyautogui.click(CONFIGURE)
    time.sleep(0.05)
    pyautogui.doubleClick(ACTION_POWER_TXT_BOX)
    time.sleep(0.1)
    pyautogui.keyDown('ctrl')
    time.sleep(0.01)
    pyautogui.keyDown('c')
    time.sleep(0.01)
    pyautogui.keyUp('c')
    time.sleep(0.01)
    pyautogui.keyUp('ctrl')
    current_speed = int(pyperclip.paste())
    if direction == 'up':
        current_speed += 25
    elif direction == 'down':
        current_speed -= 25
    print('New speed: ', str(current_speed))
    pyperclip.copy(str(current_speed))
    time.sleep(0.05)
    pyautogui.keyDown('ctrl')
    time.sleep(0.01)
    pyautogui.keyDown('v')
    time.sleep(0.01)
    pyautogui.keyUp('v')
    time.sleep(0.01)
    pyautogui.keyUp('ctrl')
    time.sleep(0.1)
    pyautogui.click(CHECK)


def swap_direction():
    global currently_forward
    pyautogui.click(CONFIGURE)
    time.sleep(0.1)
    pyautogui.click(CONFIGURE)
    time.sleep(0.1)
    if currently_forward:
        pyautogui.click(BACK)
        currently_forward = False
    else:
        pyautogui.click(FORWARD)
        currently_forward = True
    time.sleep(0.1)
    pyautogui.click(CHECK)


def switch_motor(engine_letter):
    global current_engine

    pyautogui.click(CONFIGURE)
    time.sleep(0.1)
    pyautogui.click(CONFIGURE)
    time.sleep(0.1)
    pyautogui.click(DROP_DOWN)
    time.sleep(0.5)
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
    time.sleep(0.05)
    pyautogui.click(CHECK)
    time.sleep(0.05)
    pyautogui.click(CHECK)


def check_for_key_presses() -> None:
    
    if win32api.GetKeyState(L_STICK_UP) < 0:
        buttons_pressed['l_stick_up'] = True
    else:
        buttons_pressed['l_stick_up'] = False

    if win32api.GetKeyState(L_STICK_DOWN) < 0:
        buttons_pressed['l_stick_down'] = True
    else:
        buttons_pressed['l_stick_down'] = False
    
    if win32api.GetKeyState(L_STICK_LEFT) < 0:
        buttons_pressed['l_stick_left'] = True
    else:
        buttons_pressed['l_stick_left'] = False
    
    if win32api.GetKeyState(L_STICK_RIGHT) < 0:
        buttons_pressed['l_stick_right'] = True
    else:
        buttons_pressed['l_stick_right'] = False

    if win32api.GetKeyState(A) < 0:
        buttons_pressed['a'] = True
    else:
        buttons_pressed['a'] = False

    if win32api.GetKeyState(B) < 0:
        buttons_pressed['b'] = True
    else:
        buttons_pressed['b'] = False

    if win32api.GetKeyState(X) < 0:
        buttons_pressed['x'] = True
    else:
        buttons_pressed['x'] = False

    if win32api.GetKeyState(Y) < 0:
        buttons_pressed['y'] = True
    else:
        buttons_pressed['y'] = False

    if win32api.GetKeyState(R_SHOULDER) < 0:
        buttons_pressed['r_shoulder'] = True
    else:
        buttons_pressed['r_shoulder'] = False

    if win32api.GetKeyState(START) < 0:
        buttons_pressed['start'] = True
    else:
        buttons_pressed['start'] = False

    if win32api.GetKeyState(LEFT) < 0:
        buttons_pressed['left'] = True
    else:
        buttons_pressed['left'] = False

    if win32api.GetKeyState(RIGHT) < 0:
        buttons_pressed['right'] = True
    else:
        buttons_pressed['right'] = False


if __name__ == '__main__':
    main()
