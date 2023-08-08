# Bug: problem X11 to Wayland transition 

When we run the script in x11, it works. When we run the script in Wayland, the script behaves weirdly.

First, we don't see the difference when we work with `xev`. In both Wayland and x11, the `xev` output seems to behave correctly.

But, when we run `evtest`, we see that the results differ. The test for the bug is as follows:
1. start the `deadcapsChristmas2.py` script.
2. run `evtest` on the cloned version of the keyboard that you have grabbed using `deadcapsChristma2.py`.

When we look at the output in the `evtest` for a "normal" `!` (press right shift + number 1), we get the following output:
```
Event: time 1691490624.920784, -------------- SYN_REPORT ------------
Event: time 1691490659.326593, type 4 (EV_MSC), code 4 (MSC_SCAN), value 700e5
Event: time 1691490659.326593, type 1 (EV_KEY), code 54 (KEY_RIGHTSHIFT), value 1
Event: time 1691490659.326593, -------------- SYN_REPORT ------------
Event: time 1691490659.586528, type 4 (EV_MSC), code 4 (MSC_SCAN), value 7001e
Event: time 1691490659.586528, type 1 (EV_KEY), code 2 (KEY_1), value 1
Event: time 1691490659.586528, -------------- SYN_REPORT ------------
!Event: time 1691490659.669539, type 4 (EV_MSC), code 4 (MSC_SCAN), value 7001e
Event: time 1691490659.669539, type 1 (EV_KEY), code 2 (KEY_1), value 0
Event: time 1691490659.669539, -------------- SYN_REPORT ------------
Event: time 1691490659.835436, type 4 (EV_MSC), code 4 (MSC_SCAN), value 700e5
Event: time 1691490659.835436, type 1 (EV_KEY), code 54 (KEY_RIGHTSHIFT), value 0
Event: time 1691490659.835436, -------------- SYN_REPORT ------------
```

When we make `!` using the deadcaps script (the semi-colon key, and then the "l" key), we have the following `evtest` output:

```
Event: time 1691490907.298172, type 4 (EV_MSC), code 4 (MSC_SCAN), value 70033
Event: time 1691490907.298172, -------------- SYN_REPORT ------------
Event: time 1691490907.386315, type 4 (EV_MSC), code 4 (MSC_SCAN), value 7000f
Event: time 1691490907.386315, type 1 (EV_KEY), code 42 (KEY_LEFTSHIFT), value 1
Event: time 1691490907.386315, type 1 (EV_KEY), code 2 (KEY_1), value 1
Event: time 1691490907.386315, type 1 (EV_KEY), code 2 (KEY_1), value 0
Event: time 1691490907.386315, type 1 (EV_KEY), code 42 (KEY_LEFTSHIFT), value 0
Event: time 1691490907.386315, -------------- SYN_REPORT ------------
!Event: time 1691490907.431083, type 4 (EV_MSC), code 4 (MSC_SCAN), value 70033
Event: time 1691490907.431083, -------------- SYN_REPORT ------------
Event: time 1691490907.496237, type 4 (EV_MSC), code 4 (MSC_SCAN), value 7000f
Event: time 1691490907.496237, -------------- SYN_REPORT ------------
```

So. First approach is to create a `SYN_REPORT` for each composed keystroke, resulting in neat (type 4, type 1, syn)-triplets.
