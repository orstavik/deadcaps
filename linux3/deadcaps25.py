#!/usr/bin/env python3
# CAPS (auto revert after one other keydown or CAPS to CAPSLOCK)
# CAPSLOCK (turn off when CAPS) (this is done by the system).
# SEMI (auto revert after one other keydown)
# LESSLOCK (turn off when space or LESS)


import time
import os
import sys
import libevdev
import fcntl
from libevdev import InputEvent


shift1 = InputEvent(libevdev.EV_KEY.KEY_LEFTSHIFT,1)
shift0 = InputEvent(libevdev.EV_KEY.KEY_LEFTSHIFT,0)
shift_msc = InputEvent(libevdev.EV_MSC.MSC_SCAN, 0x700e1) #left shift

ralt1 = InputEvent(libevdev.EV_KEY.KEY_RIGHTALT,1)
ralt0 = InputEvent(libevdev.EV_KEY.KEY_RIGHTALT,0)
ctrl1 = InputEvent(libevdev.EV_KEY.KEY_LEFTCTRL,1)
ctrl0 = InputEvent(libevdev.EV_KEY.KEY_LEFTCTRL,0)
space1 = InputEvent(libevdev.EV_KEY.KEY_SPACE,1)
space0 = InputEvent(libevdev.EV_KEY.KEY_SPACE,0)

msc = InputEvent(libevdev.EV_MSC.MSC_SCAN,458792)
syn0 = InputEvent(libevdev.EV_SYN.SYN_REPORT,0)

minus1 = InputEvent(libevdev.EV_KEY.KEY_MINUS,1)
minus0 = InputEvent(libevdev.EV_KEY.KEY_MINUS,0)
rbrace1 = InputEvent(libevdev.EV_KEY.KEY_RIGHTBRACE,1)
rbrace0 = InputEvent(libevdev.EV_KEY.KEY_RIGHTBRACE,0)
one1 = InputEvent(libevdev.EV_KEY.KEY_1,1)
one0 = InputEvent(libevdev.EV_KEY.KEY_1,0)
two1 = InputEvent(libevdev.EV_KEY.KEY_2,1)
two0 = InputEvent(libevdev.EV_KEY.KEY_2,0)
three1 = InputEvent(libevdev.EV_KEY.KEY_3,1)
three0 = InputEvent(libevdev.EV_KEY.KEY_3,0)
four1 = InputEvent(libevdev.EV_KEY.KEY_4,1)
four0 = InputEvent(libevdev.EV_KEY.KEY_4,0)
five1 = InputEvent(libevdev.EV_KEY.KEY_5,1)
five0 = InputEvent(libevdev.EV_KEY.KEY_5,0)
six1 = InputEvent(libevdev.EV_KEY.KEY_6,1)
six0 = InputEvent(libevdev.EV_KEY.KEY_6,0)
seven1 = InputEvent(libevdev.EV_KEY.KEY_7,1)
seven0 = InputEvent(libevdev.EV_KEY.KEY_7,0)
eight1 = InputEvent(libevdev.EV_KEY.KEY_8,1)
eight0 = InputEvent(libevdev.EV_KEY.KEY_8,0)
nine1 = InputEvent(libevdev.EV_KEY.KEY_9,1)
nine0 = InputEvent(libevdev.EV_KEY.KEY_9,0)
zero1 = InputEvent(libevdev.EV_KEY.KEY_0,1)
zero0 = InputEvent(libevdev.EV_KEY.KEY_0,0)
less1 = InputEvent(libevdev.EV_KEY.KEY_102ND,1)
less0 = InputEvent(libevdev.EV_KEY.KEY_102ND,0)
bslash1 = InputEvent(libevdev.EV_KEY.KEY_BACKSLASH,1)
bslash0 = InputEvent(libevdev.EV_KEY.KEY_BACKSLASH,0)
grave1 = InputEvent(libevdev.EV_KEY.KEY_GRAVE,1)
grave0 = InputEvent(libevdev.EV_KEY.KEY_GRAVE,0)
equal1 = InputEvent(libevdev.EV_KEY.KEY_EQUAL,1)
equal0 = InputEvent(libevdev.EV_KEY.KEY_EQUAL,0)
semi1 = InputEvent(libevdev.EV_KEY.KEY_SEMICOLON,1)
semi0 = InputEvent(libevdev.EV_KEY.KEY_SEMICOLON,0)

