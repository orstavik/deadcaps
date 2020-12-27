# `python-libevdev` + `X11/xkb/symbols/deadcaps`

1. update the keyboard layout so that the altgr keys are the ones you want on the regular letters.
2. make a python script that uses libevdev to:
   1. grab the event stream of a keyboard.
   2. add a state machine to caps-lock and semicolon (right pinky finger button) so that they toggle on the first click.
3. add the keyboard layout to xkb and the python script to your start up applications.

## 1. Deadcaps xkb layout

1. Make your deadcaps keyboard layout file using: `sudo gedit /usr/share/X11/xkb/symbols/deadcaps`.
You can debug your configuration using: `xkbcomp -i 12 /usr/share/X11/xkb/symbols/deadcaps $display`.

  [deadcaps example map](symbols/deadcaps)

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

2. Find out which `/dev/input/eventX` that your keyboard is connected to: `cat /proc/bus/input/devices`.
[explore the `/dev/input/` folder](https://thehackerdiary.wordpress.com/2017/04/21/exploring-devinput-1/).
This script is not yet good enough, so it hardcodes this keyboard into the startup command.

3. Make [`/usr/sbin/deadcaps.py`](deadcaps.py).

   * [detectKeyboard.py](detectKeyboard.py) will detect and print all the keyboards on your computer.

4. Open `settings => keyboard shortcut` and add a new keyboard shortcut:
   * name: `deadcaps`
   * command: `gnome-terminal -- sudo python3 /usr/sbin/deadcaps.py /dev/input/eventX`
   * shortcut: `ctrl+F10` (for example).

   The shortcut will open a terminal window and prompt you for the sudo password. By killing this terminal window later, you will terminate the deadcaps program at the same time.
   
> Todo: make the deadcaps script automatically add itself to all keyboards.

## deadless navigation

Triggered by pressing lesserThan (key to the left of Z). Enables navigation and editing mode using default hand position. 

* a,s,d,f = up,down,left,right(pageup/pagedown/home/end) 
* j,k,l = shift, ctrl, PageUpDownHomeEnd.
* e,r = delete, backspace
* z,x,c,v,b = z,x,c,v,a
* space and lesserThan will exit deadless navigation.

todo: common patterns for error navigation, such as u = mark the entire word? i = mark two words back? o = mark three words back?
