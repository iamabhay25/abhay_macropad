# Auto-generated bitmap data for SSD1306 128x32 OLED (MONO_HLSB)
# Each bitmap: 128*32/8 = 512 bytes

# (ALL YOUR BITMAPS UNCHANGED ABOVE — omitted here for readability in chat,
# but in your real file, keep them exactly as-is)

ALL_BITMAPS = [BMP_SCREENSHOT_SEL, BMP_CHROME, BMP_REOPEN_TAB, BMP_FORCE_QUIT, BMP_LOCK_SCREEN, BMP_FULLSCREEN_SS, BMP_SPOTIFY, BMP_PLAY_PAUSE, BMP_SPOTLIGHT]

import board
import busio
import framebuf
import time
import supervisor
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC, Key, make_key
from kmk.scanners import DiodeOrientation
from kmk.extensions.neopixel import NeoPixel
from kmk.modules.encoder import EncoderHandler
from kmk.modules.tapdance import TapDance
from kmk.modules.macros import Macros, Tap, Delay
from kmk.hid import HIDModes
from kmk.handlers.sequences import send_string

# ============================================================
# SSD1306 DRIVER
# ============================================================

class SSD1306:
    INIT_CMDS = bytes([
        0xAE, 0xD5, 0x80, 0xA8, 0x1F, 0xD3, 0x00,
        0x40, 0x8D, 0x14, 0x20, 0x00, 0xA1, 0xC8,
        0xDA, 0x02, 0x81, 0xCF, 0xD9, 0xF1, 0xDB,
        0x40, 0xA4, 0xA6, 0x2E, 0xAF
    ])

    def __init__(self, i2c, addr=0x3C):
        self._i2c = i2c
        self._addr = addr
        self._buf = bytearray(128 * 32 // 8)
        self._fb = framebuf.FrameBuffer(self._buf, 128, 32, framebuf.MONO_HLSB)
        self._cmd(self.INIT_CMDS)

    def _cmd(self, cmds):
        for c in cmds:
            self._i2c.writeto(self._addr, bytes([0x00, c]))

    def show(self):
        self._cmd([0x21, 0, 127, 0x22, 0, 3])
        buf = bytearray(len(self._buf) + 1)
        buf[0] = 0x40
        buf[1:] = self._buf
        self._i2c.writeto(self._addr, buf)

    def fill(self, v):
        self._fb.fill(v)

    def blit_bitmap(self, bmp):
        self._buf[:] = bmp

    def text(self, s, x, y, c=1):
        self._fb.text(s, x, y, c)


# ============================================================
# OLED ANIMATOR (UNCHANGED)
# ============================================================

ANIM_DURATION_MS = 10_000

class OledAnimator:
    STATE_IDLE  = 0
    STATE_SLIDE = 1
    STATE_HOLD  = 2
    STATE_FADE  = 3

    SLIDE_FRAMES = 8
    FADE_FRAMES  = 8

    def __init__(self, display):
        self.d = display
        self._state = self.STATE_IDLE
        self._key_idx = 0
        self._frame = 0
        self._hold_start = 0
        self._last_tick = supervisor.ticks_ms()
        self._tick_interval = 40
        self._scratch = bytearray(512)
        self._dirty = True

    def trigger(self, key_idx: int):
        self._key_idx = key_idx
        self._state = self.STATE_SLIDE
        self._frame = 0
        self._dirty = True

    def tick(self):
        now = supervisor.ticks_ms()
        if (now - self._last_tick) < self._tick_interval:
            return
        self._last_tick = now

        if self._state == self.STATE_IDLE:
            self._draw_idle()
            self._dirty = True

        elif self._state == self.STATE_SLIDE:
            self._draw_slide()
            self._frame += 1
            if self._frame >= self.SLIDE_FRAMES:
                self._state = self.STATE_HOLD
                self._hold_start = now

        elif self._state == self.STATE_HOLD:
            if self._dirty:
                self._draw_hold()
                self._dirty = False
            if (now - self._hold_start) >= ANIM_DURATION_MS:
                self._state = self.STATE_FADE
                self._frame = 0
                self._dirty = True

        elif self._state == self.STATE_FADE:
            self._draw_fade()
            self._frame += 1
            if self._frame >= self.FADE_FRAMES:
                self._state = self.STATE_IDLE

        self.d.show()

    def _draw_idle(self):
        self.d.fill(0)
        t = time.localtime()
        self.d.text("{:02d}:{:02d}".format(t.tm_hour, t.tm_min), 40, 2, 1)

    def _draw_slide(self):
        bmp = ALL_BITMAPS[self._key_idx]
        src = framebuf.FrameBuffer(bytearray(bmp), 128, 32, framebuf.MONO_HLSB)
        self.d.fill(0)
        self.d.blit(src, 0, 0)

    def _draw_hold(self):
        self.d.blit_bitmap(ALL_BITMAPS[self._key_idx])

    def _draw_fade(self):
        self._scratch[:] = ALL_BITMAPS[self._key_idx]
        fb = framebuf.FrameBuffer(self._scratch, 128, 32, framebuf.MONO_HLSB)
        for i in range(0, 128, 2):
            for j in range(0, 32, 2):
                fb.pixel(i, j, 0)
        self.d.blit_bitmap(self._scratch)


# ============================================================
# KEYBOARD SETUP (UNCHANGED)
# ============================================================

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP26, board.GP27, board.GP28)
keyboard.row_pins = (board.GP4, board.GP2, board.GP1)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