up1 = InputEvent(libevdev.EV_KEY.KEY_UP,1)
up0 = InputEvent(libevdev.EV_KEY.KEY_UP,0)
down1 = InputEvent(libevdev.EV_KEY.KEY_DOWN,1)
down0 = InputEvent(libevdev.EV_KEY.KEY_DOWN,0)
left1 = InputEvent(libevdev.EV_KEY.KEY_LEFT,1)
left0 = InputEvent(libevdev.EV_KEY.KEY_LEFT,0)
right1 = InputEvent(libevdev.EV_KEY.KEY_RIGHT,1)
right0 = InputEvent(libevdev.EV_KEY.KEY_RIGHT,0)
z1 = InputEvent(libevdev.EV_KEY.KEY_Z,1)
z0 = InputEvent(libevdev.EV_KEY.KEY_Z,0)
x1 = InputEvent(libevdev.EV_KEY.KEY_X,1)
x0 = InputEvent(libevdev.EV_KEY.KEY_X,0)
c1 = InputEvent(libevdev.EV_KEY.KEY_C,1)
c0 = InputEvent(libevdev.EV_KEY.KEY_C,0)
v1 = InputEvent(libevdev.EV_KEY.KEY_V,1)
v0 = InputEvent(libevdev.EV_KEY.KEY_V,0)
a1 = InputEvent(libevdev.EV_KEY.KEY_A,1)
a0 = InputEvent(libevdev.EV_KEY.KEY_A,0)
back1 = InputEvent(libevdev.EV_KEY.KEY_BACKSPACE,1)
back0 = InputEvent(libevdev.EV_KEY.KEY_BACKSPACE,0)
del1 = InputEvent(libevdev.EV_KEY.KEY_DELETE,1)
del0 = InputEvent(libevdev.EV_KEY.KEY_DELETE,0)
pageup1 = InputEvent(libevdev.EV_KEY.KEY_PAGEUP,1)
pageup0 = InputEvent(libevdev.EV_KEY.KEY_PAGEUP,0)
pagedown1 = InputEvent(libevdev.EV_KEY.KEY_PAGEDOWN,1)
pagedown0 = InputEvent(libevdev.EV_KEY.KEY_PAGEDOWN,0)
home1 = InputEvent(libevdev.EV_KEY.KEY_HOME,1)
home0 = InputEvent(libevdev.EV_KEY.KEY_HOME,0)
end1 = InputEvent(libevdev.EV_KEY.KEY_END,1)
end0 = InputEvent(libevdev.EV_KEY.KEY_END,0)
enter1= InputEvent(libevdev.EV_KEY.KEY_ENTER,1)

