#!/usr/bin/env python3
# CAPS (auto revert after one other keydown or CAPS to CAPSLOCK)
# CAPSLOCK (turn off when CAPS) (this is done by the system).
# SEMI (auto revert after one other keydown)
# LESSLOCK (turn off when space or LESS)


import sys
import libevdev
from libevdev import InputEvent


def debug(msg, e, caps_state):
    print("{}. CAPS_STATE: {}. Event type: {:02x} {} code {:03x} {:12s} value{:1d}".format(msg, caps_state, e.type.value, e.type.name, e.code.value, e.code.name, e.value))


def wrapModifierKeys(list, ctrl, shift, alt):
    if shift:
        list.insert(0, InputEvent(libevdev.EV_KEY.KEY_LEFTSHIFT,1))
        list.append(InputEvent(libevdev.EV_KEY.KEY_LEFTSHIFT,0))
    if alt:
        list.insert(0, InputEvent(libevdev.EV_KEY.KEY_RIGHTALT,1))
        list.append(InputEvent(libevdev.EV_KEY.KEY_RIGHTALT,0))
    if ctrl:
        list.insert(0, InputEvent(libevdev.EV_KEY.KEY_LEFTCTRL,1))
        list.append(InputEvent(libevdev.EV_KEY.KEY_LEFTCTRL,0))
    return list

def deadCapsIt(e, shift, alt):
    list = wrapModifierKeys([e], False, shift, alt)
    list.append(InputEvent(libevdev.EV_SYN.SYN_REPORT,0))
    return list

arrows = {
    'KEY_A': libevdev.EV_KEY.KEY_UP,
    'KEY_S': libevdev.EV_KEY.KEY_DOWN,
    'KEY_D': libevdev.EV_KEY.KEY_LEFT,
    'KEY_F': libevdev.EV_KEY.KEY_RIGHT,
    'KEY_Z': libevdev.EV_KEY.KEY_Z,
    'KEY_X': libevdev.EV_KEY.KEY_X,
    'KEY_C': libevdev.EV_KEY.KEY_C,
    'KEY_V': libevdev.EV_KEY.KEY_V,
    'KEY_B': libevdev.EV_KEY.KEY_A,
    'KEY_E': libevdev.EV_KEY.KEY_BACKSPACE,
    'KEY_R': libevdev.EV_KEY.KEY_DELETE
}
homePageArrows = {
    'KEY_A': libevdev.EV_KEY.KEY_PAGEUP,
    'KEY_S': libevdev.EV_KEY.KEY_PAGEDOWN,
    'KEY_D': libevdev.EV_KEY.KEY_HOME,
    'KEY_F': libevdev.EV_KEY.KEY_END,
}

def deadlessKey(key, homePageMode):
    if homePageMode and key in homePageArrows:
        return homePageArrows[key]
    if key in arrows:
        return arrows[key]
    return False 
    
def deadlessIt(key, ctrl, shift):
    list = wrapModifierKeys([InputEvent(key, 1)], ctrl, shift, False)
    list.append(InputEvent(key,0))
    list.append(InputEvent(libevdev.EV_SYN.SYN_REPORT,0))
    return list

def main(args):
    path = args[1]
    caps_state = 0
    pinky_state = 0

    fd = open(path, 'rb')
    d = libevdev.Device(fd)
    d.grab()

    # create a duplicate of our input device
    caps = libevdev.evbit('KEY_CAPSLOCK')
    d.enable(caps)  # make sure the code we map to is available
    uidev = d.create_uinput_device()
    print('Device is at {}'.format(uidev.devnode))

    state = 'NORMAL'   #NORMAL/DEADCAPS/CAPSLOCK/SEMIDEAD/DEADLESS
    lessJ = False
    lessK = False
    lessL = False

    while True:
        for e in d.events():

            # debug('keyboard: ', e, state) 

            # ignore non-keypress events
            if e.type.name != 'EV_KEY' :
                uidev.send_events([e])
                continue

            # debug('keydown/keyup: ', e, state) 

            key = e.code.name
            ## keyup handlers
            if not e.value:
                # handling JKL modifier keys in navigation mode
                if state == 'DEADLESS':
                    if key == 'KEY_J':
                        lessJ = False
                    elif key == 'KEY_K':
                        lessK = False
                    elif key == 'KEY_L':
                        lessL = False
                    continue

                uidev.send_events([e])
                continue

            # debug('keydown: ', e, state)

            ## keydown handlers
            #default state. intercept deadkeys, otherwise do nothing.
            if state == 'NORMAL':
                if key == 'KEY_CAPSLOCK':
                    state = 'DEADCAPS'
                elif key == 'KEY_SEMICOLON':
                    state = 'SEMIDEAD'
                elif key == 'KEY_102ND':          # < less than key
                    state = 'DEADLESS'
                else:
                    uidev.send_events([e])
                continue

            if state == 'CAPSLOCK':
                if key == 'KEY_CAPSLOCK':
                    state = 'NORMAL'
                uidev.send_events([e])
                continue

            if state == 'DEADCAPS':
                if key == 'KEY_CAPSLOCK':
                    state = 'CAPSLOCK'
                    uidev.send_events([e])
                else :
                    state = 'NORMAL'
                    uidev.send_events(deadCapsIt(e, True, False))
                continue
            
            if key == 'KEY_CAPSLOCK':       # caps key doesnt work in semidead or deadless state
                continue
            
            if state == 'SEMIDEAD':
                state = 'NORMAL'
                uidev.send_events(deadCapsIt(e, False, True))
                continue
            
            if state == 'DEADLESS':
                if key == 'KEY_102ND' or key == 'KEY_SPACE':
                    state = 'NORMAL'
                elif key == 'KEY_J':
                    lessJ = True
                elif key == 'KEY_K':
                    lessK = True
                elif key == 'KEY_L':
                    lessL = True
                else:
                    key = deadlessKey(key, lessL)
                    if key:
                        uidev.send_events(deadlessIt(key, lessJ, lessK))
                continue

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} /dev/input/eventX".format(sys.argv[0]))
        print("   press once on caps lock, and it will work only for one character. press twice in a row, and it will stick.")
        sys.exit(1)
    main(sys.argv)
