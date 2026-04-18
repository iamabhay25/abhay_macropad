import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.extensions.neopixel import NeoPixel
from kmk.extensions.oled import Oled, OledDisplayMode
from kmk.modules.tapdance import TapDance
from kmk.modules.macros import Tap, Delay

keyboard = KMKKeyboard()

# --------------------
# KEY PINS
# --------------------
keyboard.col_pins = (
    board.GP26,  # KEY 1
    board.GP27,  # KEY 2
    board.GP28,  # KEY 3
    board.GP29,  # KEY 4
    board.GP6,   # KEY 5
    board.GP7,   # KEY 6
)
keyboard.row_pins = ()
keyboard.diode_orientation = None

# --------------------
# OLED
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
# RGB (6 LEDs total)
# --------------------
rgb = NeoPixel(
    pin=board.GP3,
    num_pixels=6,
    brightness=0.3,  # lower brightness = cleaner underglow + safer power draw
    auto_write=True,
)
keyboard.extensions.append(rgb)

# Set constant white underglow
rgb.fill((255, 255, 255))

# --------------------
# CHROME TAP DANCE
# --------------------
OPEN_CHROME_SCHOOL = KC.MACRO(
    Tap(KC.LGUI, KC.SPACE), Delay(200), "CHROME", Tap(KC.ENTER), Delay(600),
    *([Tap(KC.TAB)] * 10)
)

OPEN_CHROME_PERSONAL = KC.MACRO(
    Tap(KC.LGUI, KC.SPACE), Delay(200), "CHROME", Tap(KC.ENTER), Delay(600),
    *([Tap(KC.TAB)] * 7)
)

CHROME_SELECTOR = KC.TD(
    OPEN_CHROME_SCHOOL,    # 1 Tap → School
    OPEN_CHROME_PERSONAL   # 2 Taps → Personal
)

# --------------------
# KEYMAP
# --------------------
keyboard.keymap = [
    [
        KC.LGUI(KC.LSHIFT(KC.N4)),              # 1: Screenshot
        CHROME_SELECTOR,                       # 2: Chrome selector
        KC.LGUI(KC.LSHIFT(KC.T)),              # 3: Reopen Tab
        KC.LGUI(KC.LALT(KC.ESC)),              # 4: Force Quit
        KC.LCTRL(KC.LGUI(KC.Q)),               # 5: Lock Screen
        KC.LGUI(KC.LSHIFT(KC.N4), KC.SPACE),   # 6: Screenshot Whole Screen
    ]
]

if __name__ == "__main__":
    keyboard.go()