semidead = {
    'KEY_Q': [shift1, 'sleep', minus1, minus0, shift0],
    'KEY_W': [ralt1, 'sleep', rbrace1, rbrace0, ralt0, 'sleep', space1, space0],
#    'KEY_W': syn(rightAlt(downUp(libevdev.EV_KEY.KEY_RIGHTBRACE))),
    'KEY_E': [less1, less0],
    'KEY_R': [shift1, 'sleep', less1, less0, shift0],
    'KEY_T': [shift1, 'sleep', three1, three0, shift0],
    'KEY_Y': [shift1, 'sleep', six1, six0, shift0],
    'KEY_U': [ralt1, 'sleep', two1, two0, ralt0],
    'KEY_I': [shift1, 'sleep', zero1, zero0, shift0],
    'KEY_O': [minus1, minus0],
    'KEY_P': [shift1, 'sleep', five1, five0, shift0],

    'KEY_A': [ralt1, 'sleep', eight1, eight0, ralt0],
    'KEY_S': [ralt1, 'sleep', nine1, nine0, ralt0],
    'KEY_D': [shift1, 'sleep', eight1, eight0, shift0],
    'KEY_F': [shift1, 'sleep', nine1, nine0, shift0],
    'KEY_G': [shift1, 'sleep', bslash1, bslash0, shift0],
    'KEY_H': [shift1, 'sleep', two1, two0, shift0],
    'KEY_J': [bslash1, bslash0],
    'KEY_K': [shift1, 'sleep', seven1, seven0, shift0],
    'KEY_L': [shift1, 'sleep', one1, one0, shift0],
    #'KEY_SEMICOLON': syn(downUp(libevdev.EV_KEY.KEY_SEMICOLON)), # let it pass through?

    'KEY_Z': [ralt1, 'sleep', four1, four0, ralt0],
    'KEY_X': [ralt1, 'sleep', seven1, seven0, ralt0],
    'KEY_C': [ralt1, 'sleep', zero1, zero0, ralt0],
    'KEY_V': [shift1, 'sleep', four1, four0, shift0],
    #'KEY_B': [],
    'KEY_N': [grave1, grave0],
    'KEY_M': [shift1, 'sleep', equal1, equal0, shift0, 'sleep', space1, space0],
    'KEY_COMMA': [equal1, equal0],
    'KEY_DOT': [shift1, 'sleep', rbrace1, rbrace0, shift0, 'sleep', space1, space0]
    # 'KEY_SLASH': []    sdfASDFasdfasfdASDF
}
"""
deadless = {
    'KEY_Z': [ctrl1, z1, z0, ctrl0, syn0],
    'KEY_X': [ctrl1, x1,x0, ctrl0, syn0],
    'KEY_C': [ctrl1, c1, c0, ctrl0, syn0],
    'KEY_V': [ctrl1, v1, v0, ctrl0, syn0],
    'KEY_B': [ctrl1, a1, a0, ctrl0, syn0],
    'KEY_E': [back1, back0, syn0],
    'KEY_R': [del1, del0, syn0]
}
deadlessNavi = {
    'KEY_A': [up1, up0, syn0],
    'KEY_S': [down1, down0, syn0],
    'KEY_D': [left1, left0, syn0],
    'KEY_F': [right1, right0, syn0],
    'KEY_Ashift': [shift1, up1, up0, shift0, syn0],
    'KEY_Sshift': [shift1, down1, down0, shift0, syn0],
    'KEY_Dshift': [shift1, left1, left0, shift0, syn0],
    'KEY_Fshift': [shift1, right1, right0, shift0, syn0],
    'KEY_Actrl': [ctrl1, up1, up0, ctrl0, syn0],
    'KEY_Sctrl': [ctrl1, down1, down0, ctrl0, syn0],
    'KEY_Dctrl': [ctrl1, left1, left0, ctrl0, syn0],
    'KEY_Fctrl': [ctrl1, right1, right0, ctrl0, syn0],
    'KEY_Ashiftctrl': [shift1, ctrl1, up1, up0, ctrl0, shift0, syn0],
    'KEY_Sshiftctrl': [shift1, ctrl1, down1, down0, ctrl0, shift0, syn0],
    'KEY_Dshiftctrl': [shift1, ctrl1, left1, left0, ctrl0, shift0, syn0],
    'KEY_Fshiftctrl': [shift1, ctrl1, right1, right0, ctrl0, shift0, syn0],

    'KEY_Aalt': [pageup1, pageup0, syn0],
    'KEY_Salt': [pagedown1, pagedown0, syn0],
    'KEY_Dalt': [home1, home0, syn0],
    'KEY_Falt': [end1, end0, syn0],
    'KEY_Aaltshift': [shift1, pageup1, pageup0, shift0, syn0],
    'KEY_Saltshift': [shift1, pagedown1, pagedown0, shift0, syn0],
    'KEY_Daltshift': [shift1, home1, home0, shift0, syn0],
    'KEY_Faltshift': [shift1, end1, end0, shift0, syn0],
    'KEY_Aaltctrl': [ctrl1, pageup1, pageup0, ctrl0, syn0],
    'KEY_Saltctrl': [ctrl1, pagedown1, pagedown0, ctrl0, syn0],
    'KEY_Daltctrl': [ctrl1, home1, home0, ctrl0, syn0],
    'KEY_Faltctrl': [ctrl1, end1, end0, ctrl0, syn0],
    'KEY_Aaltshiftctrl': [shift1, ctrl1, pageup1, pageup0, ctrl0, shift0, syn0],
    'KEY_Saltshiftctrl': [shift1, ctrl1, pagedown1, pagedown0, ctrl0, shift0, syn0],
    'KEY_Daltshiftctrl': [shift1, ctrl1, home1, home0, ctrl0, shift0, syn0],
    'KEY_Faltshiftctrl': [shift1, ctrl1, end1, end0, ctrl0, shift0, syn0]
}
"""

