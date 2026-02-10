import board
import time
import threading
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
# RGB
# --------------------
rgb = NeoPixel(
    pin=board.GP3,
    num_pixels=2,
    brightness=1.0,
    auto_write=True,
)
keyboard.extensions.append(rgb)

# Default to white
rgb.fill((255, 255, 255))

# --------------------
# LED Helper Functions
# --------------------
blinking_flag = False  # global flag to control blinking

def blink_color(color, times=1, delay=0.2):
    """Blink all LEDs a fixed number of times, then return to white"""
    for _ in range(times):
        rgb.fill(color)
        time.sleep(delay)
        rgb.fill((0, 0, 0))
        time.sleep(delay)
    rgb.fill((255, 255, 255))  # back to default white

def blink_while_running(color=(0,0,255), interval=0.2):
    """Blink LEDs continuously while blinking_flag is True"""
    while blinking_flag:
        rgb.fill(color)
        time.sleep(interval)
        rgb.fill((0,0,0))
        time.sleep(interval)
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
# GLOBAL KEYPRESS HOOK
# --------------------
def on_key_press(key):
    """Blink LEDs for any key, macro or normal shortcut"""
    global blinking_flag
    blinking_flag = True
    
    # Start blinking in a separate thread
    t = threading.Thread(target=blink_while_running)
    t.start()

    # Run the key action if callable (macro or tapdance)
    if callable(key):
        key()  # execute macro or tapdance
    
    # Stop blinking when done
    blinking_flag = False
    t.join()

    # Blink red once to signal completion
    blink_color((0,255,0), times=2)

# Register the hook
keyboard.pre_keypress.append(on_key_press)

# --------------------
# KEYMAP
# --------------------
keyboard.keymap = [
    [
        KC.LGUI(KC.LSHIFT(KC.N4)),  # 1: Screenshot
        CHROME_SELECTOR,            # 2: TAP ONCE FOR SCHOOL / TWICE FOR PERSONAL
        KC.LGUI(KC.LSHIFT(KC.T)),   # 3: Reopen Tab
        KC.LGUI(KC.LALT(KC.ESC)),   # 4: Force Quit
        KC.LCTRL(KC.LGUI(KC.Q)),    # 5: Lock Screen
        KC.LGUI(KC.LSHIFT(KC.N4), KC.SPACE), # 6: Screenshot Whole Screen
    ]
]

if __name__ == "__main__":
    keyboard.go()
