# PROBLEMS Wayland vs X11

When we run the script in x11, it works. When we run the script in Wayland, the script behaves weirdly.

In Wayland:
1. 'xev' prints out the same result as in x11 (i think).
2. 'evtest' prints the wrong output. I also get a new keyboard listed in the 'evtest' list of input devices
    when the 'deadcapsChristmas2.py' script is started before 'evtest'.
