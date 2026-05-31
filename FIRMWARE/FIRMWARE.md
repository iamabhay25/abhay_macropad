# Macropad Documentation

## Overview

This is a 9 key macropad that connects to a computer. Each key does a shortcut so you don’t need to click around or remember key combos.

It also has a knob for volume, RGB lights under each key, and a small OLED screen.

---

## Key Functions

### Key 1
Takes a screenshot of part of the screen. You select what area to capture.

---

### Key 2
Opens Chrome in two ways:
- One press = Chrome (school profile)
- Two presses = Chrome (personal profile)

---

### Key 3
Reopens the last tab you closed in Chrome.

---

### Key 4
Opens force quit menu to close frozen apps.

---

### Key 5
Locks the computer.

---

### Key 6
Takes a screenshot of the whole screen.

---

### Key 7
Opens Spotify.

---

### Key 8
Plays or pauses music or videos.

---

### Key 9
Opens Spotlight search.

---

## Knob (Rotary Encoder)

- Turn left = volume down  
- Turn right = volume up  
- Press = does nothing

---

## RGB Lights

- 9 lights (one under each key)
- White color
- Half brightness
- No animations

---

## OLED Screen

- Small screen (128x32)
- Used for basic status info
- Connected using I2C (0x3C)

---

## How the code works

The firmware uses KMK. It does:

- Reads which key you press
- Runs macros (multiple steps at once)
- Detects single vs double press (tap dance)
- Controls the knob
- Controls lights
- Controls OLED screen

---

## Macros

### Chrome key
- Opens search (Spotlight)
- Types "Chrome"
- Presses enter
- Waits a bit
- Switches profile depending on tap

### Spotify key
- Opens search (Spotlight)
- Types "Spotify"
- Presses enter

---

## Summary

This macropad makes common actions faster by turning them into one button presses instead of using menus or shortcuts.
