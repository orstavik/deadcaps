# `python-libevdev` + `X11/xkb/symbols/deadcaps3`

1. update the keyboard layout so that the altgr keys are the ones you want on the regular letters.
2. make a python script that uses libevdev to:
   1. grab the event stream of a keyboard.
   2. add a state machine to caps-lock and semicolon (right pinky finger button) so that they toggle on the first click.
3. add the keyboard layout to xkb and the python script to your start up applications.

## 1. Deadcaps xkb layout

1. Make your deadcaps keyboard layout file using: `sudo gedit /usr/share/X11/xkb/symbols/deadcaps`.
You can debug your configuration using: `xkbcomp -i 12 /usr/share/X11/xkb/symbols/deadcaps $display`.
Fill this file with the following content:

```
// based on a keyboard map from an 'xkb/symbols/no' file

default  partial alphanumeric_keys
xkb_symbols "deadcaps" {

    // Describes the differences between a very simple en_US
    // keyboard and a Norwegian keyboard with dead key support
    // and all of ISO-8859-1 characters available.

    include "no(basic)"

    name[Group1]="Norwegian (deadcaps)";

    //latin, latin type2, no basic
//    key <TLDE>	{ [       bar,    section,    brokenbar,    paragraph ]	};
//    key <AE01>	{ [         1,     exclam,   exclamdown,  onesuperior ]	};
//    key <AE02>	{ [         2,   quotedbl,           at,  twosuperior ]	};
//    key <AE03>	{ [         3, numbersign,     sterling, threesuperior]	};
//    key <AE04>	{ [         4,   currency,       dollar,   onequarter ]	};
//    key <AE05>	{ [         5,    percent,      onehalf,    0x1002030 ]	};
//    key <AE06>	{ [         6,  ampersand,          yen,  fiveeighths ]	};
//    key <AE07>	{ [         7,      slash,    braceleft,     division ]	};
//    key <AE08>	{ [         8,  parenleft,  bracketleft, guillemotleft]	};
//    key <AE09>	{ [         9, parenrigh2t, bracketright, guillemotright] };
//    key <AE10>	{ [         0,      equal,   braceright,       degree ]	};
//    key <AE11>	{ [      plus,   question,    plusminus, questiondown ]	};
//    key <AE12>	{ [ backslash, dead_grave,   dead_acute,      notsign ]	};

    key <AD01>	{ [         q,          Q,     question,  Greek_OMEGA ]	};
    key <AD02>	{ [         w,          W,   asciitilde,      Lstroke ]	};
    key <AD03>	{ [         e,          E,         less,         cent ]	};
    key <AD04>	{ [         r,          R,      greater,    trademark ]	};
    key <AD05>	{ [         t,          T,   numbersign,        THORN ]	};
    key <AD06>	{ [         y,          Y,    ampersand,          yen ]	};
    key <AD07>	{ [         u,          U,           at,      uparrow ]	};
    key <AD08>	{ [         i,          I,        equal,     idotless ]	};
    key <AD09>	{ [         o,          O,         plus,           OE ]	};
    key <AD10>	{ [         p,          P,      percent,     Greek_PI ]	};
//    key <AD11>	{ [     aring,  Aring, dead_diaeresis, dead_abovering ]	};
//    key <AD12>	{ [dead_diaeresis, dead_circumflex, dead_tilde, dead_caron ] };


    key <AC01>	{ [         a,          A,  bracketleft,    masculine ]	};
    key <AC02>	{ [         s,          S, bracketright,      section ]	};
    key <AC03>	{ [         d,          D,    parenleft,          ETH ]	};
    key <AC04>	{ [         f,          F,   parenright,  ordfeminine ]	};
    key <AC05>	{ [         g,          G,     asterisk,          ENG ]	};
    key <AC06>	{ [         h,          H,     quotedbl,      Hstroke ]	};
    key <AC07>	{ [         j,          J,   apostrophe,    dead_horn ] };
    key <AC08>	{ [         k,          K,        slash,    ampersand ]	};
    key <AC09>	{ [         l,          L,       exclam,      Lstroke ]	};
    key <AC10>	{ [    oslash,   Ooblique,       oslash, dead_doubleacute ] }; 
//    key <AC11>	{ [        ae,         AE, dead_circumflex, dead_caron]	};

    //ATT!! the first oslash is being highjacked in the evdev script.
    //but when we press it twice, it is there in the altgr group.

//    key <BKSL>	{ [apostrophe,   asterisk, dead_doubleacute, multiply ]	};
//    key <AB01>	{ [         z,          Z, guillemotleft,        less ]	};
    key <AB02>	{ [         x,          X,    braceleft,    greater ]	};
    key <AB03>	{ [         c,          C,   braceright,    copyright ]	};
    key <AB04>	{ [         v,          V,       dollar, leftsinglequotemark ]	};
    key <AB05>	{ [         b,          B,     currency, rightsinglequotemark ] };
    key <AB06>	{ [         n,          N,          bar,            N ]	};
    key <AB07>	{ [         m,          M,        grave,    masculine ]	};
    key <AB08>	{ [     comma,  semicolon,    backslash,  dead_ogonek ]	};
    key <AB09>	{ [    period,      colon,  asciicircum, periodcentered ]	};
//    key <AB10>	{ [     minus, underscore,       endash,       emdash ]	};

//    key <LSGT>	{ [      less,    greater,      onehalf, threequarters]	};
};
```

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

2. Make `deadcaps.py` and store it in your folder for startup scripts:

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

4. Open `startup applications` from the task manager and add this script, for example: `sudo python3 ~/Desktop/deadcaps.py /dev/input/event8` 
   * debug the startup application, do: `cat /var/log/syslog | grep -B 3 -A 3 deadcaps`
