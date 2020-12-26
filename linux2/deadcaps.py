#!/usr/bin/env python3
#
#   NORMAL (no caps) state.
#     -> CAPSLOCK KEYDOWN, NO event, go to DEADCAPS1 state.
#     -> ANY KEY, send event.
#   DEADCAPS1 state (single key caps activated).
#     -> CAPSLOCK KEYUP, NO event, go to DEADCAPS2 state.
#     -> ANY KEY, send event, and go to NORMAL state.
#   DEADCAPS2 state (single key caps).
#     -> CAPSLOCK KEYDOWN, send event, and go to CAPSLOCK1 state.
#     -> ANY KEY, send event, and go to NORMAL state.
#   CAPSLOCK1 state (multi key caps).
#     -> CAPSLOCK KEYUP, send event, and go to CAPSLOCK2 state.
#     -> ANY KEY, send event.
#   CAPSLOCK2 state (multi key caps).
#     -> CAPSLOCK KEYUP, send event, and go to NORMAL state.
#     -> ANY KEY, send event.


import sys
import libevdev
from libevdev import InputEvent


def debug(msg, e, caps_state):
    print("{}. CAPS_STATE: {}. Event type: {:02x} {} code {:03x} {:12s} value{:1d}".format(msg, caps_state, e.type.value, e.type.name, e.code.value, e.code.name, e.value))   


def deadCapsIt(e, wrap):
    return [InputEvent(wrap, 1), e, InputEvent(wrap, 0), InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)]


# lockKey is true if the key is the lockKey, 
# keydown: KEYDOWN => True, KEYUP => False
def statemachine(state, lockKey, keydown):
    #normal (no lock) state
    if state == 0 :
        if lockKey and keydown :
            return 10
        return 0
    #toggle1 state
    if state == 10 :
        if lockKey and not keydown :
            return 11
        return 0
    #toggle2 state
    if state == 11 :
        if lockKey and keydown :
            return 20
        return 0
    #lock1 state
    if state == 20 :
        if lockKey and not keydown :
            return 21
        return 20
    #lock2 state
    if state == 21 :
        if lockKey and not keydown :
            return 0
        return 21


# NORMAL state
#   KEYDOWN lock, NO event, ACTIVE
#   ALL OTHER KEYDOWN/UP, send event through, NORMAL STATE
# ACTIVE
#   KEYUP lock, NO event, ACTIVE
#   ALL OTHER KEYDOWN/UP, wrap event, NORMAL STATE

# lockKey is true if the key is the lockKey, 
# keydown: KEYDOWN => True, KEYUP => False
def smallStatemachine(state, lockKey, keydown):
    #normal (no lock) state
    if state == 0 :
        if lockKey and keydown :
            return 1
        return 0
    #active state
    if state == 1 :
        if lockKey and not keydown :
            return 1
        return 0


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

    while True:
        for e in d.events():
            
            # ignore non-keypress events
            if e.type.name != 'EV_KEY' :
                uidev.send_events([e])
                continue

            is_caps = e.code.name == 'KEY_CAPSLOCK'
            old_caps_state = caps_state
            caps_state = statemachine(caps_state, is_caps, e.value)
            # a1) if lockkey and new state is 10 or 11, then no event.
            if is_caps and caps_state >= 10 and caps_state <= 11 :
                continue
            # b1) if old state is 10 or 11 and new state is 0, then deadcaps around event.
            elif caps_state == 0 and old_caps_state >= 10 and old_caps_state <= 11 :
                uidev.send_events(deadCapsIt(e, libevdev.EV_KEY.KEY_LEFTSHIFT))
                continue
                
            is_pinky = e.code.name == 'KEY_SEMICOLON'
            old_pinky_state = pinky_state
            pinky_state = smallStatemachine(pinky_state, is_pinky, e.value)
            # a2) pinkystate is being set to active, then don't send the key event
            if pinky_state == 1 :
                continue
            # b2) if old state is 10 or 11 and new state is 0, then deadcaps around event.
            elif pinky_state == 0 and old_pinky_state == 1 :
                uidev.send_events(deadCapsIt(e, libevdev.EV_KEY.KEY_RIGHTALT))
                continue
            
            # c) else, then pass the event as is.
            uidev.send_events([e])

                
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} /dev/input/eventX".format(sys.argv[0]))
        print("   press once on caps lock, and it will work only for one character. press twice in a row, and it will stick.")
        sys.exit(1)
    main(sys.argv)
