import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.extensions.neopixel import NeoPixel
from kmk.extensions.oled import Oled, OledDisplayMode
from kmk.handlers.sequences import simple_key_sequence

keyboard = KMKKeyboard()

# --------------------
# KEY PIN DEFINITIONS
# --------------------
keyboard.col_pins = (
    board.GP26,  # KEY 1
    board.GP27,  # KEY 2
    board.GP28,  # KEY 3
    board.GP29,  # KEY 4
    board.GP6,   # KEY 5 (SDA)
    board.GP7,   # KEY 6 (SCL)
)

keyboard.row_pins = ()
keyboard.diode_orientation = None

# --------------------
# OLED SETUP
# --------------------
oled = Oled(
    sda=board.GP6,
    scl=board.GP7,
    i2c_addr=0x3C,
    width=128,
    height=32,
    display_mode=OledDisplayMode.TXT,
)

keyboard.extensions.append(oled)

# --------------------
# HELPER FUNCTION
# This updates the OLED when a key is pressed
# --------------------
def show_key(oled, key_num, label):
    oled.clear()
    oled.write("Key Pressed:\n")
    oled.write(f"KEY {key_num}\n")
    oled.write(label)

# --------------------
# CUSTOM KEYS
# Each key both:
# 1. Sends its normal shortcut
# 2. Prints info to the OLED
# --------------------

KEY1 = KC.MACRO(
    simple_key_sequence(lambda *_: show_key(oled, 1, "Screenshot Sel")),
    KC.LGUI(KC.LSHIFT(KC.N4))
)

KEY2 = KC.MACRO(
    simple_key_sequence(lambda *_: show_key(oled, 2, "Save As")),
    KC.LGUI(KC.LSHIFT(KC.S))
)

KEY3 = KC.MACRO(
    simple_key_sequence(lambda *_: show_key(oled, 3, "Reopen Tab")),
    KC.LGUI(KC.LSHIFT(KC.T))
)

KEY4 = KC.MACRO(
    simple_key_sequence(lambda *_: show_key(oled, 4, "Force Quit")),
    KC.LGUI(KC.LALT(KC.ESC))
)

KEY5 = KC.MACRO(
    simple_key_sequence(lambda *_: show_key(oled, 5, "Lock Screen")),
    KC.LCTRL(KC.LGUI(KC.Q))
)

KEY6 = KC.MACRO(
    simple_key_sequence(lambda *_: show_key(oled, 6, "Shot Window")),
    KC.LGUI(KC.LSHIFT(KC.N4)),
    KC.SPACE
)

# --------------------
# RGB (SK6812)
# --------------------
rgb = NeoPixel(
    pin=board.GP3,
    num_pixels=2,
    brightness=0.3,
    auto_write=True,
)
keyboard.extensions.append(rgb)

# --------------------
# KEYMAP
# --------------------
keyboard.keymap = [
    [
        KEY1,  # KEY 1
        KEY2,  # KEY 2
        KEY3,  # KEY 3
        KEY4,  # KEY 4
        KEY5,  # KEY 5
        KEY6,  # KEY 6
    ]
]

if __name__ == "__main__":
    keyboard.go()
