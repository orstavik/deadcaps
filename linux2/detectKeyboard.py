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
