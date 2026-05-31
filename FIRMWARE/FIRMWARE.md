# Macropad firmware documentation

This code runs a 9-key macropad with an OLED screen, RGB lights, and a rotary encoder. It is written using KMK firmware for a Seeed Studio XIAO RP2040.

---

## Keyboard (9 keys)

There are 9 keys arranged in a 3x3 grid.

Each key is assigned:
- a label
- a keyboard shortcut or macro
- a color for its RGB LED
- an icon for the OLED screen

When a key is pressed:
- it sends a keyboard shortcut or runs a macro
- it lights up its assigned RGB color
- it triggers an OLED animation based on the key index

When released:
- all RGB LEDs are turned off

---

## OLED display

The OLED is a 128×32 SSD1306 display.

It is controlled using a custom driver that:
- writes directly to the display over I2C
- supports drawing text and bitmaps
- uses a framebuffer for rendering

The display shows different content depending on state.

---

## OLED states

The display runs a state machine with four states:

### IDLE
- Shows current time in HH:MM format
- Shows date below the time
- Colon in the time blinks every second

### SLIDE
- Displays the selected key’s bitmap
- The image slides in from the right

### HOLD
- Keeps the bitmap fully visible
- Holds for 10 seconds
- No continuous redraws during this state

### FADE
- Gradually clears the image using a pixel removal pattern
- Returns to idle state after completion

---

## Bitmaps

Each key has a 128×32 monochrome bitmap.

These bitmaps are stored as byte arrays and represent:
- app icons
- control icons
- system actions

The bitmap is displayed when the key is triggered.

---

## RGB LEDs

There are 9 NeoPixel LEDs, one per key.

Behavior:
- all LEDs are off when idle
- only the active key LED turns on
- each key has a fixed RGB color

---

## Rotary encoder

The encoder is used for volume control:
- rotating left decreases volume
- rotating right increases volume

---

## Macros

Some keys run multi-step macros instead of single shortcuts.

Examples:
- Chrome key opens Spotlight, types “Chrome”, then launches it
- Spotify key opens Spotlight and launches Spotify

Macros use delays and simulated key presses.

---

## Key press flow

When a key is pressed:

1. OLED animation is triggered (SLIDE state)
2. RGB LED for that key turns on
3. The assigned shortcut or macro runs
4. The OLED displays the bitmap
5. After 10 seconds, the screen fades back to idle

---

## Performance

The code is optimized by:
- limiting OLED refresh rate (~25 FPS)
- skipping redraws during HOLD state
- using direct bitmap writes instead of per-pixel updates

---

## Summary

This firmware controls:
- 9 programmable macro keys
- OLED display with animations
- per-key RGB lighting
- rotary encoder for volume control

It handles input, display output, and macros in a single system.
