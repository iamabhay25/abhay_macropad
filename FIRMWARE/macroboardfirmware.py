import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation

from kmk.extensions.neopixel import NeoPixel
from kmk.extensions.oled import Oled

from kmk.modules.encoder import EncoderHandler
from kmk.modules.tapdance import TapDance
from kmk.modules.macros import Macros, Tap, Delay

keyboard = KMKKeyboard()

# ============================================================
# MODULES
# ============================================================

tapdance = TapDance()
keyboard.modules.append(tapdance)

macros = Macros()
keyboard.modules.append(macros)

# ============================================================
# MATRIX (3x3)
# ============================================================

keyboard.col_pins = (
    board.GP26,
    board.GP27,
    board.GP28,
)

keyboard.row_pins = (
    board.GP4,
    board.GP2,
    board.GP1,
)

keyboard.diode_orientation = DiodeOrientation.COL2ROW

# ============================================================
# OLED
# ============================================================

oled = Oled(
    sda=board.GP6,
    scl=board.GP7,
    i2c_addr=0x3C,
    width=128,
    height=32,
)

keyboard.extensions.append(oled)

# ============================================================
# RGB LEDs
# ============================================================

rgb = NeoPixel(
    pin=board.GP3,
    num_pixels=9,
    brightness=0.5,
    auto_write=True,
)

keyboard.extensions.append(rgb)

rgb.fill((255, 255, 255))

# ============================================================
# ROTARY ENCODER
# ============================================================

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

encoder_handler.pins = (
    (board.GP29, board.GP0, None),
)

encoder_handler.map = [
    (
        (KC.VOLD, KC.VOLU, KC.NO),
    ),
]

# ============================================================
# MACROS
# ============================================================

OPEN_CHROME_SCHOOL = KC.MACRO(
    Tap(KC.LGUI, KC.SPACE),
    Delay(200),
    "CHROME",
    Tap(KC.ENTER),
    Delay(600),
    *([Tap(KC.TAB)] * 10)
)

OPEN_CHROME_PERSONAL = KC.MACRO(
    Tap(KC.LGUI, KC.SPACE),
    Delay(200),
    "CHROME",
    Tap(KC.ENTER),
    Delay(600),
    *([Tap(KC.TAB)] * 7)
)

CHROME_SELECTOR = KC.TD(
    OPEN_CHROME_SCHOOL,      # Single tap
    OPEN_CHROME_PERSONAL     # Double tap
)

OPEN_SPOTIFY = KC.MACRO(
    Tap(KC.LGUI, KC.SPACE),
    Delay(200),
    "SPOTIFY",
    Tap(KC.ENTER),
    Delay(500),
)

# ============================================================
# KEYMAP
# ============================================================

keyboard.keymap = [
    [
        KC.LGUI(KC.LSHIFT(KC.N4)),  # 1 Screenshot Selection
        CHROME_SELECTOR,            # 2 Chrome School/Personal
        KC.LGUI(KC.LSHIFT(KC.T)),   # 3 Reopen Closed Tab

        KC.LGUI(KC.LALT(KC.ESC)),   # 4 Force Quit
        KC.LCTRL(KC.LGUI(KC.Q)),    # 5 Lock Screen
        KC.LGUI(KC.LSHIFT(KC.N3)),  # 6 Full Screen Screenshot

        OPEN_SPOTIFY,               # 7 Open Spotify
        KC.MPLY,                    # 8 Play/Pause
        KC.LGUI(KC.SPACE),          # 9 Spotlight
    ]
]

# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    keyboard.go()
