# `python-libevdev` + `X11/xkb/symbols/deadcaps`

1. update the keyboard layout so that the altgr keys are the ones you want on the regular letters.
2. make a python script that uses libevdev to:
   1. grab the event stream of a keyboard.
   2. add a state machine to caps-lock and semicolon (right pinky finger button) so that they toggle on the first click.
3. add the keyboard layout to xkb and the python script to your start up applications.

## 1. Deadcaps xkb layout

1. Make your deadcaps keyboard layout file using: `sudo gedit /usr/share/X11/xkb/symbols/deadcaps`.
You can debug your configuration using: `xkbcomp -i 12 /usr/share/X11/xkb/symbols/deadcaps $display`.

  [deadcaps example map](symbols/deadcaps3)

2. Open `sudo gedit /usr/share/X11/xkb/rules/evdev.xml` and insert the following snippet inside the existing text.
(Don't paste the whole text, only paste the content inside the comments.)

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xkbConfigRegistry SYSTEM "xkb.dtd">
<xkbConfigRegistry version="1.1">
    <!--    ...    -->
    <layoutList>
        <!--    ...    -->
        <!--    INSERT THE CODE BELOW    -->
        <layout>
            <configItem>
                <name>deadcaps</name>

                <shortDescription>no</shortDescription>
                <description>Norwegian deadcaps</description>
                <languageList>
                    <iso639Id>nor</iso639Id>
                    <iso639Id>nob</iso639Id>
                    <iso639Id>nno</iso639Id>
                </languageList>
            </configItem>
            <variantList>
                <variant>
                    <configItem>
                        <name>deadcaps</name>
                        <description>Norwegian (deadcaps)</description>
                    </configItem>
                </variant>
            </variantList>
        </layout>
        <!--    INSERT THE CODE ABOVE    -->
        <!--    ...    -->
    </layoutList>
    <!--    ...    -->
</xkbConfigRegistry>
```

3. Restart `X11` using: `sudo systemctl restart display-manager`.

4. Open `settings` and `languages` and `add` scroll down to `other` and then search for `deadcaps`. Add it. And select it.

## 2. `deadcaps.py`

1. Install `python-libevdev`. Check out the [python-libevdev documentation](https://python-libevdev.readthedocs.io/en/latest/)
    * `sudo apt-get install -y python3-pip`
    * `sudo pip install libevdev`

2. Make `/usr/sbin/deadcaps.py`:

```python
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
```

3. Find out which `/dev/input/eventX` that your keyboard is connected to: `cat /proc/bus/input/devices`.
[explore the `/dev/input/` folder](https://thehackerdiary.wordpress.com/2017/04/21/exploring-devinput-1/).
This script is not yet good enough, so it hardcodes this keyboard into the startup command.

This python program will detect and print all the keyboards on your computer:

```python
#!/usr/bin/env python3
#
# This example illustrate how you can scan the /dev/input/eventX devices
# and list all the devices that support CAPSLOCK.


from pathlib import Path
import sys
import libevdev

def has_caps_lock(path) :
    if not path.stem.startswith('event'):
        return False
    with open(path, "rb") as fd:
        dev = libevdev.Device(fd)
        return dev.has(libevdev.EV_KEY.KEY_CAPSLOCK)
    

def devices_with_caps_lock() :
    return [p for p in Path('/dev/input/').iterdir() if has_caps_lock(p)]


def main():
    for path in devices_with_caps_lock() :
        print(path)


if __name__ == "__main__":
    main()
```

4. Open `settings => keyboard shortcut` and add a new keyboard shortcut:
   * name: `deadcaps`
   * command: `gnome-terminal -- sudo python3 /usr/sbin/deadcaps.py /dev/input/eventX`
   * shortcut: `ctrl+F10` (for example).

   The shortcut will open a terminal window and prompt you for the sudo password. By killing this terminal window later, you will terminate the deadcaps program at the same time.
   
> Todo: make the deadcaps script automatically add itself to all keyboards.

> Todo: deadless navigation: a,s,d,f = up,down,left,right(pageup/pagedown/home/end under `alt`). j,k,l = shift, ctrl, alt. that way, i could navigate using my four left fingers, while holding down j,k,l as a means to augment that navigation. In numlock navigation mode,  q = a. this way ctrl+z,x,c,v,a/q is all available.

`<` is converted into numlock. numlock mode turns normal keys into navigation keys. numlock is a normal click once to start, click again to stop, mode. numlock mode will clear any other state in deadcaps.
1. when numlock, a,s,d,f become arrow keys, and q=a (language map), 
2. make `<` into `numlock` (try language map, then script),
3. when numlock j,k,l = ctrl, shift, alt (try language map, then script),
4. asdf in numlock mode with alt becomes pagedown, pageup, home, end (try language map, then script).