def selectDevice():
    print("")
    print("    Select keyboard to use with deadcaps:")
    print("")
    event_number = 0
    while True:
        event_path = f"/dev/input/event{event_number}"
        if not os.path.exists(event_path):
            break
        with open(event_path, "rb") as fd:
            fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)
            device = libevdev.Device(fd)
            if device.has(libevdev.EV_KEY.KEY_A):
                print(f"    [{event_number}]: {device.name} {len(device.evbits)}")
        event_number += 1
    res = input()
    return "/dev/input/event" + res


def debug(msg, e, caps_state):
    print("{}. CAPS_STATE: {}. Event type: {:02x} {} code {:03x} {:12s} value{:1d}".format(msg, caps_state, e.type.value, e.type.name, e.code.value, e.code.name, e.value))


def state_normal(e, key, uidev):
    if key == 'KEY_CAPSLOCK':
        return state_deadcaps
    if key == 'KEY_SEMICOLON':
        return state_semidead
#     if key == 'KEY_102ND':          # < less than key
#         return state_deadless
    uidev.send_events([e])
    return state_normal

def send_events(uidev, events):
    for ev in events:
        if ev == 'sleep':
            time.sleep(0.004)         # sleephack :(
        else:
            uidev.send_events([ev, syn0])

def state_deadcaps(e, key, uidev):
    if key == 'KEY_CAPSLOCK':
        uidev.send_events([e])
        return state_capslock
    send_events(uidev, [shift1, 'sleep', e, shift0])
    return state_normal
    
def state_capslock(e,key,uidev):
    uidev.send_events([e])
    if key == 'KEY_CAPSLOCK':
        return state_normal
    return state_capslock

def state_semidead(e,key,uidev):
    if key == 'KEY_CAPSLOCK':  # caps key doesnt work in semidead state
        return state_normal
    if key in semidead :
        send_events(uidev, semidead[key])
    else :
         uidev.send_events([e])
    return state_normal

def open_clone_keyboard(kb_path):
    fd = open(kb_path, 'rb')
    kb = libevdev.Device(fd)
    kb.grab()
    clone = kb.create_uinput_device()
    print('Device is at {}'.format(clone.devnode))
    return (kb, clone)

def event_loop(kb, kb_clone):
    state = state_normal
    for e in kb.events():
        # debug('event: ', e, state.__name__)
        if e.type.name != 'EV_KEY' or e.value == 0:
            kb_clone.send_events([e])
        else :
            state = state(e, e.code.name, kb_clone)


if __name__ == "__main__":
    print("##########################")
    print("## Welcome to deadcaps! ##")
    print("##########################")
    path = selectDevice()
    #enter bug. Wait for enter key to be released when called from command prompt.
    #250ms is default delay before repeated keystrokes.
    time.sleep(0.25)
    event_loop(*open_clone_keyboard(path))
