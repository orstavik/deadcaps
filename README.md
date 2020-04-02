# DeadCaps

The problem of typing is not to hit the keys; the problem of typing is to get the fingers back in their default, starting position after having hit a key. Once this is achieved, both speed, accuracy, and reduced muscle tension follow automatically.

So, how to get the fingers back to their starting position after having hit their target key? By not moving the hands!

## How to avoid moving your hands while typing?

There are a couple of sources for hand movements:
1. CAPITAL LETTERS. Capital letters require the use of shift. To use shift require moving at least one hand. Out of position. Thus, our first goal is to remove the need to use shift to create capital letters.
2. Those pesky, difficult, darn, "#¤%&! symbols. As with capital letters, symbols often require the use of shift or keys that are outside the range of normal keys. Thus, our second goal is to remove the need for shift to create symbols.
3. Arrows and navigation. Unfortunately, many apps listen for key codes instead of key symbols here. This makes it very difficult to make alter keyboard navigation and editing via the keyboard. If I manage to solve this problem, I will post my solutions here.

DeadCaps and DeadLess/SemiDead replace the use of shift for capital letters and symbols respectively by adding a dead key on CapsLock and another dead key on the lesserThan/semicolon keys on the keyboard. It is based on the following assumptions:

1. Most capital letters and symbols are written one by one (or two by two) interspersed in normal, lower-case text. Sure, sometimes (5% of the time?) you might want to write three or more symbols or capital letters at the same time, but most often you WANT to automatically turn off capital letter and symbol mode automatically after having typed one.
2. It takes more time, trial-and-errors, and muscular effort to type two keys in difficult hand positions at the same time, ie. to use shift and/or altGr, than it is to tap two keys within normal hand positions in quick succession.
3. Writing is individual, and there is no set frequency of letter and symbol combinations and frequencies that apply to all keyboard users. However, most users are in "normal" writing mode at least 90% of the time (Normal writing mode = lowercase letters, comma, period, dash, semicolon, colon, underscore, space, numbers, and enter). Most users are in  "capital"/"symbol" writing mode no more than 10% of the time.
4. "Capital"/"symbol" writing mode is in 90% of the time done as a single entry *within* normal writing mode. For example, most capital letters are singular entries: first letters of names and the first letter in a sentence. Symbols equally so: 1+1=2 is written at least 90% at the time.
5. The need to convert to either "capital" or "symbol" writing mode for more than one character at a time occurs less than 1% of the time. While the need to convert to a singular "capital" or "symbol" writing mode might occur 9% of the time.

Sticky keys is a solution to this problem. But sticky keys:
 * encompasses all modifying keys such as ctrl and alt too, not just shift, and
 * sticky keys use the slightly difficult position of the shift, not for example the better positioned caps lock key.

DeadCaps and DeadSemi/DeadLess essentially implement a "shift only sticky key on the CapsLock/Semicolon/LesserThan keys". This has the following effect that the *next* keystroke after the 9% singular capital or symbol keystrokes occur from the normal unshifted hand position, which result in a normal hand position for not only the 9% capital and symbol uncomfortable-shift-hand-position keystrokes, but also for the next 9% following, trying-to-find-back-to-normal-hand-position keystrokes. Ergo sum:
 * using shift: 80% normal keystroke.
 * DeadCaps + SemiDead: 100% normal keystrokes.

The cost in added keystrokes is only for the 1% key combinations where more than 3-4 capital and symbol letters are needed. 99% of the time, there is no added cost of using a dead key instead of an active modifier such as shift. Furthermore, as the solutions are almost without a footprint, shift or shift+caps can be used to get a normal solution to the previous problems.

## How to implement it on my computer?

### Linux
1. add a custom language layout in `/usr/share/X11/xkb/symbols`. such as
 `deadcaps` or `deadcaps2`.
 `sudo gedit /usr/share/X11/xkb/symbols/deadcaps`
2. update the `/usr/share/X11/xkb/rules/evdev.xml` file to reference your new language layout. This is not done automatically based on the presence of the layout file in the correct folder.
 `sudo gedit /usr/share/X11/xkb/rules/evdev.xml`
   * To debug your deadcaps file, do a dry run compile
`xkbcomp -i 12 /usr/share/X11/xkb/symbols/deadcaps $display`
3. Add a `.XCompose` file in the user directory.
   `gedit .XCompose`
4. To update both your .XCompose file and available languages, reload X11:
 `sudo systemctl restart display-manager`
5. in Settings, open languages and add deadcaps and deadcaps2.

### Windows:
1. download and install AutoHotKey.
2. add and run a script `deadcaps` using AutoHotKey.
3. add the deadcaps script to startup

## Considerations

DeadCaps is fairly unobtrusive. It alters as little as possible of the normal operation of all other keys and shift. As many recommend using CapsLock instead of shift for capital letters as well, users of deadCaps can transfer their new habits to normal keyboards using normal caps lock with an extra keystroke. Again, CapsLock is faster than shift. Go figure. The conclusion is that speed is not stopped by finger movement, but by hand movement.

## Future work

Implement a working mechanism for navigation. This is difficult as many text editors seem to rely on keycodes and not keysymbols for navigation, thus rendering custom keyboard setups impossible to use.



 This is demonstrated by  fast typist: writing 150wpm is possible, and using shift, altgr, and normal caps lock only reduces