i2c = busio.I2C(scl=board.GP7, sda=board.GP6)
oled = SSD1306(i2c)
animator = OledAnimator(oled)

rgb = NeoPixel(pin=board.GP3, num_pixels=9, brightness=0.5, auto_write=True)

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

# ============================================================
# FIXED KEY HANDLING (THIS IS THE ONLY REAL CHANGE)
# ============================================================

def _make_wrapped(idx):
    raw = KEY_DEFS[idx]["action"]
    color = KEY_DEFS[idx]["color"]

    def _pressed(key, keyboard, *args, **kwargs):
        animator.trigger(idx)

        # TURN EVERYTHING OFF
        rgb.fill((0, 0, 0))

        # TURN ONLY THIS ONE ON
        rgb[idx] = color

        keyboard.hid_pending = True
        keyboard.tap_key(raw)

    def _released(key, keyboard, *args, **kwargs):
        rgb.fill((0, 0, 0))

    return make_key(
        names=("AK{:d}".format(idx),),
        on_press=_pressed,
        on_release=_released,
    )


# KEY DEFINITIONS (UNCHANGED)
OPEN_SPOTIFY = KC.MACRO(Tap(KC.LGUI, KC.SPACE), Delay(200), "SPOTIFY", Tap(KC.ENTER))

KEY_DEFS = [
    {"label": "SCREENSHOT", "action": KC.LGUI(KC.LSHIFT(KC.N4)), "color": (255, 80, 0)},
    {"label": "CHROME", "action": KC.LGUI(KC.SPACE), "color": (0, 100, 255)},
    {"label": "REOPEN TAB", "action": KC.LGUI(KC.LSHIFT(KC.T)), "color": (0, 200, 200)},
    {"label": "FORCE QUIT", "action": KC.LGUI(KC.LALT(KC.ESC)), "color": (255, 0, 0)},
    {"label": "LOCK", "action": KC.LCTRL(KC.LGUI(KC.Q)), "color": (160, 0, 255)},
    {"label": "FULL SS", "action": KC.LGUI(KC.LSHIFT(KC.N3)), "color": (255, 140, 0)},
    {"label": "SPOTIFY", "action": OPEN_SPOTIFY, "color": (0, 220, 60)},
    {"label": "PLAY/PAUSE", "action": KC.MPLY, "color": (200, 200, 200)},
    {"label": "SPOTLIGHT", "action": KC.LGUI(KC.SPACE), "color": (255, 220, 0)},
]

AK = [_make_wrapped(i) for i in range(9)]

keyboard.keymap = [[AK[0], AK[1], AK[2], AK[3], AK[4], AK[5], AK[6], AK[7], AK[8]]]

class _OledTickExtension:
    def before_hid_send(self, keyboard):
        animator.tick()

keyboard.extensions.append(_OledTickExtension())

if __name__ == "__main__":
    keyboard.go()
